from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from .models import Profile

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=24, help_text='Required. 24 characters or fewer.')
    first_name = forms.CharField(max_length=30, help_text='Required.')
    last_name = forms.CharField(max_length=30, help_text='Required.')
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    password1 = forms.CharField(max_length=254, label='Password', help_text='Required. Must contain at least 8 characters.', widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=254, label='Password confirmation', help_text='Required. Enter indentical password for verification', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(help_text='Required. Must be at least 18 years old.', widget=forms.TextInput(attrs={'placeholder': 'MM/DD/YYYY'}))
    phone_number = forms.CharField(help_text='Required. Enter a valid phone number.', widget=forms.TextInput(attrs={'placeholder': '8888888888'}))

    class Meta:
        model = Profile
        fields= ('date_of_birth', 'phone_number', 'address', 'city', 'state', 'zipcode')