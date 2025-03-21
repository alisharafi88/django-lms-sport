from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin

from apps.tickets.models import TicketReply, Ticket


class TicketReplyInline(StackedInlineJalaliMixin, admin.StackedInline):
    model = TicketReply
    extra = 1
    readonly_fields = ('date_created',)
    fields = ('message', 'date_created')
    verbose_name = _('Reply')
    verbose_name_plural = _('Replies')


@admin.register(Ticket)
class TicketAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('subject', 'status', 'user', 'date_created')
    list_filter = ('status', 'date_created',)
    search_fields = ('subject', 'message')
    list_editable = ('status',)
    inlines = [TicketReplyInline]
    ordering = ('-date_created',)

    actions = ['mark_as_resolved', 'mark_as_closed']

    @admin.action(description=_('Mark selected tickets as Resolved'))
    def mark_as_resolved(self, request, queryset):
        update_count = queryset.update(status=Ticket.StatusChoices.RESOLVED)
        self.message_user(
            request,
            _(f'{update_count} of tickets status has been updated to pending.'),
            messages.SUCCESS
        )

    @admin.action(description=_('Mark selected tickets as Closed'))
    def mark_as_closed(self, request, queryset):
        update_count = queryset.update(status=Ticket.StatusChoices.CLOSED)
        self.message_user(
            request,
            _(f'{update_count} of tickets status has been updated to closed.'),
            messages.SUCCESS
        )


@admin.register(TicketReply)
class TicketReplyAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('ticket', 'date_created')
    list_filter = ('date_created',)
    search_fields = ('message',)
    readonly_fields = ('date_created',)
