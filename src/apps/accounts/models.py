from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static

from phonenumbers import parse, is_valid_number, NumberParseException, region_code_for_number
from phonenumber_field.modelfields import PhoneNumberField


def phone_number_validator_for_iran(value):
    try:
        phone_number = parse(value, 'IR')
        if not is_valid_number(phone_number):
            raise ValidationError(_('Invalid phone number.'))
        if region_code_for_number(phone_number) != 'IR':
            raise ValidationError(_('Phone number must be from Iran.'))
    except NumberParseException:
        raise ValidationError(_('Invalid phone number format.'))


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError(_('The Phone Number must be set'))

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(phone_number, password, **extra_fields)


def upload_user_profle_photo_path(instance, filename):
    return f'user/profile-photo/{instance.phone_number}/{filename}'


class CustomUser(AbstractUser):
    phone_number = PhoneNumberField(_('Phonenumber'), region='IR', validators=[phone_number_validator_for_iran], unique=True,)
    username = None

    profile_photo = models.ImageField(_('Profile Photo'), upload_to=upload_user_profle_photo_path, blank=True, null=True)

    bio = models.TextField(_('Bio'), blank=True, null=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.phone_number)

    @property
    def get_photo_url(self):
        if self.profile_photo and self.profile_photo.url:
            return self.profile_photo.url

        return static('assets/img/avatar/default-avatar-icon.jpg')

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between if it exists.
        """
        if self.first_name or self.last_name:
            full_name = "%s %s" % (self.first_name, self.last_name)
            return full_name.strip()
        return _('Anonymous')

    @property
    def get_name(self):
        if self.first_name or self.last_name:
            return self.get_full_name()
        return self.phone_number


