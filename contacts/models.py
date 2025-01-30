from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _
from django_ckeditor_5.fields import CKEditor5Field


class ContactInfo(models.Model):
    phonenumber = models.CharField(_('Phone number'), max_length=11,)
    email = models.EmailField(_('Email address'), blank=True, null=True,)
    adress = CKEditor5Field(_('Adress'), max_length=255, blank=True, null=True,)

    is_primary = models.BooleanField(_('Is primary'), help_text=_('you can only have 1 primary contact'))


class Message(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='messages',
        verbose_name=_('User')
    )
    text = models.TextField(_('Message'),)

    date_sent = models.DateTimeField(auto_now_add=True, verbose_name=_('Date sent'))
