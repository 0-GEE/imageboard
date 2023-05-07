from django.db import models
from django.contrib.auth.models import User


class Posting(models.Model):
    title = models.CharField(max_length=50)
    upload_date = models.DateTimeField(auto_now=True)
    file = models.ImageField(upload_to='imageboard')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=0)


class Comment(models.Model):
    posted_at = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=200)
    post = models.ForeignKey(Posting, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=40)
    post = models.ForeignKey(Posting, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'name')