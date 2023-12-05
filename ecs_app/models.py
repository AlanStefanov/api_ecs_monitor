# models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class UserProfile(AbstractUser):
    # Campos adicionales que desees agregar
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.username
