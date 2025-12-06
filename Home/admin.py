from django.contrib import admin
from . import models
# Register your models here.
# admin.site.register(models.Nobat)
# admin.site.register(models.ReservationDay)

class InlineResevation(admin.StackedInline):
    model=models.Nobat

@admin.register(models.ReservationDay)
class ReservationDayAdmin(admin.ModelAdmin):
    list_display = ("date",)
    inlines = (InlineResevation,)