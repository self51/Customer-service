from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import User


class CustomerSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
        )
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'username': 'Username',
        }

    def save(self, commit: bool = True) -> User:
        user: User = super().save(commit=False)
        user.is_customer = True
        if commit:
            user.save()
        return user


class WorkerSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'provide_service',
        )
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'username': 'Username',
            'provide_service': 'Provide service',
        }

    def save(self, commit: bool = True) -> User:
        user: User = super().save(commit=False)
        user.is_worker = True
        if commit:
            user.save()
        return user


class WorkerUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'provide_service',
        )


class CustomerUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
        )
