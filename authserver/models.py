from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    verified = models.BooleanField(default=False)
    uuid = models.CharField(max_length=50, blank=True)
    graduating_year = models.IntegerField(default=2030)
    email_code = models.CharField(max_length=50, blank=True)
    pass


class PermManager(models.Model):
    class Meta:
        managed = False

        default_permissions = ()

        permissions = (
            ('club_attendance_admin', 'Club Attendance admin'),
            ('bathroom_pass_admin', 'Bathroom Pass admin')
        )
