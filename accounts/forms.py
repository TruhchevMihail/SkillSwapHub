from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

UserModel = get_user_model()


ROLE_MENTOR = 'Mentors'
ROLE_LEARNER = 'Learners'
ROLE_CHOICES = (
    (ROLE_LEARNER, 'Learner - I want to book sessions'),
    (ROLE_MENTOR, 'Mentor - I want to create offers'),
)


class AppUserCreateForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Email address',
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        initial=ROLE_LEARNER,
        label='Account type',
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_picture'].required = False

    class Meta:
        model = UserModel
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
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


class AppUserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = (
            'first_name',
            'last_name',
            'email',
            'profile_picture',
        )
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'Email address',
            'profile_picture': 'Profile picture',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'John'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Doe'}),
            'email': forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_picture'].required = False

