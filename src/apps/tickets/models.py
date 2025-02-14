from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Ticket(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'p', _('Pending')
        RESOLVED = 'r', _('Resolved')
        CLOSED = 'c', _('Closed')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets',
        verbose_name=_('User')
    )

    subject = models.CharField(
        _('Subject'),
        max_length=255,
    )

    message = models.TextField(
        _('Message')
    )

    status = models.CharField(
        _('Status'),
        max_length=1,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
    )

    date_created = models.DateTimeField(
        _('Date Created'),
        auto_now_add=True,
    )

    date_updated = models.DateTimeField(
        _('Date Updated'),
        auto_now=True,
    )

    def __str__(self):
        return f"{self.subject} - {self.get_status_display()}"

    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')
        ordering = ('date_updated', '-date_created')

        indexes = [
            models.Index(fields=['date_updated', 'date_created'], name='date_idx'),
            models.Index(fields=['user'], name='user_idx'),
        ]


class TicketReply(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name=_('Ticket')
    )

    message = models.TextField(
        _('Message'),
    )

    date_created = models.DateTimeField(
        _('Date Created'),
        auto_now_add=True,
    )

    def __str__(self):
        return f"Reply for Ticket ({self.ticket.get_status_display()}) on {self.ticket.subject}"

    class Meta:
        verbose_name = _('Reply')
        verbose_name_plural = _('Replies')
        ordering = ('date_created',)
        indexes = [
            models.Index(fields=['ticket'], name='replies_ticket_idx'),
            models.Index(fields=['date_created'], name='replies_date_idx'),
        ]