""" forms """

from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email, RegexValidator
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Profile


class RegistrationForm(UserCreationForm):
    """User password change form"""

    username = forms.CharField(
        validators=[RegexValidator(regex="[a-zA-Z0-9_-]+")],
        label=_("Username"),
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        ),
        required=True,
        help_text="Username can only contain a-zA-Z, 0-9 and -_",
    )

    email = forms.EmailField(
        validators=[validate_email],
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}
        ),
        required=True,
        help_text="Your email will only be used for password resets. It will never be shared with third-party services.",
    )

    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
        required=True,
    )

    password2 = forms.CharField(
        label=_("Verify new password"),
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Verify Password"}
        ),
        required=True,
    )

    class Meta:
        model = Profile
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )

    def clean_email(self):
        """Check if email exists"""
        email = self.cleaned_data["email"]
        if not Profile.objects.filter(email=email).exists():
            return email

        raise ValidationError(_("Email address already exists."))
