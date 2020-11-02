from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Account, Profile

class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password']

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username']

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image', 'name', 'gender', 'age', 'phone', 'major', 'minor', 'graduation', 'zoom_link']