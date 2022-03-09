from django import forms
from django.contrib.auth.forms import UserCreationForm
from doghelp.models import Case, Video
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class NewUserForm(UserCreationForm):
    email = forms.EmailField()
    is_specialist = forms.BooleanField(label='Sign up as a specialist', required=False)


class AddVideosForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['name', 'videofile', 'author']
        widgets = {'author': forms.HiddenInput()}


class NewCaseForm(forms.ModelForm):
    pet_name = forms.CharField(help_text='Type letters only.')

    class Meta:
        model = Case
        fields = ['title', 'pet_name', 'description', 'is_public', 'author', 'status', 'video']
        widgets = {
            'author': forms.HiddenInput(),
            'status': forms.HiddenInput()
        }

    def __init__(self, user, *args, **kwargs):
        super(NewCaseForm, self).__init__(*args, **kwargs)
        self.fields['video'].queryset = Video.objects.filter(author_id=user)

    def clean(self):
        cleaned_data = super().clean()
        pet_name = cleaned_data.get('pet_name')
        if isinstance(pet_name, str) and not pet_name.isalpha():
            raise ValidationError('Only letters are allowed in the "Pet name" field.')
        else:
            return cleaned_data
