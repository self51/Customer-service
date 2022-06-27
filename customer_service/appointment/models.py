from django.db import models

from authentication.models import User
from worker.models import Location, Schedule


class Appointment(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    time = models.TimeField()
    status = models.BooleanField(default=False)