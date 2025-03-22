from common.custom_types.custom_types import CustomerID, LocationID, WorkerID
from pydantic import BaseModel


class AppointmentDataType(BaseModel):
    worker_id: WorkerID
    customer_id: CustomerID
    location_id: LocationID
    date: str
    time: str
