from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    isadmin = models.BooleanField(default=False)  

