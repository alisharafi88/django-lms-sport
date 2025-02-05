from django.db.models import Prefetch, F

from apps.courses.models import Course
from .models import Instructor, InstructorHonor


def get_all_instructor():
    """
    all the instructors who are active.
    The 'only' method was used to ensure we have access to the Instructor’s full_name property and get_absolute_url method.
    :return: queryset
    """
    return Instructor.objects.select_related('user').only('img', 'id', 'slug', 'is_master', 'telegram_id', 'youtube_id',
                                                          'instagram_id', 'user__first_name',
                                                          'user__last_name', ).filter(is_active=True)


def get_instructor_by_id_slug(pk, slug):
    return Instructor.objects.filter(pk=pk, slug=slug, is_active=True,)\
            .select_related('user')\
            .prefetch_related('widjets', Prefetch('honors', queryset=InstructorHonor.objects.filter(status=True)), Prefetch('courses', queryset=Course.objects.filter(status=True)))
