from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    isadmin = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to="profile_pictures/", default="profile_pictures/default.png")
    def is_member_of(self, society):
        return society.members.filter(id=self.id).exists()
