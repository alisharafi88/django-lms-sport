from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from phonenumbers import parse, is_valid_number, NumberParseException, region_code_for_number
from phonenumber_field.modelfields import PhoneNumberField

from apps.courses.models import Course


def phone_number_validator_for_iran(value):
    try:
        phone_number = parse(value, 'IR')
        if not is_valid_number(phone_number):
            raise ValidationError(_('Invalid phone number.'))
        if region_code_for_number(phone_number) != 'IR':
            raise ValidationError(_('Phone number must be from Iran.'))
    except NumberParseException:
        raise ValidationError(_('Invalid phone number format.'))


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

    def __str__(self):
        return f'{self.total_price}'

    class Meta:
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
        unique=True
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
        return _(f'{self.order} - DVD Details')

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
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name=_('Course')
    )
    unit_price = models.PositiveIntegerField(_('UnitPrice'), default=0)

    class Meta:
        unique_together = ('order', 'course')

        verbose_name = _('Order\'s Item')
        verbose_name_plural = _('Order\'s Items')

    def __str__(self):
        return f'{self.order} - {self.course}'
