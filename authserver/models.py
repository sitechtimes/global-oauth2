from django.db import models

# Create your models here.


class AccessToken(models.Model):
    token = models.CharField(max_length=100)


class RefreshToken(models.Model):
    token = models.CharField(max_length=100)


class User(models.Model):
    email = models.EmailField(primary_key=True)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    access_token = models.OneToOneField(
        AccessToken,
        on_delete=models.CASCADE,
    )
    refresh_token = models.OneToOneField(
        RefreshToken,
        on_delete=models.CASCADE
    )
    is_verified = models.BooleanField(default=False)
    graduation_year = models.IntegerField(max_length=4)

    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class AuthorizationCode(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=64)
