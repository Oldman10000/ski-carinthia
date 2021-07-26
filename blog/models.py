from django.db import models
from django.utils import timezone

from profiles.models import UserProfile


class Post(models.Model):
    """
    blog post
    """
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='blogs'
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(
        blank=True, null=True, default=timezone.now)
    views = models.IntegerField(default=0)
    tag = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.title


class PostComment(models.Model):
    """
    allows user to add comment to blog
    """
    author = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, null=True, blank=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    published_date = models.DateTimeField(
        blank=True, null=True, default=timezone.now)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.content
