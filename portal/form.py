from django import forms
from .models import UserProfile
from django.contrib.auth.models import User


class Userform(forms.ModelForm):

    class Meta:
        model = User
        exclude =("username",)

class UserProfileform(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = "__all__" 