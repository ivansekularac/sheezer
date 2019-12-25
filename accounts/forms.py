from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


# Create new form using ModelForm class
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']


class ProfileUpdateForm(forms.ModelForm):
    #image = forms.ImageField()

    class Meta:
        model = Profile
        fields = ['image']
