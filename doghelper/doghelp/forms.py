from django import forms
from django.contrib.auth.forms import UserCreationForm
from doghelp.models import Case, Video


class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class NewUserForm(UserCreationForm):
    email = forms.EmailField()
    is_specialist = forms.BooleanField(label='Sign up as specialist', required=False)


class AddVideosForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['name', 'videofile', 'author']
        widgets = {'author': forms.HiddenInput()}


# class NewCaseForm(forms.ModelForm):
#     class Meta:
#         model = Case
#         exclude = ['creation_date', 'last_modified', 'status', 'author', 'pet_specialist']
