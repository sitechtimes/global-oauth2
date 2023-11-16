from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import CustomUser


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")
