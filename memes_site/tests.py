from django.contrib.auth.models import User
from django.test import TestCase, Client

# Create your tests here.
from django.urls import reverse

from memes_site.models import Image, Vote, Comment, CommentVote


class SiteTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin', email='k@k.pl')
        self.image = Image.objects.create(author=self.user, title="test")
        self.comment = Comment.objects.create(content="test", author=self.user, image=self.image)
        self.client = Client()
        self.client.login(username='admin', password='admin')

    def test_upload_view_without_login(self):
        url = reverse('memes:image_upload')
        response = self.client.get(url)
        self.assertEqual(response.url, "/account/login/?next=/image/upload/")

    def test_upload_view_with_login(self):
        url = reverse('memes:image_upload')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_image_vote_up(self):
        url = reverse('memes:vote_up', kwargs={'image_id': 1})
        self.client.get(url)
        self.assertEqual(Vote.objects.filter(image=self.image, type="UP").count(), 1)
        self.assertEqual(Vote.objects.filter(image=self.image, type="down").count(), 0)

    def test_image_vote_down(self):
        url = reverse('memes:vote_down', kwargs={'image_id': 1})
        self.client.get(url)
        self.assertEqual(Vote.objects.filter(image=self.image, type="UP").count(), 0)
        self.assertEqual(Vote.objects.filter(image=self.image, type="DOWN").count(), 1)

    def test_image_double_vote_down(self):
        url = reverse('memes:vote_down', kwargs={'image_id': 1})
        self.client.get(url)
        self.client.get(url)
        self.assertEqual(Vote.objects.filter(image=self.image, type="UP").count(), 0)
        self.assertEqual(Vote.objects.filter(image=self.image, type="DOWN").count(), 0)

    def test_image_vote_up_and_down(self):
        url = reverse('memes:vote_up', kwargs={'image_id': 1})
        self.client.get(url)
        url = reverse('memes:vote_down', kwargs={'image_id': 1})
        self.client.get(url)
        self.assertEqual(Vote.objects.filter(image=self.image, type="UP").count(), 0)
        self.assertEqual(Vote.objects.filter(image=self.image, type="DOWN").count(), 1)

    def test_comment_vote_up(self):
        url = reverse('memes:comment_vote', kwargs={'vote_type': 'vote_up', 'comment_id': 1})
        self.client.get(url)
        self.assertEqual(CommentVote.objects.filter(comment=self.comment, type="UP").count(), 1)
        self.assertEqual(CommentVote.objects.filter(comment=self.comment, type="DOWN").count(), 0)

    def test_comment_vote_down(self):
        url = reverse('memes:comment_vote', kwargs={'vote_type': 'vote_down', 'comment_id': 1})
        self.client.get(url)
        self.assertEqual(CommentVote.objects.filter(comment=self.comment, type="UP").count(), 0)
        self.assertEqual(CommentVote.objects.filter(comment=self.comment, type="DOWN").count(), 1)

    def test_comment_vote_up_and_down(self):
        url = reverse('memes:comment_vote', kwargs={'vote_type': 'vote_up', 'comment_id': 1})
        self.client.get(url)
        url = reverse('memes:comment_vote', kwargs={'vote_type': 'vote_down', 'comment_id': 1})
        self.client.get(url)
        self.assertEqual(CommentVote.objects.filter(comment=self.comment, type="UP").count(), 0)
        self.assertEqual(CommentVote.objects.filter(comment=self.comment, type="DOWN").count(), 1)

    def test_comment_add(self):
        url = reverse('memes:create_comment', kwargs={'image_id': self.image.id})
        self.client.post(url, {'comment': "test"})
        self.assertEqual(Comment.objects.count(), 2)

    def test_comment_add_without_login(self):
        self.client.logout()
        url = reverse('memes:create_comment', kwargs={'image_id': self.image.id})
        self.client.post(url, {'comment': "test"})
        self.assertEqual(Comment.objects.count(), 1)

    def test_comment_delete(self):
        url = reverse('memes:delete_comment')
        self.client.post(url, {'comment_id': self.comment.id,
                               'next': '/'})
        self.assertEqual(Comment.objects.count(), 0)

    def test_another_user_comment_delete(self):
        user = User.objects.create_user(username='kamil', password='kamil', email='kamil@kamil.pl')
        comment = Comment.objects.create(content="test2", author=user, image=self.image)
        url = reverse('memes:delete_comment')
        response = self.client.post(url, {'comment_id': comment.id,
                                          'next': '/'})
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(response.url, '/')
