from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from phonenumbers import parse, is_valid_number, NumberParseException, region_code_for_number
from phonenumber_field.modelfields import PhoneNumberField

from apps.courses.models import Course
from apps.utils.numbers.convert_numbers import PersianNumberConverter


def phone_number_validator_for_iran(value):
    try:
        phone_number = parse(value, 'IR')
        if not is_valid_number(phone_number):
            raise ValidationError(_('Invalid phone number.'))
        if region_code_for_number(phone_number) != 'IR':
            raise ValidationError(_('Phone number must be from Iran.'))
    except NumberParseException:
        raise ValidationError(_('Invalid phone number format.'))


class ShippingSettings(models.Model):
    dvd_shipping_price = models.PositiveIntegerField(_('DVD Shipping Price'), default=0)

    date_created = models.DateTimeField(_('Date Created'), auto_now_add=True)
    date_updated = models.DateTimeField(_('Date Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Shipping Settings')
        verbose_name_plural = _('Shipping Settings')
        ordering = ('-date_updated',)

    def save(self, *args, **kwargs):
        self.id = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PAID = 'p', _('Paid')
        UNPAID = 'u', _('Unpaid')
        CANCELED = 'c', _('Canceled')

    class AccessStatus(models.TextChoices):
        ONLINE = 'o', _('Online')
        DVD = 'd', _('DVD')

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name=_('Customer')
    )
    status = models.CharField(
        _('Status'),
        max_length=1,
        choices=OrderStatus.choices,
        default=OrderStatus.UNPAID
    )
    access_status = models.CharField(
        _('AccessStatus'),
        max_length=1,
        choices=AccessStatus.choices,
        default=AccessStatus.ONLINE
    )
    total_price = models.PositiveIntegerField(_('TotalPrice'), default=0)

    date_created = models.DateTimeField(_('DateCreated'), auto_now_add=True)

    coupon_code = models.CharField(_('Coupon Code'), max_length=50, null=True, blank=True)
    zarinpal_authority = models.CharField(_('Payment Authority'), max_length=255, null=True, blank=True)
    zarinpal_ref_id = models.CharField(max_length=150, null=True, blank=True)
    zarinpal_data = models.TextField(null=True, blank=True)

    dvd_shipping_price = models.PositiveIntegerField(_('DVD Shipping Price'), default=0)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ('-date_created',)

        indexes = [
            models.Index(fields=['status', 'zarinpal_authority'], name='status_zarinpal_authority_idx'),
            models.Index(fields=['date_created'], name='date_created_idx'),
        ]

        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class DVDOrderDetail(models.Model):
    class DeliveryStatus(models.TextChoices):
        PENDING = 'p', _('Pending')
        SENT = 's', _('Sent')
        REJECTED = 'r', _('Rejected')
        CANCELED = 'c', _('Canceled')

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='dvd_detail',
        verbose_name=_('Order'),
    )

    city = models.CharField(_('City'), max_length=15)
    address = models.CharField(_('Address'), max_length=255)
    postal_code = models.CharField(_('PostalCode'), max_length=20)
    first_name = models.CharField(_('firstName'), max_length=20)
    last_name = models.CharField(_('LastName'), max_length=30)
    email = models.EmailField(_('Email'))
    phone_number = PhoneNumberField(
        _('Phonenumber'),
        region='IR',
        validators=[phone_number_validator_for_iran],
    )
    order_note = models.CharField(_('Order\'sNote'), max_length=255, null=True, blank=True)

    delivery_status = models.CharField(
        _('DeliveryStatus'),
        max_length=1,
        choices=DeliveryStatus.choices,
        default=DeliveryStatus.PENDING,
    )

    date_created = models.DateTimeField(_('Created Date'), auto_now_add=True)

    def __str__(self):
        return str(_(f'{self.order} - DVD Details'))

    def save(self, *args, **kwargs):
        super().save()
        self.order.access_status = self.order.AccessStatus.DVD

    class Meta:
        verbose_name = _('DVD\'s Order')
        verbose_name_plural = _('DVD\'s Orders')


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        related_name='items',
        verbose_name=_('Order'),
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={'model__in': ('course', 'package')},
        verbose_name=_('Content Type'),
        null=True,
        blank=True,
    )
    object_id = models.PositiveIntegerField(verbose_name=_('Object ID'), null=True, blank=True)
    product = GenericForeignKey('content_type', 'object_id')
    unit_price = models.PositiveIntegerField(_('Unit Price'), default=0)

    class Meta:
        unique_together = ('order', 'content_type', 'object_id')

        verbose_name = _('Order\'s Item')
        verbose_name_plural = _('Order\'s Items')

    def __str__(self):
        return f'{self.order} - {self.product}'
