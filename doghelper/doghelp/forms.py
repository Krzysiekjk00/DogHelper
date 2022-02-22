from django import forms
from django.core.exceptions import ValidationError
from doghelp.validators import validate_username


class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class NewCommonUserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=64, validators=[validate_username])
    password = forms.CharField(label='Password', max_length=64, widget=forms.PasswordInput())
    repassword = forms.CharField(label='Repeated password', max_length=64, widget=forms.PasswordInput())
    email = forms.EmailField()

    def clean(self):
        cleaned_data = super().clean()
        pass_1 = cleaned_data['password']
        pass_2 = cleaned_data['repassword']
        if pass_1 != pass_2:
            raise ValidationError('Given password does not equal to repeated one.')
