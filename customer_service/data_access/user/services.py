from __future__ import annotations

from typing import TYPE_CHECKING

from data_access.user.interfaces import BaseUserReaderService

if TYPE_CHECKING:
    from authentication.models import User
    from common.custom_types.custom_types import WorkerID


class UserReaderService(BaseUserReaderService):
    __slots__ = ('user_model',)

    def __init__(self, user_model: type[User]) -> None:
        self.user_model = user_model

    def get_worker_name(self, worker_id: WorkerID) -> str | None:
        user = (
            self.user_model.objects.filter(id=worker_id)
            .only('first_name', 'last_name')
            .first()
        )
        return f'{user.first_name} {user.last_name}' if user else None
