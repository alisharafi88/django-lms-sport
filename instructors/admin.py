from django.contrib import admin
from django.db.models import Count
from django.utils.translation import gettext as _

from .models import Instructor, InstructorHonor, InstructorWidjet


class InstructorWidjetInline(admin.TabularInline):
    model = InstructorWidjet
    extra = 0


class InstructorHonorInline(admin.TabularInline):
    model = InstructorHonor
    extra = 0


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'num_of_courses', 'status',)
    fieldsets = (
        (None, {'fields': ('user', 'slug')}),
        (_('instructor info'), {'fields': ('description', 'exprience', 'img',)}),
        (_('social media info'), {'fields': ('telegram_id', 'youtube_id', 'instagram_id',)}),
        (_('status info'), {'fields': ('status',)}),
    )
    search_fields = ('full_name',)
    list_editable = ('status',)
    inlines = (InstructorWidjetInline, InstructorHonorInline,)

    @admin.display(ordering='user__first_name')
    def full_name(self, instructor):
        return instructor.full_name

    @admin.display(ordering='user__phone_number')
    def phone_number(self, instructor):
        return instructor.user.phone_number

    def get_queryset(self, request):
        return super().get_queryset(request) \
                .select_related('user') \
                .prefetch_related('courses') \
                .annotate(num_of_courses=Count('courses'))

    @admin.display(description=_('# courses'), ordering='num_of_courses')
    def num_of_courses(self, instructor):
        return instructor.num_of_courses


@admin.register(InstructorHonor)
class InstructorHonorAdmin(admin.ModelAdmin):
    list_display = ('instructor', 'status',)
    search_fields = ('instructor', 'text',)
    list_editable = ('status',)
    list_filter = ('instructor',)


@admin.register(InstructorWidjet)
class InstructorWidjetAdmin(admin.ModelAdmin):
    list_display = ('instructor',)
    search_fields = ('instructor', 'widjet',)





