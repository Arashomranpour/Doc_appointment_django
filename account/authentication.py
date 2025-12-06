from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class PhoneEmailAuthBackend(ModelBackend):
    """
    Allow authentication using phone OR email.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None

        # Try phone (USERNAME_FIELD)
        try:
            user = User.objects.get(phone=username)
        except User.DoesNotExist:
            pass

        # Try email
        if user is None:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None

        # Check password
        if user.check_password(password):
            return user

        return None
