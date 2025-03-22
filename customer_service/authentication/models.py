from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING, Any

from allauth.account.utils import get_next_redirect_url
from allauth.socialaccount.adapter import get_adapter
from allauth.utils import get_request_param
from django.contrib.auth.models import AbstractUser
from django.db import models

if TYPE_CHECKING:
    from django.http import HttpRequest


def state_from_request(request: HttpRequest) -> dict[str, Any]:
    state = {}
    next_url = get_next_redirect_url(request)
    with contextlib.suppress(KeyError):
        request.session['user_type'] = get_request_param(request, 'user', None)

    if next_url:
        state['next'] = next_url
    state['process'] = get_request_param(request, 'process', 'login')
    state['scope'] = get_request_param(request, 'scope', '')
    state['auth_params'] = get_request_param(request, 'auth_params', '')
    return state


get_adapter().state_from_request = state_from_request


class User(AbstractUser):
    is_customer = models.BooleanField('customer status', default=False)
    is_worker = models.BooleanField('worker status', default=False)
    provide_service = models.CharField(max_length=35, blank=False)
    google_calendar_credentials = models.JSONField(blank=True, null=True)
