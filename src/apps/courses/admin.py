from django.contrib import admin
from django.db.models import Count, OuterRef, IntegerField, Subquery, Prefetch
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin

from .models import Course, Coupon, CourseVideo, CourseMembership, CourseComments, Package, CourseSeason, \
    CourseTelegramLink, CouponUsage


class CourseVideoInline(StackedInlineJalaliMixin, admin.StackedInline):
    model = CourseVideo
    extra = 1
    fields = ('title', 'status')
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related('season__course')
        return queryset


class CourseSeasonInline(TabularInlineJalaliMixin, admin.StackedInline):
    model = CourseSeason
    extra = 1
    readonly_fields = ('created_at', 'updated_at')

    inlines = (CourseVideoInline,)

    def get_queryset(self, request):
        queryset = super().get_queryset(request).prefetch_related('videos')
        return queryset


@admin.register(Coupon)
class CouponAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('code', 'date_valid_from', 'date_valid_to', 'status',)
    search_fields = ('code',)
    list_filter = ('status',)
    date_hierarchy = 'date_valid_from'

    fieldsets = (
        (_('Coupon code'), {'fields': ('code',)}),
        (_('Discount amount'), {'fields': ('discount_amount',)}),
        (_('Date range'), {'fields': ('date_valid_from', 'date_valid_to',)}),
        (_('Statuses'), {'fields': ('max_usage_total', 'max_usage_per_user', 'status')}),
    )


@admin.register(CouponUsage)
class CouponUsageAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('coupon', 'user')
    search_fields = ('user__phone_number', 'coupon__code')
    date_hierarchy = 'usage_date'
    list_select_related = ('user',)


@admin.register(Course)
class CourseAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('title', 'get_coach', 'price', 'date_modified', 'get_num_videos', 'get_num_members', 'telegram_link_count', 'available_links', 'status')
    list_filter = ('status', 'date_modified')
    search_fields = ('title', 'coach__user__first_name', 'coach__user__last_name')
    date_hierarchy = 'date_modified'
    readonly_fields = ('date_created', 'date_modified',)
    list_select_related = ('coach__user',)
    prepopulated_fields = {'slug': ('title',)}

    list_per_page = 5

    inlines = (CourseSeasonInline,)

    fieldsets = (
        (_('Details'), {'fields': ('title', 'coach', 'description', 'img', 'slug',)}),
        (_('Specifications'), {'fields': ('age_range', 'duration', 'free_leasson_link', 'is_featured_on_homepage')}),
        (_('Price Information'), {'fields': ('price', 'discount_amount',)}),
        (_('Statuses'), {'fields': (
            'status', 'certificate_status', 'analysis_room_status', 'extra_movments_status',
            'injury_prevention_status')}),
        (_('Date Information'), {'fields': ('date_created', 'date_modified',)}),
    )
    add_fieldsets = (
        (_('Details'), {'fields': ('title', 'coach', 'description', 'img', 'slug',)}),
        (_('Specifications'), {'fields': ('age_range', 'duration', 'free_leasson_link', 'is_featured_on_homepage')}),
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
        ).prefetch_related(
            'memberships',
            'telegram_links',
            Prefetch(
                'seasons',
                queryset=CourseSeason.objects.prefetch_related('videos').all()
            )
        ).select_related(
            'coach__user',
        )

    @admin.display(description=_('#Videos'), ordering='num_videos')
    def get_num_videos(self, course):
        return course.num_videos

    @admin.display(description=_('#Members'), ordering='num_members')
    def get_num_members(self, course):
        return course.num_members

    @admin.display(description=_('Coach'))
    def get_coach(self, course):
        return course.coach or _('No Coach Assigned')

    @admin.display(description=_('#TotalLinks'))
    def telegram_link_count(self, obj):
        return obj.telegram_links.count()

    @admin.display(description=_('#AvailableLinks'))
    def available_links(self, obj):
        count = obj.telegram_links.filter(is_used=False).count()
        color = 'green' if count > 0 else 'red'
        return format_html(f'<span style="color:{color}">{count}</span>')

    def save_model(self, request, obj, form, change):

        if obj.is_featured_on_homepage:
            Course.objects.filter(is_featured_on_homepage=True).exclude(pk=obj.pk).update(is_featured_on_homepage=False)
        super().save_model(request, obj, form, change)


@admin.register(Package)
class PackageAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('title', 'price', 'date_modified', 'num_courses', 'num_members', 'status')
    list_filter = ('status', 'date_modified')
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

    @admin.display(description=_('#Courses'), ordering='num_courses')
    def num_courses(self, package):
        return package.num_courses

    @admin.display(description=_('#Members'), ordering='num_members')
    def num_members(self, package):
        return package.num_members


@admin.register(CourseSeason)
class CourseSeasonAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
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

    def get_queryset(self, request):
        queryset = super().get_queryset(request).prefetch_related('videos')
        return queryset


@admin.register(CourseVideo)
class CourseVideoAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
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
class CourseMembershipAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('user', 'product_type', 'product_title', 'date_modified')
    list_filter = ('content_type', 'date_modified')
    search_fields = ('user__phone_number', 'object_id')
    list_select_related = ['user', 'content_type']
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

    def get_queryset(self, request):
        queryset = super().get_queryset(request).prefetch_related('product')
        return queryset

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    @admin.display(description=_('Product Type'))
    def product_type(self, membership):
        return membership.content_type.model.capitalize()

    @admin.display(description=_('Product Title'))
    def product_title(self, membership):
        return str(membership.product) if membership.product else _('Unknown Product')


@admin.register(CourseTelegramLink)
class TelegramLinkAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('course', 'invite_link', 'user', 'date_created', 'date_used', 'is_used')
    list_filter = ('course', 'is_used')
    search_fields = ('course__title', 'invite_link')
    readonly_fields = ('date_created', 'date_used')
    list_select_related = ('user', 'course')


@admin.register(CourseComments)
class CourseCommentsAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'rate', 'status')
    date_hierarchy = 'date_created'
    search_fields = ('course__title', 'user__phone_number')
    select_related = ('user', 'course')


