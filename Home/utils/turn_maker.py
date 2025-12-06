from django.utils import timezone
from Home.models import ReservationDay, Nobat
import datetime
from khayyam import JalaliDate


def create_reservations(interval_minutes=30):
    today = timezone.now().date()

    for day_offset in range(6):
        reservation_date = today + datetime.timedelta(days=day_offset)

        jalali_date = JalaliDate(reservation_date)

        if jalali_date.weekday() in [5, 6]:
            continue

        reservation_day, created = ReservationDay.objects.get_or_create(date=reservation_date)

        morning_times = []
        evening_times = []

        start_time = datetime.time(9, 0)
        end_time = datetime.time(13, 0)
        while start_time < end_time:
            morning_times.append(start_time)
            start_time = (datetime.datetime.combine(datetime.date.today(), start_time) + datetime.timedelta(
                minutes=interval_minutes)).time()

        current_time = datetime.time(17, 0)
        end_time = datetime.time(22, 0)
        while current_time < end_time:
            evening_times.append(current_time)
            current_time = (datetime.datetime.combine(datetime.date.today(), current_time) + datetime.timedelta(
                minutes=interval_minutes)).time()

        turn_times = morning_times + evening_times

        for turn_time in turn_times:
            if not Nobat.objects.filter(day=reservation_day, time=turn_time).exists():
                Nobat.objects.create(day=reservation_day, time=turn_time)
