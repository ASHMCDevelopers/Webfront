from django import forms

# from django.contrib.auth.models import User


class LandingLoginForm(forms.Form):
    username = forms.CharField(
            max_length=30,
            widget=forms.TextInput(
                attrs={
                    'placeholder': 'username',
                }
            )
        )

    password = forms.CharField(
            widget=forms.PasswordInput(
                attrs={
                    'placeholder': 'password',
                }
            )
        )
