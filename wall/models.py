from django.db import models

from Social_Media_API import settings


class Hashtag(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=64)
    content = models.TextField(blank=True)
    published = models.DateTimeField(auto_now_add=True)
    hashtags = models.ManyToManyField(Hashtag, related_name="posts", blank=True)
    user = models.ForeignKey(
        "Profile",
        on_delete=models.CASCADE,
        related_name="posts",
        blank=True,
    )

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    username = models.CharField(max_length=64, blank=True)
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    bio = models.TextField(blank=True)
    email = models.EmailField(max_length=254, blank=True)
    follow = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="user_followers", blank=True
    )

    def __str__(self):
        return str(self.user)
