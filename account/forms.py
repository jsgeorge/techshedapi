from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
# creating a form


class RegForm(UserCreationForm):

    # create metaclass
    class Meta:
        # specify model to be used
        model = User

        # specify field to be used
        fields = [
            "first_name", "last_name", "username", "email", "password1",
            "password2"
        ]


class LoginForm(AuthenticationForm):

    # create metaclass
    class Meta:
        # specify model to be used
        model = User

        # specify field to be used
        fields = ["username", "password"]
