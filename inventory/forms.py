from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=30, help_text='24 characters or fewer.')
    first_name = forms.CharField(max_length=30, help_text=' ')
    last_name = forms.CharField(max_length=30, help_text=' ')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address.')
    password1 = forms.CharField(max_length=254, label='Password', help_text='Must contain at least 8 characters.', widget=forms.PasswordInput)
    date_of_birth = forms.DateField(widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')