from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.db import models


class AppUser(AbstractUser):
    profile_picture = CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return self.username
