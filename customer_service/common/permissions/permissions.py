from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.core.exceptions import PermissionDenied

if TYPE_CHECKING:
    from django.http import HttpRequest


class IsObjectOwner:
    """Ensure that user is the owner of the object."""

    @staticmethod
    def has_object_permission(request: HttpRequest, obj: Any) -> None:
        if obj.user != request.user:
            msg = 'You do not have permission to access this item.'
            raise PermissionDenied(msg)

    @staticmethod
    def ensure_customer_or_worker_access(request: HttpRequest, obj: Any) -> None:
        user = request.user
        if user not in {obj.customer, obj.worker}:
            msg = 'You do not have permission to access this item.'
            raise PermissionDenied(msg)
