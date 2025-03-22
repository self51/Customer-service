from common.custom_types.custom_types import WorkerID
from common.pydantic_models.location import LocationData
from common.pydantic_models.user import CustomerCredentialsModel
from pydantic import BaseModel


class AppointmentInputData(BaseModel):
    worker_id: WorkerID
    location_data: LocationData
    date_time: str
    customer_credentials: CustomerCredentialsModel
