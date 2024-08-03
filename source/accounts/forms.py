from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from accounts.models import Profile


class MyUserCreationForm(UserCreationForm):
    avatar = forms.ImageField(required=False, label='Аватар')

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'password1', 'password2', 'avatar']


class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar"]
