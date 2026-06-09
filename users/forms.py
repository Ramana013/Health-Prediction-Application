# users/forms.py

from django import forms
from datetime import date
from .models import User
import re


class UserRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm Password'
            }
        ),
        label='Confirm Password'
    )
    class Meta:
        model = User
        fields = ['full_name', 'date_of_birth', 'email_address', 'password']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'email_address': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }),

        }

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')

        if dob > date.today():
            raise forms.ValidationError(
                "Date of Birth cannot be a future date."
            )

        return dob

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise forms.ValidationError(
                "Password must contain at least 8 characters."
            )

        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError(
                "Password must contain at least one uppercase letter."
            )

        if not re.search(r'[a-z]', password):
            raise forms.ValidationError(
                "Password must contain at least one lowercase letter."
            )

        if not re.search(r'\d', password):
            raise forms.ValidationError(
                "Password must contain at least one number."
            )

        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
            raise forms.ValidationError(
                "Password must contain at least one special character."
            )

        return password

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                self.add_error(
                    'confirm_password',
                    "Password and Confirm Password must match."
                )

        return cleaned_data