from datetime import date, time, timedelta


def hour_list_generate(schedule):
    from_hour = schedule.from_hour
    to_hour = schedule.to_hour

    hour_list = []
    while from_hour <= to_hour:
        hour_list.append(from_hour.strftime('%H:%M'))
        from_hour = time(from_hour.hour + 1, from_hour.minute)

    return hour_list


def day_list_generate(schedules):
    today = date.today()

    day_list = []
    for next_day in range(7):
        day = {}
        current_day = today + timedelta(days=next_day)
        weekday = current_day.strftime("%A").upper()
        weekday_number = current_day.weekday()
        schedule = schedules.get(weekday=weekday_number)
        day["date"] = str(current_day)
        day["weekday"] = weekday
        day["hour_list"] = hour_list_generate(schedule)
        day_list.append(day)

    return day_list
