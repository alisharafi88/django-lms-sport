from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    phone_number = PhoneNumberField(_('Phone number'), region='IR',)
