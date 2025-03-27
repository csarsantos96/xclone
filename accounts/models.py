from django.db import models
from django.contrib.auth.models import AbstractUser


def profile_image_upload_path(instance, filename):
    return f'profile_images/{instance.username}/{filename}'


class CustomUser(AbstractUser):

    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )

    name = models.CharField(max_length=255, blank=True, null=True)


    profile_image = models.ImageField(
        upload_to=profile_image_upload_path,
        blank=True,
        null=True
    )
    def __str__(self):
        return self.username
