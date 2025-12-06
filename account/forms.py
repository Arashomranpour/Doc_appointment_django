from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from .models import MyUser, messagecontactus
from django import forms
from django.core.exceptions import ValidationError

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = MyUser
        fields = ["phone"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = [ "phone", "password", "is_active", "is_admin"]

class LoginForm(forms.Form):
    phone=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder": "Phone Number / Email"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder": "Password"}))

class otploginform(forms.Form):
        phone = forms.CharField(
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your Phone"}),validators=[validators.MaxLengthValidator(12)])

class RegisterForm(forms.Form):

    phone=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Your Phone"}),validators=[validators.MaxLengthValidator(12)])

class checkotpform(forms.Form):
    code=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Your Code "}),validators=[validators.MaxLengthValidator(4)])

class SetPasswordForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter your email"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "New Password"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Repeat Password"}
        )
    )

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")

        if p1 != p2:
            raise ValidationError("Passwords do not match.")

        return cleaned

class ProfileUpdateForm(forms.Form):
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"})
    )
    password1 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "New Password"})
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Repeat Password"})
    )

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")

        # Only validate password if user entered a new password
        if p1 or p2:
            if p1 != p2:
                raise ValidationError("Passwords do not match.")
        return cleaned
class Contactusform(forms.ModelForm):
    class Meta:
        model = messagecontactus
        fields = ("subject","message")

        widgets={
            "subject":forms.TextInput(attrs={'class':'form-control','placeholder':'Subject of your message'}),
        }