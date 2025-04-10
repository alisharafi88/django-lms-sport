from django.contrib import admin
from django.db.models import Count, Q
from django.utils.translation import gettext_lazy as _

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
    list_display = ('full_name', 'phone_number', 'num_of_courses', 'is_active',)
    fieldsets = (
        (None, {'fields': ('user', 'slug')}),
        (_('instructor info'), {'fields': ('description', 'experience')}),
        (_('status info'), {'fields': ('is_active',)}),
    )
    list_editable = ('is_active',)
    inlines = (InstructorWidjetInline, InstructorHonorInline,)

    search_fields = ('user__first_name', 'user__last_name', 'user__phone_number')

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            instructors = queryset.filter(Q(user__first_name__icontains=search_term) | Q(user__last_name__icontains=search_term))
            queryset = instructors
        except ValueError:
            pass
        return queryset, use_distinct

    @admin.display(ordering='user__first_name', description=_('FullName'))
    def full_name(self, instructor):
        return instructor.full_name

    @admin.display(ordering='user__phone_number', description=_('PhoneNumber'))
    def phone_number(self, instructor):
        return instructor.user.phone_number

    def get_queryset(self, request):
        return super().get_queryset(request) \
                .select_related('user') \
                .prefetch_related('courses') \
                .annotate(num_of_courses=Count('courses'))

    @admin.display(description=_('#courses'), ordering='num_of_courses')
    def num_of_courses(self, instructor):
        return instructor.num_of_courses


@admin.register(InstructorHonor)
class InstructorHonorAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('instructor', 'status',)
    search_fields = ('instructor__user__first_name', 'instructor__user__last_name', 'instructor__user__phone_number', 'text',)
    list_editable = ('status',)
    list_select_related = ('instructor__user',)


@admin.register(InstructorWidjet)
class InstructorWidjetAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('instructor',)
    search_fields = ('instructor__user__first_name', 'instructor__user__last_name', 'instructor__user__phone_number', 'widjet')
    list_select_related = ('instructor__user',)





