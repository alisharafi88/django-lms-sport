from django.contrib.contenttypes.models import ContentType
from django.db.models import Prefetch, F, Count, Avg, Q, Value, IntegerField

from apps.courses.models import Course
from .models import Instructor, InstructorHonor


def get_all_instructor():
    """
    all the instructors who are active.
    The 'only' method was used to ensure we have access to the Instructor’s full_name property and get_absolute_url method.
    :return: queryset
    """

    course_ct = ContentType.objects.get_for_model(Course)

    return Instructor.objects.select_related(
        'user'
    ).only(
        'user__profile_photo',
        'id',
        'slug',
        'is_master',
        'telegram_id',
        'youtube_id',
        'instagram_id',
        'user__first_name',
        'user__last_name',
    ).filter(
        is_active=True,
    ).annotate(
        student_count=Count(
            'courses__memberships__user',
            distinct=True,
            filter=Q(courses__memberships__content_type=course_ct),
        ),
        video_count=Count(
            'courses__seasons__videos',
        )

    )


def get_instructor_by_id_slug(pk, slug):
    course_ct = ContentType.objects.get_for_model(Course)
    return Instructor.objects.filter(
        pk=pk,
        slug=slug,
        is_active=True,
    ) \
        .select_related(
        'user',
    ) \
        .prefetch_related(
        'widjets',
        Prefetch(
            'honors',
            queryset=InstructorHonor.objects.filter(status=True)
        ),
        Prefetch(
            'courses',
            queryset=Course.objects.filter(
                status=True
            ).annotate(
                num_comment=Count('comments', distinct=True),
                avg_rate=Avg('comments__rate'),
                discounted_price=F('price') - F('discount_amount'),
                num_members=Count('memberships', filter=Q(memberships__content_type=course_ct), distinct=True),
                num_videos=Count('seasons__videos'),
                product_type=Value(1, output_field=IntegerField()),  # 1 = course
            )
        )
    )
