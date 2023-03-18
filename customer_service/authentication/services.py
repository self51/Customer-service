from datetime import date, time, timedelta

from appointment.models import Appointment
from worker.models import Schedule


class ScheduleGenerate:

    def __init__(self, worker_id):
        self.worker_id = worker_id
        self.schedules = Schedule.objects.filter(worker=worker_id)
        self.appointments = Appointment.objects.filter(worker=worker_id)

    @staticmethod
    def hour_list_generator(from_hour, to_hour, booked_hours):
        while from_hour <= to_hour:
            if from_hour.strftime('%H:%M') not in booked_hours:
                yield from_hour.strftime('%H:%M')
            from_hour = time(from_hour.hour + 1, from_hour.minute)

    def get_hour_list(self, current_day):
        weekday_number = current_day.weekday()
        current_day_appointments = self.appointments.filter(date=str(current_day))

        try:
            schedules = self.schedules.filter(weekday=weekday_number)
        except Schedule.DoesNotExist:
            return None

        finally_hour_list = []
        for schedule in schedules:
            from_hour = schedule.from_hour
            to_hour = schedule.to_hour

            # extract time from appointment and converts it into the required format
            booked_hours = [appointment.time.strftime('%H:%M') for appointment in current_day_appointments]

            # generates list without booked hours
            hour_list = [hour for hour in self.hour_list_generator(from_hour, to_hour, booked_hours)]
            finally_hour_list = finally_hour_list + hour_list

        return finally_hour_list

    def get_day_list(self):
        today = date.today()

        day_list = []
        for next_day in range(7):
            current_day = today + timedelta(days=next_day)
            weekday = current_day.strftime("%A").upper()
            day = {
                "date": str(current_day),
                "weekday": weekday,
                "hour_list": self.get_hour_list(current_day)
            }
            day_list.append(day)

        return day_list
