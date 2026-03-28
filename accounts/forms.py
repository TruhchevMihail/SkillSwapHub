from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

UserModel = get_user_model()


class AppUserCreateForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Email address',
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
    )

    class Meta:
        model = UserModel
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'profile_picture',
            'password1',
            'password2',
        )
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'profile_picture': 'Profile picture',
        }
        help_texts = {
            'username': 'Use letters, numbers and @/./+/-/_ only.',
            'profile_picture': 'Optional. Upload a clear profile photo.',
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Choose a username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'John'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Doe'}),
        }
