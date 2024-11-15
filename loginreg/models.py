from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    isadmin = models.BooleanField(default=False)  
    def is_member_of(self, society):
        return society.members.filter(id=self.id).exists()
