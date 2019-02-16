""" forms """

from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext, gettext_lazy as _

class ChangePasswordForm(forms.Form):
    """ User password change form """
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder':'Enter your old password'
            }),
        required=False
    )

    new_password1 = forms.CharField(
        label=_("New password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder':'Enter your new password'
            }),
        required=False
    )

    new_password2 = forms.CharField(
        label=_("Verify new password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder':'Verify your new password'
            }),
        required=False
    )

    error_messages = {
        'password_mismatch': ("The new password did not match the verification password."),
        'both_pass_fields': ("If you are changing your password, you need to enter all fields."),
        'password_incorrect': _("Your old password was entered incorrectly. Please enter it again."),
    }


    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        """ Validates that the old_password field is correct. """
        old_password = self.cleaned_data["old_password"]
        if old_password:
            if not self.user.check_password(old_password):
                raise forms.ValidationError(
                    self.error_messages['password_incorrect'],
                    code='password_incorrect',
                )
            return old_password

    def clean_new_password2(self):
        """ Validate that the new passwords match """
        oldpw = self.cleaned_data.get('old_password')
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        """ Save the new password for the user """
        if self.cleaned_data.get('new_password2'):
            self.user.set_password(self.cleaned_data.get('new_password2'))
            if commit:
                self.user.save()
        return self.user
