from django.contrib import admin
from django.db.models import Count, Q
from django.utils.translation import gettext as _

from jalali_date.admin import ModelAdminJalaliMixin, TabularInlineJalaliMixin

from .models import Instructor, InstructorHonor, InstructorWidjet


class InstructorWidjetInline(TabularInlineJalaliMixin, admin.TabularInline):
    model = InstructorWidjet
    extra = 0


class InstructorHonorInline(TabularInlineJalaliMixin, admin.TabularInline):
    model = InstructorHonor
    extra = 0


@admin.register(Instructor)
class InstructorAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'num_of_courses', 'is_master', 'is_active',)
    fieldsets = (
        (None, {'fields': ('user', 'slug')}),
        (_('instructor info'), {'fields': ('description', 'experience')}),
        (_('social media info'), {'fields': ('telegram_id', 'youtube_id', 'instagram_id',)}),
        (_('status info'), {'fields': ('is_active', 'is_master',)}),
    )
    list_editable = ('is_active',)
    inlines = (InstructorWidjetInline, InstructorHonorInline,)

    # search_fields = ('full_name',)
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            instructors = queryset.filter(Q(user__first_name__icontains=search_term) | Q(user__last_name__icontains=search_term))
            queryset = instructors
        except ValueError:
            pass
        return queryset, use_distinct

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
class InstructorHonorAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('instructor', 'status',)
    search_fields = ('instructor', 'text',)
    list_editable = ('status',)
    list_filter = ('instructor',)


@admin.register(InstructorWidjet)
class InstructorWidjetAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('instructor',)
    search_fields = ('instructor', 'widjet',)





