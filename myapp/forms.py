from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=_("email"),
        max_length=254,
        help_text='\n',
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    username = forms.CharField(
        label=_("username"),
        max_length=54,
        help_text='\n',
        widget=forms.TextInput(attrs={'autocomplete': 'username'})
    )

    password1 = forms.CharField(
        label=_("password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text='\n',
    )
    password2 = forms.CharField(
        label=_("confirm password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("\n"),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'accept': 'application/pdf'}))

