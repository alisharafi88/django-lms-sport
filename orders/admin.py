from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'date_created', 'access_status', 'status',)
    list_filter = ('access_status', 'status',)
    search_fields = ('customer', 'date_created',)
    date_hierarchy = 'date_created'
    list_per_page = 20
    ordering = ('-date_created',)
    readonly_fields = ('date_created',)
    list_editable = ('status', 'access_status',)
    actions = ('status_paid', 'status_canceled', 'status_unpaid')

    fieldsets = (
        (_('custome information'), {'fields': ('customer',)}),
        (_('status'), {'fields': ('status', 'access_status',)}),
        (_('date'), {'fields': ('date_created',)}),
    )

    add_fieldsets = (
        (_('custome information'), {'fields': ('customer',)}),
        (_('status'), {'fields': ('status', 'access_status',)}),
    )

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return self.add_fieldsets
        return self.fieldsets

    @admin.action(description=_('Update status to paid'))
    def status_paid(self, request, queryset):
        update_count = queryset.update(status=Order.OrderStatus.PAID)
        self.message_user(
            request,
            _(f'{update_count} of orders status has been updated to paid.'),
            messages.WARNING
        )

    @admin.action(description=_('Update status to canceled'))
    def status_canceled(self, request, queryset):
        update_count = queryset.update(status=Order.OrderStatus.CANCELED)
        self.message_user(
            request,
            _(f'{update_count} of orders status has been updated to canceled.'),
            messages.SUCCESS
        )

    @admin.action(description=_('Update status to unpaid'))
    def status_unpaid(self, request, queryset):
        update_count = queryset.update(status=Order.OrderStatus.UNPAID)
        self.message_user(
            request,
            _(f'{update_count} of orders status has been updated to unpaid.'),
            messages.SUCCESS
        )
