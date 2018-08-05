from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=30, help_text='24 characters or fewer.')
    first_name = forms.CharField(max_length=30, help_text=' ')
    last_name = forms.CharField(max_length=30, help_text=' ')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address.')
    password1 = forms.CharField(max_length=254, label='Password', help_text='Must contain at least 8 characters.', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    date_of_birth = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}), help_text='Must be at least 18 years old.')
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '888-888-8888'}))

    class Meta:
        model = Profile
        fields= ('date_of_birth', 'phone_number', 'address', 'city', 'state', 'zipcode')