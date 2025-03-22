from pydantic import BaseModel

from common.custom_types.custom_types import LocationID


class LocationData(BaseModel):
    location_id: LocationID
    address: str
