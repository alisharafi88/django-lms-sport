from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field


class ContactInfo(models.Model):
    phonenumber = models.CharField(_('Phone number'), max_length=11)
    email = models.EmailField(_('Email address'), blank=True, null=True)
    address = CKEditor5Field(_('Address'), max_length=255, blank=True, null=True)

    telegram_id = models.CharField(_('telegram id'), max_length=50, blank=True, null=True, help_text=_('Enter your Telegram ID.'))
    youtube_id = models.CharField(_('youtube id'), max_length=50, blank=True, null=True, help_text=_('Enter your YouTube ID.'))
    instagram_id = models.CharField(_('instagram id'), max_length=50, blank=True, null=True, help_text=_('Enter your Instagram ID.'))

    is_primary = models.BooleanField(_('Is primary'), help_text=_('you can only have 1 primary contact'))

    class Meta:
        verbose_name = _('Contact Information')
        verbose_name_plural = _('Contact Information')


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

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
