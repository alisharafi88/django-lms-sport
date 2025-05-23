from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from jalali_date.admin import ModelAdminJalaliMixin

from .models import QuestionAnswer


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('question', 'date_created', 'status',)
    list_filter = ('date_created', 'status',)
    search_fields = ('question', 'answer', 'date_created', 'status',)
    date_hierarchy = 'date_created'
    readonly_fields = ('date_created', 'date_modified',)
    ordering = ('-date_created',)
    actions = ('status_to_false', 'status_to_true',)
    fieldsets = (
        (_('QuestionAnswer'), {'fields': ('question', 'answer',)}),
        (_('Status'), {'fields': ('status',)}),
        (_('Date\'s informations'), {'fields': ('date_created', 'date_modified',)}),
    )
    add_fieldsets = (
        ('_(QuestionAnswer', {'fields': ('question', 'answer',)}),
        (_('Status'), {'fields': ('status',)}),
    )

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    @admin.action(description=_('Change status to false'),)
    def status_to_false(self, request, queryset):
        updated_count = queryset.update(status=False)
        self.message_user(
            request,
            _(f'{updated_count} of status changed to false.'),
        )
        return updated_count

    @admin.action(description=_('Change status to True'),)
    def status_to_true(self, request, queryset):
        updated_count = queryset.update(status=True)
        self.message_user(
            request,
            _(f'{updated_count} of status changed to True.')
        )
        return updated_count
