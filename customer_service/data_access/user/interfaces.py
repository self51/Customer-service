from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from common.custom_types.custom_types import WorkerID


class BaseUserReaderService(ABC):
    @abstractmethod
    def get_worker_name(self, worker_id: WorkerID) -> str | None:
        """Retrieves worker name for a given worker ID."""
