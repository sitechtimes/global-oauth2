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
        self.request = kwargs.pop("request")
        self.user = self.request.user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    old_password = forms.CharField(
        label="Old password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )
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
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError(
                "Your old password was entered incorrectly. Please enter it again.",
                code="password_incorrect"
            )
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

    def generate_code(self):
        email = self.cleaned_data["email"]
        user = User.objects.get(email__iexact=email)
        if not user:
            raise ValidationError(
                "A user with that email does not exist.",
                code="user_nonexistent"
            )
        code = uuid.uuid4()
        user.email_code = code

    def send(self):
        email = self.cleaned_data["email"]
        send_mail
