# urls.py
from django.urls import path
from . import views


app_name="Home"
# urls.py
urlpatterns = [
    path("", views.Home, name="home"),

    # confirmation + reservation system
    path("reserve/confirm/<int:id>/", views.ReserveConfirmView.as_view(), name="reserve_confirm"),
    path("reserve/<int:id>/", views.ReserveNobatView.as_view(), name="reserve_nobat"),

    # user's appointments
    path("my-appointments/", views.MyAppointmentsView.as_view(), name="my_appointments"),
    path("cancel/<int:id>/", views.CancelAppointmentView.as_view(), name="cancel_nobat"),
]
