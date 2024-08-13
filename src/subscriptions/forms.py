from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
import uuid
from django import forms

import unicodedata
from django.contrib.auth.forms import PasswordResetForm as BasePasswordResetForm

from .models import Client, Profile


class UserCreationForm(BaseUserCreationForm):

    client = forms.ModelChoiceField(queryset=Client.objects)

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['password1'].required = True
        self.fields['password2'].required = True
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = super(UserCreationForm, self).clean_password2()
        if bool(password1) ^ bool(password2):
            raise forms.ValidationError('Fill out both password fields')
        return password2

    def save(self, commit=True):
        client = self.cleaned_data['client']
        # save user first
        user = super(UserCreationForm, self).save(commit=False)
        user.username = uuid.uuid4()
        user.save()

        # update profile to match form data
        profile = user.profile
        profile.client = client
        profile.save()
        return user


UserModel = get_user_model()


class PasswordResetForm(BasePasswordResetForm):
    def _unicode_ci_compare(self, s1, s2):
        """
        Perform case-insensitive comparison of two identifiers, using the
        recommended algorithm from Unicode Technical Report 36, section
        2.11.2(B)(2).
        """
        return unicodedata.normalize('NFKC', s1).casefold() == unicodedata.normalize('NFKC', s2).casefold()

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This customized class allow users with unusable password to recovery password,
        but still block all inactive users
        """
        email_field_name = UserModel.get_email_field_name()
        active_users = UserModel._default_manager.filter(**{
            '%s__iexact' % email_field_name: email,
            'is_active': True,
        })
        return (
            u for u in active_users
            if self._unicode_ci_compare(email, getattr(u, email_field_name))
        )
