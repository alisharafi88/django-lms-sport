from django.contrib.auth.backends import ModelBackend

from .models import CustomUser


class PhoneAuthenticationBackend(ModelBackend):
    @staticmethod
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
            return user

        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def get_user(self, user_id):
        try:
            user = CustomUser.objects.get(pk=user_id)
            return user
        except CustomUser.DoesNotExist:
            return None
