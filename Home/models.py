from django.db import models
from account.models import MyUser# Create your models here.


# model roz k faghat tarikh migire
class ReservationDay(models.Model):
    date=models.DateField(verbose_name="Date")
    class Meta:
        verbose_name=("Reservation Days",)
        ordering=("-date",)
    def __str__(self):
        return str(self.date)


class Nobat(models.Model):
    day=models.ForeignKey(ReservationDay,on_delete=models.CASCADE,verbose_name="Day",related_name="reservations")
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE,blank=True,null=True,verbose_name="User")
    time=models.TimeField()
    class Meta:
        verbose_name=("Reservation List",)
        ordering = ("day__date", "time")
    def __str__(self):
        return f"{self.day.date} - {self.time}"


