from django import forms
from django.contrib.auth.models import User as UserModel
from django.core.exceptions import ValidationError
from django.contrib.auth.views import PasswordResetView

from .models import(
    Profile as ProfileModel,
)

from utils.base_alerts import BaseAlert


class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your UserName'
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your Email'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your Password'
            }
        )
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm Your Password'
            }
        )
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        user = UserModel.objects.filter(username=username).exists()
        # exists work for 'filter' because if username not exists in db,
        # ' ' returned empty query_set but 'get' returned DoseNotExist if
        # username not exists in db
        if user:
            raise ValidationError(BaseAlert.username_already_exist)
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        user = UserModel.objects.filter(email=email).exists()
        if user:
            raise ValidationError(BaseAlert.email_already_exist)
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValidationError(BaseAlert.password_must_math)
        return password

    def save(self, commit=True):
        password = self.cleaned_data.get('password')
        user = super().save(commit=False)
        user.set_password(password)
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your Username or Email'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your Password'
            }
        )
    )


class UserProfileEditForm(forms.ModelForm):
    age = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your Age...',
            }
        )
    )
    bio = forms.CharField(
        label='Biography',
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your Biography...',
            },
        ),
    )
    address = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your Address...',
            },
        ),
    )

    class Meta:
        model = UserModel
        fields = (
            'first_name',
            'last_name',
            'email',
        )
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Your First Name...',
                },
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Your Last Name...',
                },
            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Your Email Address...',
                },
            ),
        }
