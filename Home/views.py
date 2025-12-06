from datetime import timezone

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, TemplateView
from django.contrib import messages

from Home.models import Nobat
from Home.utils.turn_maker import create_reservations
from khayyam import JalaliDate

# Create your views here.
def Home(request):
    create_reservations()

    today_jalali = JalaliDate.today()
    today = today_jalali.todate()
    objects = (
        Nobat.objects.select_related("day")
        .filter(user__isnull=True, day__date__gte=today)   # auto-hide taken AND hide past
        .order_by("day__date", "time")
    )

    return render(request, "Home/index.html", {"objects": objects, "today": today})


class MyAppointmentsView(LoginRequiredMixin, View):
    login_url = reverse_lazy("account:login")

    def get(self, request):
        my_nobats = Nobat.objects.filter(user=request.user).order_by("day__date", "time")
        return render(request, "Home/my_appointments.html", {"my_nobats": my_nobats})

class CancelAppointmentView(LoginRequiredMixin, View):
    login_url = reverse_lazy("account:login")

    def post(self, request, id):
        nobat = get_object_or_404(Nobat, id=id, user=request.user)

        nobat.user = None
        nobat.save()

        messages.success(request, "Your appointment has been canceled.")
        return redirect("Home:my_appointments")


class ReserveNobatView(LoginRequiredMixin, View):
    login_url = reverse_lazy("account:login")

    def get(self, request, id):
        nobat = get_object_or_404(Nobat, id=id)

        # Prevent multiple reservations (limit 1 total)
        if Nobat.objects.filter(user=request.user).exists():
            messages.error(request, "You already have an active appointment. You cannot reserve a new one.")
            return redirect("Home:home")

        # Extra check: prevent double booking the same slot
        if nobat.user is not None:
            messages.error(request, "This appointment is already taken.")
            return redirect("Home:home")

        return render(request, "Home/confirm.html", {"nobat": nobat})

    def post(self, request, id):
        nobat = get_object_or_404(Nobat, id=id)

        if Nobat.objects.filter(user=request.user).exists():
            messages.error(request, "You already have an active appointment.")
            return redirect("Home:home")

        if nobat.user is not None:
            messages.error(request, "This appointment is already taken.")
            return redirect("Home:home")

        nobat.user = request.user
        nobat.save()
        messages.success(request, "Your appointment has been successfully reserved.")
        return redirect("Home:my_appointments")


class ReserveConfirmView(LoginRequiredMixin, View):
    login_url = reverse_lazy("account:login")

    def get(self, request, id):
        nobat = get_object_or_404(Nobat, id=id)
        return render(request, "Home/confirm.html", {"nobat": nobat})