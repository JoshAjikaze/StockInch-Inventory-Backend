from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'phone_number', 'password1', 'password2', 'role', 'address')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'phone_number', 'role', 'address')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'phone_number', 'email', 'address', 'profile_picture']
        widgets = {
            'email': forms.EmailInput(attrs={'readonly': 'readonly'}),
        }