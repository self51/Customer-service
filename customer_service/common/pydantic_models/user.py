from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from common.custom_types.custom_types import UserID


class CustomerCredentialsModel(BaseModel):
    user_id: UserID = Field(alias='id')
    google_calendar_credentials: dict[str, Any] | None = None

    model_config = ConfigDict(from_attributes=True)
