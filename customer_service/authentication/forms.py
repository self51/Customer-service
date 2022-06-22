from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomerSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'username': 'Username',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(CustomerSignUpForm, self).__init__(*args, **kwargs)

class WorkerSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'provide_service')
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'username': 'Username',
            'provide_service': 'Provide service',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_worker = True
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(WorkerSignUpForm, self).__init__(*args, **kwargs)