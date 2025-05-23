from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _

from jalali_date.admin import ModelAdminJalaliMixin

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(CustomUser)
class CustomUserAdmin(ModelAdminJalaliMixin, UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('phone_number', 'is_staff',)
    ordering = ('date_joined',)
    search_fields = ('phone_number', 'first_name', 'last_name', 'email')
    list_per_page = 10

    fieldsets = (
        (_('Personal info'), {'fields': ('profile_photo', 'first_name', 'last_name', 'email', 'phone_number', 'bio')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('phone_number', 'password1', 'password2'),
            },
        ),
    )
