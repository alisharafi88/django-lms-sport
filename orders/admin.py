from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

from orders.models import Order, OrderItem, DVDOrderDetail


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class DVDOrderDetailInline(admin.TabularInline):
    model = DVDOrderDetail
    extra = 0


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
    inlines = (OrderItemInline, DVDOrderDetailInline,)

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

    @admin.action(description=_('Update status to PAID'))
    def status_paid(self, request, queryset):
        update_count = queryset.update(status=Order.OrderStatus.PAID)
        self.message_user(
            request,
            _(f'{update_count} of orders status has been updated to paid.'),
            messages.WARNING
        )

    @admin.action(description=_('Update status to CANCELED'))
    def status_canceled(self, request, queryset):
        update_count = queryset.update(status=Order.OrderStatus.CANCELED)
        self.message_user(
            request,
            _(f'{update_count} of orders status has been updated to canceled.'),
            messages.SUCCESS
        )

    @admin.action(description=_('Update status to UNPAID'))
    def status_unpaid(self, request, queryset):
        update_count = queryset.update(status=Order.OrderStatus.UNPAID)
        self.message_user(
            request,
            _(f'{update_count} of orders status has been updated to unpaid.'),
            messages.SUCCESS
        )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'unit_price',)
    list_per_page = 50
    search_fields = ('order', 'order__customer',)

    fieldsets = (
        (_('Order'), {'fields': ('order',)}),
        (_('course information'), {'fields': ('course', 'unit_price',)}),
    )


@admin.register(DVDOrderDetail)
class DVDOrderDetailAdmin(admin.ModelAdmin):
    list_display = ('order', 'date_created', 'delivery_status',)
    list_per_page = 50
    search_fields = ('order', 'order__customer', 'address',)
    list_editable = ('delivery_status',)
    date_hierarchy = 'date_created'
    list_filter = ('delivery_status',)
    actions = ('delivery_status_pending', 'delivery_status_sent', 'delivery_status_rejectd', 'delivery_status_canceled',)
    readonly_fields = ('date_created',)

    fieldsets = (
        (_('order'), {'fields': ('order',)}),
        (_('delivery information'), {'fields': ('address', 'postal_code', 'order_note', 'delivery_status', 'date_created',)}),
    )
    add_fieldsets = (
        (_('order'), {'fields': ('order',)}),
        (_('delivery information'), {'fields': ('address', 'postal_code', 'order_note', 'delivery_status',)}),
    )

    @admin.action(description=_('Update delivery_status to PENDING'))
    def delivery_status_pending(self, request, queryset):
        update_count = queryset.update(delivery_status=DVDOrderDetail.delivery_status.PENDING)
        self.message_user(
            request,
            _(f'{update_count} of orders delivery_status has been updated to pending.'),
            messages.SUCCESS
        )

    @admin.action(description=_('Update delivery_status to SENT'))
    def delivery_status_sent(self, request, queryset):
        update_count = queryset.update(delivery_status=DVDOrderDetail.delivery_status.SENT)
        self.message_user(
            request,
            _(f'{update_count} of orders delivery_status has been updated to sent.'),
            messages.SUCCESS
        )

    @admin.action(description=_('Update delivery_status to REJECTD'))
    def delivery_status_rejectd(self, request, queryset):
        update_count = queryset.update(delivery_status=DVDOrderDetail.delivery_status.REJECTED)
        self.message_user(
            request,
            _(f'{update_count} of orders delivery_status has been updated to rejectd.'),
            messages.SUCCESS
        )

    @admin.action(description=_('Update delivery_status to CANCELED'))
    def delivery_status_canceled(self, request, queryset):
        update_count = queryset.update(delivery_status=DVDOrderDetail.delivery_status.CANCELED)
        self.message_user(
            request,
            _(f'{update_count} of orders delivery_status has been updated to canceled.'),
            messages.SUCCESS
        )
