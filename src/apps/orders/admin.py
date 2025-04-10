from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

from jalali_date.admin import ModelAdminJalaliMixin, TabularInlineJalaliMixin, StackedInlineJalaliMixin

from .models import Order, OrderItem, DVDOrderDetail


class OrderItemInline(TabularInlineJalaliMixin, admin.TabularInline):
    model = OrderItem
    extra = 0

    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related('content_type')
        return queryset


class DVDOrderDetailInline(StackedInlineJalaliMixin, admin.StackedInline):
    model = DVDOrderDetail
    extra = 0


@admin.register(Order)
class OrderAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('customer', 'date_created', 'access_status', 'status',)
    list_filter = ('access_status', 'status',)
    search_fields = ('date_created', 'customer__phone_number')
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
        (_('Payment'), {'fields': ('zarinpal_authority', 'zarinpal_ref_id', 'zarinpal_data')}),
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

    def get_queryset(self, request):
        queryset = super().get_queryset(request).prefetch_related('dvd_detail', 'items').select_related('customer')
        return queryset


@admin.register(OrderItem)
class OrderItemAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('order', 'unit_price', 'product_type', 'product_title')
    list_per_page = 50
    search_fields = ('order', 'order__customer',)

    fieldsets = (
        (_('Order'), {'fields': ('order',)}),
        (_('product information'), {'fields': ('content_type', 'object_id', 'unit_price',)}),
    )

    @admin.display(description=_('Type'))
    def product_type(self, obj):
        return obj.content_type.model

    @admin.display(description=_('Product'))
    def product_title(self, obj):
        return obj.product.title


@admin.register(DVDOrderDetail)
class DVDOrderDetailAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
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
        update_count = queryset.update(delivery_status=DVDOrderDetail.DeliveryStatus.PENDING)
        self.message_user(
            request,
            _(f'{update_count} of orders delivery_status has been updated to pending.'),
            messages.SUCCESS
        )

    @admin.action(description=_('Update delivery_status to SENT'))
    def delivery_status_sent(self, request, queryset):
        update_count = queryset.update(delivery_status=DVDOrderDetail.DeliveryStatus.SENT)
        self.message_user(
            request,
            _(f'{update_count} of orders delivery_status has been updated to sent.'),
            messages.SUCCESS
        )

    @admin.action(description=_('Update delivery_status to REJECTD'))
    def delivery_status_rejectd(self, request, queryset):
        update_count = queryset.update(delivery_status=DVDOrderDetail.DeliveryStatus.REJECTED)
        self.message_user(
            request,
            _(f'{update_count} of orders delivery_status has been updated to rejectd.'),
            messages.SUCCESS
        )

    @admin.action(description=_('Update delivery_status to CANCELED'))
    def delivery_status_canceled(self, request, queryset):
        update_count = queryset.update(delivery_status=DVDOrderDetail.DeliveryStatus.CANCELED)
        self.message_user(
            request,
            _(f'{update_count} of orders delivery_status has been updated to canceled.'),
            messages.SUCCESS
        )
