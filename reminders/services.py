from datetime import date, time
from .models import Reminder
from datetime import time, date
from reminders.models import Reminder

TIME_MAP = {1: [time(9, 0)], 2: [time(9, 0), time(21, 0)], 3: [time(8, 0), time(14, 0), time(20, 0)]}


def generate_today_reminders(user):
    today = date.today()
    for med in user.medicines.all():
        for t in TIME_MAP.get(med.frequency_per_day, [time(9, 0)]):
            Reminder.objects.get_or_create(user=user, medicine=med, date=today, time=t)



def create_reminders(medicine):
    times = []

    if medicine.frequency_per_day == 1:
        times = [time(9, 0)]
    elif medicine.frequency_per_day == 2:
        times = [time(9, 0), time(21, 0)]
    elif medicine.frequency_per_day == 3:
        times = [time(9, 0), time(14, 0), time(21, 0)]

    for t in times:
        Reminder.objects.create(
            user=medicine.user,
            medicine=medicine,
            time=t,
            date=date.today()
        )