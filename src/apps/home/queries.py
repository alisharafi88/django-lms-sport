from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Q, Value, IntegerField, F

from apps.courses.models import Course, Package
from apps.instructors.models import Instructor
from apps.blogs.models import Blog


def get_top_products():
    course_content_type = ContentType.objects.get_for_model(Course)
    package_content_type = ContentType.objects.get_for_model(Package)

    # Queryset for courses
    courses_queryset = Course.objects.filter(status=True).annotate(
        num_members=Count('memberships', filter=Q(memberships__content_type=course_content_type)),
        num_videos=Count('videos'),
        product_type=Value(1, output_field=IntegerField()),  # 1 = course
        num_courses=Value(0, output_field=IntegerField()),
        discounted_price=F('price') - F('discount_amount')
    ).defer('coach', 'duration')

    # Queryset for packages
    packages_queryset = Package.objects.filter(status=True).annotate(
        num_members=Count('memberships', filter=Q(memberships__content_type=package_content_type)),
        num_videos=Value(0, output_field=IntegerField()),
        product_type=Value(2, output_field=IntegerField()),  # 2 = package
        num_courses=Count('courses'),
        discounted_price=F('price') - F('discount_amount')
    )

    # Combine the two querysets using union
    combined_queryset = courses_queryset.union(packages_queryset, all=True).order_by('-date_created', '-date_modified')[:3]
    return combined_queryset
    # return Course.objects.filter(status=True).only('title', 'parent__title', 'img', 'price', 'discount_amount', 'slug',
    #                                                'id')[:3]


def get_featured_instructors():
    return Instructor.objects.select_related(
        'user'
    ).filter(
        is_active=True
    ).only(
        'user__first_name',
        'user__last_name',
        'slug',
        'id'
    )[:3]


def get_latest_blogs():
    return Blog.objects.select_related(
        'author__user'
    ).filter(
        status=Blog.BLOG_STATUS_PUBLISHED
    ).only(
        'title',
        'date_created',
        'img',
        'author__user__first_name',
        'author__user__last_name',
        'id', 'slug',
    )[:3]
