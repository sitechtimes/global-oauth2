from django.contrib.auth.forms import UserCreationForm, password_validation
from django import forms
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from .models import User
import uuid


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")


class ChangePasswordForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    def clean_passwords(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                "The two password fields didn't match.",
                code="password_mismatch"
            )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class ForgotEmailMailer(forms.Form):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    def send(self):
        email = self.cleaned_data["email"]
        user = User.objects.get(email__iexact=email)
        if not user:
            raise ValidationError(
                "A user with that email does not exist.",
                code="user_nonexistent"
            )
        code = uuid.uuid4()
        user.email_code = code
        user.save()
        send_mail(
            subject="Password Reset Link",
            message=f"Click this link to reset your password. DO NOT SHARE THIS LINK WITH ANYONE. http://127.0.0.1:8000/users/reset_password?code={code}",
            from_email="noreplysitechlogin@gmail.com",
            recipient_list=[email]
        )
