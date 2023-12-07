from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    verified = models.BooleanField(default=False)
    email_code = models.CharField(max_length=50, blank=True)
    pass
