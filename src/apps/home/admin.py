from django.contrib import admin

from .models import Counter


@admin.register(Counter)
class CounterAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
