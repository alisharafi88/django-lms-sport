from django.contrib import admin
from django.db.models import Count
from django.utils.translation import gettext as _

from .models import Course, Coupon, CourseVideo, CourseMembership, CourseComments


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('discount_amount', 'date_valid_from', 'date_valid_to', 'status',)

    fieldsets = (
        (_('Coupon code'), {'fields': ('code',)}),
        (_('Discount amount'), {'fields': ('discount_amount',)}),
        (_('Date range'), {'fields': ('date_valid_from', 'date_valid_to',)}),
        (_('Statuses'), {'fields': ('max_usage_per_user', 'status')}),
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_instructor', 'price', 'date_modified', 'num_of_videos', 'status',)
    list_filter = ('price', 'status', 'date_modified', 'instructor',)
    search_fields = ('title',)
    date_hierarchy = 'date_modified'
    readonly_fields = ('date_created', 'date_modified',)
    list_select_related = ('instructor__user',)
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('parent', )
    fieldsets = (
        (_('details'), {'fields': ('title', 'instructor', 'description', 'img', 'slug',)}),
        (_('specifications'), {'fields': ('parent', 'age_range', 'duration',)}),
        (_('Price information'), {'fields': ('price', 'discount_amount',)}),
        (_('Statuses'), {'fields': ('status', 'certificate_status', 'analysis_room_status', 'extra_movments_status', 'injury_prevention_status')}),
        (_('date_information'), {'fields': ('date_created', 'date_modified',)}),

    )
    add_fieldsets = (
        (_('details'), {'fields': ('title', 'instructor', 'description', 'img', 'slug',)}),
        (_('specifications'), {'fields': ('parent', 'age_range', 'duration',)}),
        (_('Statuses'), {'fields': ('status', 'certificate_status', 'analysis_room_status', 'extra_movments_status', 'injury_prevention_status')}),
        (_('Price information'), {'fields': ('price', 'discount_amount',)}),

    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(num_videos=Count('videos'))

    @admin.display(description='#videos', ordering='num_videos')
    def num_of_videos(self, course):
        return course.num_videos

    @admin.display(description='instructor')
    def get_instructor(self, course):
        print(course.is_package)
        if course.is_package:
            return "It's a package"
        return course.instructor


@admin.register(CourseVideo)
class CourseVideoAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'course_title', 'status',)
    list_filter = ('status', 'course',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('course__title', 'title')

    @admin.display(description='course', ordering='course__title')
    def course_title(self, course):
        return course.title


@admin.register(CourseMembership)
class CourseMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'date_modified',)
    list_filter = ('course', 'date_modified',)
    search_fields = ('course__title', 'user__username',)
    list_select_related = ['course', 'user',]
    date_hierarchy = 'date_created'
    readonly_fields = ('date_modified', 'date_created',)
    list_per_page = 10

    fieldsets = (
        (_('User information'), {'fields': ('user',)}),
        (_('Course information'), {'fields': ('course',)}),
        (_('Date information'), {'fields': ('date_created', 'date_modified',)}),
    )
    add_fieldsets = (
        (_('User information'), {'fields': ('user',)}),
        (_('Course information'), {'fields': ('course',)}),
    )

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)


admin.site.register(CourseComments)
