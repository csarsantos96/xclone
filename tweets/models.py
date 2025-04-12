from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Tweet(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tweets"
    )
    content = models.CharField(max_length=280, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    media = models.ImageField(upload_to='tweets_media/', null=True, blank=True)

    def __str__(self):
        return f"{self.author.username}: {self.content[:30]}"


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tweet = models.ForeignKey('Tweet', on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tweet')


class Repost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    original_tweet = models.ForeignKey('Tweet', on_delete=models.CASCADE, related_name='reposts')
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tweet = models.ForeignKey('Tweet', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class TweetMedia(models.Model):
    MEDIA_TYPES = (
        ('photo', 'Foto'),
        ('gif', 'GIF'),
        ('video', 'Vídeo'),
    )
    tweet = models.ForeignKey(
        Tweet,
        on_delete=models.CASCADE,
        related_name='tweet_medias'
    )
    file = models.FileField(upload_to='tweet_media/')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)

    def __str__(self):
        return f"{self.tweet} - {self.media_type}"
