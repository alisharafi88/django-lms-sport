from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django.db.models import Count
from django.utils.translation import gettext as _

from .models import Course, Coupon, CourseVideo, CourseMembership, CourseComments, Package


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
    list_display = ('title', 'get_coach', 'price', 'date_modified', 'num_of_videos', 'num_members', 'status')
    list_filter = ('price', 'status', 'date_modified', 'coach')
    search_fields = ('title',)
    date_hierarchy = 'date_modified'
    readonly_fields = ('date_created', 'date_modified',)
    list_select_related = ('coach__user',)
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        (_('Details'), {'fields': ('title', 'coach', 'description', 'img', 'slug',)}),
        (_('Specifications'), {'fields': ('age_range', 'duration',)}),
        (_('Price Information'), {'fields': ('price', 'discount_amount',)}),
        (_('Statuses'), {'fields': ('status', 'certificate_status', 'analysis_room_status', 'extra_movments_status', 'injury_prevention_status')}),
        (_('Date Information'), {'fields': ('date_created', 'date_modified',)}),
    )
    add_fieldsets = (
        (_('Details'), {'fields': ('title', 'coach', 'description', 'img', 'slug',)}),
        (_('Specifications'), {'fields': ('age_range', 'duration',)}),
        (_('Statuses'), {'fields': ('status', 'certificate_status', 'analysis_room_status', 'extra_movments_status', 'injury_prevention_status')}),
        (_('Price Information'), {'fields': ('price', 'discount_amount',)}),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            num_videos=Count('videos'),
            num_members=Count('memberships')
        )

    @admin.display(description='#Videos', ordering='num_videos')
    def num_of_videos(self, course):
        return course.num_videos

    @admin.display(description='#Members', ordering='num_members')
    def num_members(self, course):
        return course.num_members

    @admin.display(description='Coach')
    def get_coach(self, course):
        return course.coach or "No Coach Assigned"


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'date_modified', 'num_courses', 'num_members', 'status')
    list_filter = ('price', 'status', 'date_modified')
    search_fields = ('title',)
    date_hierarchy = 'date_modified'
    readonly_fields = ('date_created', 'date_modified',)
    filter_horizontal = ('courses',)
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        (_('Details'), {'fields': ('title', 'description', 'img', 'slug',)}),
        (_('Courses'), {'fields': ('courses',)}),
        (_('Price Information'), {'fields': ('price', 'discount_amount',)}),
        (_('Statuses'), {'fields': ('status', 'certificate_status', 'analysis_room_status', 'extra_movments_status', 'injury_prevention_status')}),
        (_('Date Information'), {'fields': ('date_created', 'date_modified',)}),
    )
    add_fieldsets = (
        (_('Details'), {'fields': ('title', 'description', 'img', 'slug',)}),
        (_('Courses'), {'fields': ('courses',)}),
        (_('Statuses'), {'fields': ('status', 'certificate_status', 'analysis_room_status', 'extra_movments_status', 'injury_prevention_status')}),
        (_('Price Information'), {'fields': ('price', 'discount_amount',)}),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            num_courses=Count('courses'),
            num_members=Count('memberships')  # Add membership count
        )

    @admin.display(description='#Courses', ordering='num_courses')
    def num_courses(self, package):
        return package.num_courses

    @admin.display(description='#Members', ordering='num_members')
    def num_members(self, package):
        return package.num_members


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
    list_display = ('user', 'product_type', 'product_title', 'date_modified')
    list_filter = ('content_type', 'date_modified')
    search_fields = ('user__username', 'object_id')
    list_select_related = ['user']
    date_hierarchy = 'date_created'
    readonly_fields = ('date_modified', 'date_created',)
    list_per_page = 10

    fieldsets = (
        (_('User Information'), {'fields': ('user',)}),
        (_('Product Information'), {'fields': ('content_type', 'object_id')}),
        (_('Date Information'), {'fields': ('date_created', 'date_modified',)}),
    )
    add_fieldsets = (
        (_('User Information'), {'fields': ('user',)}),
        (_('Product Information'), {'fields': ('content_type', 'object_id')}),
    )

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    @admin.display(description='Product Type')
    def product_type(self, membership):
        return membership.content_type.model.capitalize()

    @admin.display(description='Product Title')
    def product_title(self, membership):
        return str(membership.product) if membership.product else "Unknown Product"


admin.site.register(CourseComments)
