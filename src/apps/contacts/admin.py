from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.template.response import TemplateResponse

from admin_confirm.admin import AdminConfirmMixin
from jalali_date.admin import ModelAdminJalaliMixin

from .models import ContactInfo, Message


@admin.register(ContactInfo)
class ContactInfoAdmin(ModelAdminJalaliMixin, AdminConfirmMixin, admin.ModelAdmin):
    confirm_change = True
    confirm_add = True
    confirmation_fields = ('is_primary',)

    list_display = ('phonenumber', 'email', 'is_primary',)
    list_editable = ('is_primary',)
    search_fields = ('phonenumber', 'email',)
    list_filter = ('is_primary',)

    fieldsets = (
        (_('Contact Information'), {'fields': ('phonenumber', 'email', 'address')}),
        (_('SocialMedia Information'), {'fields': ('telegram_id', 'youtube_id', 'instagram_id')}),
        (_('Status'), {'fields': ('is_primary',)}),
    )

    def render_change_confirmation(self, request, context):
        primary_instance = ContactInfo.objects.filter(is_primary=True).first()
        context['primary_instance'] = primary_instance
        return TemplateResponse(request, 'admin/custom_change_confirmation.html', context)


@admin.register(Message)
class MessageAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('user', 'date_sent',)
    list_filter = ('user',)
    search_fields = ('user',)
    date_hierarchy = 'date_sent'
    readonly_fields = ('date_sent',)

    fieldsets = (
        (_('user information'), {'fields': ('user',)}),
        (_('message info'), {'fields': ('text', 'date_sent',)}),
    )
    add_fieldsets = (
        (_('user information'), {'fields': ('user',)}),
        (_('message info'), {'fields': ('text',)}),
    )
    
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)
