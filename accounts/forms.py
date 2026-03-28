from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

UserModel = get_user_model()


class AppUserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

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
