from django.contrib.auth.models import AbstractUser
from django.db import models


# Cloudinary uploads will be stored under "accounts/<username>/<filename>"
def profile_image_path(instance, filename):
    return f"accounts/{instance.username}/{filename}"


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to=profile_image_path,  #  Cloudinary folder path
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username
