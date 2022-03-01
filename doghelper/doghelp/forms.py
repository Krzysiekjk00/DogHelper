from django import forms
from django.core.exceptions import ValidationError
from doghelp.validators import validate_username
# from django.contrib.auth.forms import UserCreationForm
from doghelp.models import Case, Video


class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class NewUserForm(forms.Form):
    username = forms.CharField(label='Username', min_length=3, max_length=64, validators=[validate_username])
    password1 = forms.CharField(label='Password', min_length=4, max_length=64, widget=forms.PasswordInput())
    password2 = forms.CharField(label='Repeated password', min_length=4, max_length=64, widget=forms.PasswordInput())
    email = forms.EmailField()
    is_specialist = forms.BooleanField(label='Sign up as specialist', required=False)

    def clean(self):
        cleaned_data = super().clean()
        pass_1 = cleaned_data['password1']
        pass_2 = cleaned_data['password2']
        if pass_1 != pass_2:
            raise ValidationError('Given password does not equal to the repeated one.')


# class NewUserForm(UserCreationForm):
#     email = forms.EmailField()
#     is_specialist = forms.BooleanField(label='Sign up as specialist', required=False)


class VideosForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['name', 'videofile', 'author']
        widgets = {'author': forms.HiddenInput()}


# class NewCaseForm(forms.ModelForm):
#     class Meta:
#         model = Case
#         exclude = ['creation_date', 'last_modified', 'status', 'author', 'pet_specialist']
