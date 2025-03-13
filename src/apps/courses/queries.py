from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Case, When, Value, F, CharField, Q, Count, IntegerField, Avg
from django.db.models.functions import Concat
from django.urls import reverse

from .models import Course, Package


def get_courses_queryset():
    """
        Retrieve a queryset of active courses with annotated fields.
    """
    course_content_type = ContentType.objects.get_for_model(Course)

    # Generate base URL (e.g., '/courses/course/slug')
    base_course_url = reverse('courses:course_detail', args=['dummy-slug']).replace('dummy-slug', '').rstrip('/')

    queryset = Course.objects.filter(status=True).annotate(
        coach_profile=Case(
            When(coach__user__profile_photo__isnull=False,
                 then=Concat(Value(settings.MEDIA_URL), F("coach__user__profile_photo"), output_field=CharField())),
            output_field=CharField(),
        ),
        num_members=Count('memberships', filter=Q(memberships__content_type=course_content_type), distinct=True),
        num_videos=Count('seasons__videos'),
        product_type=Value(1, output_field=IntegerField()),  # 1 = course
        num_courses=Value(0, output_field=IntegerField()),
        discounted_price=F('price') - F('discount_amount'),
        avg_rate=Avg('comments__rate'),
        num_comment=Count('comments', distinct=True),
        get_absolute_url=Concat(
            Value(base_course_url + '/'),
            F('slug'),
            Value('/'),
            output_field=CharField(),
        ),
    ).values(
        'id',
        'title',
        'coach_profile',
        'num_members',
        'num_videos',
        'product_type',
        'slug',
        'num_courses',
        'discounted_price',
        'avg_rate',
        'num_comment',
        'date_created',
        'date_modified',
        'img',
        'get_absolute_url',
    )

    return queryset


def get_packages_queryset():
    """
        Retrieve a queryset of active packages with annotated fields.
    """
    package_content_type = ContentType.objects.get_for_model(Package)

    # Generate base URL (e.g., '/courses/package/slug')
    base_course_url = reverse('courses:package_detail', args=['dummy-slug']).replace('dummy-slug', '').rstrip('/')

    queryset = Package.objects.filter(status=True).annotate(
        coach_profile=Value(None, output_field=CharField()),
        num_members=Count('memberships', filter=Q(memberships__content_type=package_content_type), distinct=True),
        num_videos=Value(0, output_field=IntegerField()),
        product_type=Value(2, output_field=IntegerField()),  # 2 = package
        num_courses=Count('courses'),
        discounted_price=F('price') - F('discount_amount'),
        avg_rate=Avg('courses__comments__rate'),
        num_comment=Count('courses__comments', distinct=True),
        get_absolute_url=Concat(
            Value(base_course_url + '/'),
            F('slug'),
            Value('/'),
            output_field=CharField(),
        ),
    ).values(
        'id',
        'title',
        'coach_profile',
        'num_members',
        'num_videos',
        'product_type',
        'slug',
        'num_courses',
        'discounted_price',
        'avg_rate',
        'num_comment',
        'date_created',
        'date_modified',
        'img',
        'get_absolute_url',
    )

    return queryset


def get_combined_course_package_queryset(search=None):
    """
        Retrieve a combined queryset of active courses & packages with search feature.
    """
    courses_queryset = get_courses_queryset()
    packages_queryset = get_packages_queryset()

    if search:
        courses_queryset = courses_queryset.filter(title__icontains=search)
        packages_queryset = packages_queryset.filter(title__icontains=search)

    combined_queryset = courses_queryset.union(packages_queryset, all=True).order_by('-date_created', '-date_modified')
    return combined_queryset
