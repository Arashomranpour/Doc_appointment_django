from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.transaction import commit
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView

from .forms import LoginForm, RegisterForm, checkotpform, otploginform, Contactusform
from .models import otp, messagecontactus
from django.contrib.auth import authenticate,login,logout
from .models import MyUser
from django.contrib.auth import authenticate, login


from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.utils.crypto import get_random_string
from django.views import View
# Create your views here.
from uuid import uuid4
from random import randint
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SetPasswordForm
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import ProfileUpdateForm



class UserLoginView(View):

    def get(self, request):
        # Already logged in → redirect
        if request.user.is_authenticated:
            return redirect('Home:home')

        form = LoginForm()
        return render(request, "account/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            # username field can contain phone OR email
            username = cd["phone"]
            password = cd["password"]

            # authenticate using our custom backend
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                next_page=request.GET.get("next")
                if next_page:
                    return redirect(next_page)
                return redirect('Home:home')
            else:
                form.add_error("username", "Invalid email/phone or password.")
        else:
            form.add_error(None, "Invalid form data.")

        return render(request, "account/login.html", {"form": form})

@login_required(login_url='/account/login')
def UserLogoutView(request):
    logout(request)
    # print(f"{request.user} is now logged out")
    return redirect("Home:home")
class UserSignUpView(View):

    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('Home:home')
        form = RegisterForm()
        return render(request, "account/otplogin.html", {"form": form})

    def post(self, request):
        if self.request.user.is_authenticated:
            return redirect('Home:home')
        form = RegisterForm(request.POST)

        # not logged in so have to login
        if form.is_valid():

            cd = form.cleaned_data
            if MyUser.objects.filter(phone=form.cleaned_data['phone']).exists():
                # form.add_error("phone", "Phone Number already taken.")
                return redirect(reverse('account:login') + "?already_exists=1")
            randcode=randint(1000,9999)
            # sms.verification({"receptor": cd["phone"], "type": "1", "template": "Ghasedak", "param1": randcode,'%Code%': randcode,"%param1%":randcode})
            token=str(uuid4())
            otp.objects.create(phone=cd["phone"], code=randcode,token=token)
            print(randcode)
            return redirect(reverse("account:checkotp")+f"?token={token}")

        else:
            form.add_error('password', "form is not valid , please try again later")
        return render(request, "account/otplogin.html", {"form": form})


class Checkotpview(View):
    def get(self, request):
        form = checkotpform(request.POST)
        return render(request, "account/checkotp.html", {"form": form})

    def post(self, request):
        if self.request.user.is_authenticated:
            return redirect('Home:home')
        token=request.GET.get("token")
        form = checkotpform(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if otp.objects.filter(token=token,code=cd["code"]).exists():
                otsp=otp.objects.get(token=token)
                user,is_created=MyUser.objects.get_or_create(phone=otsp.phone)
                user.backend='django.contrib.auth.backends.ModelBackend'
                otsp.delete()
                login(request,user)

                return redirect("account:set_password")
        else:
            form.add_error('password', "form is not valid , please try again later")
        return render(request, "account/checkotp.html", {"form": form})



class OtploginView(View):

    def get(self, request):
        # if self.request.user.is_authenticated:
        #     return redirect('home:home')
        form =otploginform()
        return render(request, "account/otplogin.html", {"form": form})

    def post(self, request):
        # if self.request.user.is_authenticated:
        #     return redirect('home:home')
        form =  otploginform(request.POST)

        # not logged in so have to login
        if form.is_valid():
            cd = form.cleaned_data
            randcode=randint(1000,9999)
            # sms.verification({"receptor": cd["phone"], "type": "1", "template": "Ghasedak", "param1": randcode,'%Code%': randcode,"%param1%":randcode})
            token=str(uuid4())
            otp.objects.create(phone=cd["phone"], code=randcode,token=token)
            print(randcode)
            return redirect(reverse("account:checkotp")+f"?token={token}")

        else:
            form.add_error('password', "form is not valid , please try again later")
        return render(request, "account/otplogin.html", {"form": form})




class SetPasswordView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("account:login")
        form = SetPasswordForm(initial={'email': request.user.email})
        return render(request, "account/set_password.html", {"form": form})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect("account:login")

        form = SetPasswordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = request.user

            # Set password
            user.set_password(cd["password1"])

            # Set email
            user.email = cd["email"]

            user.save()

            # Login user with proper backend
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            # Pass success for toast
            return render(request, "account/set_password.html", {"form": form, "success": True})

        return render(request, "account/set_password.html", {"form": form})




@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(View):
    def get(self, request):
        # prefill email if exists
        form = ProfileUpdateForm(initial={'email': request.user.email})
        return render(request, "account/profile_update.html", {"form": form})

    def post(self, request):
        form = ProfileUpdateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = request.user

            # Update email if provided
            if cd.get("email"):
                user.email = cd["email"]

            # Update password if provided
            if cd.get("password1"):
                user.set_password(cd["password1"])
                user.save()

                # Re-login user with backend set to fix multiple backends issue
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
            else:
                user.save()

            return render(request, "../Home/templates/Home/index.html", {"form": form, "success": True})


        return render(request, "account/profile_update.html", {"form": form})

@method_decorator(login_required, name='dispatch')
class DeleteProfileView(View):
    def get(self, request):
        # Render confirmation page
        return render(request, "account/profile_delete_confirm.html")

    def post(self, request):
        user = request.user
        logout(request)  # log out the user first
        user.delete()    # delete the user account
        return redirect("Home:home")  # redirect to home page

class ContactusView(LoginRequiredMixin,CreateView):
    template_name = "account/contactus.html"
    form_class = Contactusform
    success_url = "/"
    login_url = "accounts/login"
    # fields = ("subject", "message")
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.email = self.request.user.email
        instance.save()
        return  super().form_valid(form)
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["message"]=messagecontactus.objects.all()
        return context

class MessageListView(ListView):
    model = messagecontactus
    template_name = "account/messagelist.html"
    context_object_name = "message_list"
    def get_queryset(self):
        user=self.request.user
        if user.is_authenticated:
            return messagecontactus.objects.filter(email=user.email)
        else :
            return messagecontactus.objects.none()

class MessageDelete(DeleteView,LoginRequiredMixin):
    model=messagecontactus
    login_url = "accounts/login"

    success_url = reverse_lazy("Home:home")
    template_name = "account/deletemessage.html"