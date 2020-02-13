from django.contrib.auth.models import User
from django.test import TestCase, Client

# Create your tests here.
from django.urls import reverse


class SiteTests(TestCase):
    def setUp(self):
        return User.objects.create(username='admin', password='admin', email='k@k.pl')

    def test_upload_without_login(self):
        client = Client()
        url = reverse('memes:image_upload')
        # print(User.objects.count())
        # print(client.login(username='admin', password='admin'))
        print(client.login(username='admin', password='admin'))
        response = client.get(url)
        self.assertEqual(response.url, "/account/login/?next=/image/upload/")