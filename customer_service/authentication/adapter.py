from __future__ import annotations

from typing import TYPE_CHECKING

from allauth.account.adapter import DefaultAccountAdapter

if TYPE_CHECKING:
    from django.contrib.auth.forms import UserCreationForm
    from django.http import HttpRequest

    from authentication.models import User


class AccountAdapter(DefaultAccountAdapter):
    def save_user(
        self,
        request: HttpRequest,
        user: User,
        form: UserCreationForm,
        commit: bool = True,
    ) -> User:
        if request.session['user_type'] == 'is_customer':
            user.is_customer = True
        elif request.session['user_type'] == 'is_worker':
            user.is_worker = True
        updated_user: User = super().save_user(request, user, form, commit)
        return updated_user
