from django.contrib import admin
from django.db.models import Count, OuterRef, IntegerField, Subquery, Prefetch
from django.utils.translation import gettext as _

from .models import Course, Coupon, CourseVideo, CourseMembership, CourseComments, Package, CourseSeason


class CourseVideoInline(admin.StackedInline):
    model = CourseVideo
    extra = 1
    fields = ('title', 'status')
    readonly_fields = ('created_at', 'updated_at')


class CourseSeasonInline(admin.StackedInline):
    model = CourseSeason
    extra = 1
    readonly_fields = ('created_at', 'updated_at')

    inlines = (CourseVideoInline,)


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
    list_display = ('title', 'get_coach', 'price', 'date_modified', 'get_num_videos', 'get_num_members', 'status')
    list_filter = ('price', 'status', 'date_modified', 'coach')
    search_fields = ('title',)
    date_hierarchy = 'date_modified'
    readonly_fields = ('date_created', 'date_modified',)
    list_select_related = ('coach__user',)
    prepopulated_fields = {'slug': ('title',)}

    inlines = (CourseSeasonInline,)

    fieldsets = (
        (_('Details'), {'fields': ('title', 'coach', 'description', 'img', 'slug',)}),
        (_('Specifications'), {'fields': ('age_range', 'duration',)}),
        (_('Price Information'), {'fields': ('price', 'discount_amount',)}),
        (_('Statuses'), {'fields': (
            'status', 'certificate_status', 'analysis_room_status', 'extra_movments_status',
            'injury_prevention_status')}),
        (_('Date Information'), {'fields': ('date_created', 'date_modified',)}),
    )
    add_fieldsets = (
        (_('Details'), {'fields': ('title', 'coach', 'description', 'img', 'slug',)}),
        (_('Specifications'), {'fields': ('age_range', 'duration',)}),
        (_('Statuses'), {'fields': (
            'status', 'certificate_status', 'analysis_room_status', 'extra_movments_status',
            'injury_prevention_status')}),
        (_('Price Information'), {'fields': ('price', 'discount_amount',)}),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_queryset(self, request):
        video_count_subquery = CourseVideo.objects.filter(
            season__course=OuterRef('pk')
        ).values('season__course').annotate(count=Count('id')).values('count')

        return super().get_queryset(request).annotate(
            num_videos=Subquery(video_count_subquery, output_field=IntegerField()),
            num_members=Count('memberships')
        ).prefetch_related('memberships', Prefetch('seasons', queryset=CourseSeason.objects.prefetch_related('videos').all()))

    @admin.display(description='#Videos', ordering='num_videos')
    def get_num_videos(self, course):
        return course.num_videos

    @admin.display(description='#Members', ordering='num_members')
    def get_num_members(self, course):
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
        (_('Details'), {'fields': ('title', 'description', 'slug')}),
        (_('Media'), {'fields': ('img', 'introduce_video_url', 'introduce_video_cover')}),
        (_('Specifications'), {'fields': ('age_range', 'duration',)}),
        (_('Courses'), {'fields': ('courses',)}),
        (_('Price Information'), {'fields': ('price', 'discount_amount',)}),
        (_('Statuses'), {'fields': (
            'status', 'certificate_status', 'analysis_room_status', 'extra_movments_status',
            'injury_prevention_status')}),
        (_('Date Information'), {'fields': ('date_created', 'date_modified',)}),
    )
    add_fieldsets = (
        (_('Details'), {'fields': ('title', 'description', 'img', 'slug',)}),
        (_('Courses'), {'fields': ('courses',)}),
        (_('Statuses'), {'fields': (
            'status', 'certificate_status', 'analysis_room_status', 'extra_movments_status',
            'injury_prevention_status')}),
        (_('Price Information'), {'fields': ('price', 'discount_amount',)}),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            num_courses=Count('courses'),
            num_members=Count('memberships')
        )

    @admin.display(description='#Courses', ordering='num_courses')
    def num_courses(self, package):
        return package.num_courses

    @admin.display(description='#Members', ordering='num_members')
    def num_members(self, package):
        return package.num_members


@admin.register(CourseSeason)
class CourseSeasonAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('title', 'course__title')
    ordering = ('created_at',)

    list_select_related = ('course',)

    inlines = (CourseVideoInline,)

    fieldsets = (
        (_('General Information'), {
            'fields': ('course', 'title'),
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = ('created_at', 'updated_at')


@admin.register(CourseVideo)
class CourseVideoAdmin(admin.ModelAdmin):
    list_display = ('season_course_title', 'title', 'status_display', 'created_at')

    list_filter = ('status', 'season__course', 'created_at')

    search_fields = ('title', 'season__title', 'season__course__title')

    ordering = ('created_at',)

    list_select_related = ('season__course',)

    fieldsets = (
        (_('General Information'), {
            'fields': ('season', 'title', 'status'),
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),

        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    @admin.display(description=_('Course'), ordering='season__course__title')
    def season_course_title(self, obj):
        return obj.season.course.title

    @admin.display(description=_('Status'), ordering='status')
    def status_display(self, obj):
        return obj.get_status_display()


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
