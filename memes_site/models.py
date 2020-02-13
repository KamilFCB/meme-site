from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Image(models.Model):
    """
        Stores a single image, related to :model:`auth.User`
    """
    title = models.CharField(max_length=30)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='static/uploads/', default='')
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)

    def is_valid(self):
        return self.image.width < 700


class Comment(models.Model):
    """
        Represents a single comment, related to :model:`auth.User` and :model:`memes_site.Image`
    """
    content = models.CharField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)


class Vote(models.Model):
    """
        Stores a single vote, related to :model:`auth.User`, :model:`memes_site.Image`
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    VOTE_TYPE = [
        ('UP', 'Vote up'),
        ('DOWN', 'Vote down')
    ]
    type = models.CharField(max_length=5, choices=VOTE_TYPE)


class CommentVote(models.Model):
    """
        Stores a single comment vote, related to :model:`auth.User`, :model:`memes_site.Comment`
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    VOTE_TYPE = [
        ('UP', 'Vote up'),
        ('DOWN', 'Vote down')
    ]
    type = models.CharField(max_length=5, choices=VOTE_TYPE)
