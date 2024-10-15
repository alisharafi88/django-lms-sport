from django.db.models import Prefetch, F

from courses.models import Course
from instructors.models import Instructor, InstructorHonor


def get_all_instructor():
    """
    all the instructors who are active.
    The 'only' method was used to ensure we have access to the Instructor’s full_name property and get_absolute_url method.
    :return: queryset
    """
    return Instructor.objects.select_related('user').only('img', 'id', 'slug', 'telegram_id', 'youtube_id',
                                                          'instagram_id', 'user__first_name',
                                                          'user__last_name', ).filter(status=True)


def get_instructor_by_id_slug(pk, slug):
    return Instructor.objects.filter(pk=pk, slug=slug, status=True,)\
            .select_related('user')\
            .prefetch_related('widjets', Prefetch('honors', queryset=InstructorHonor.objects.filter(status=True)), Prefetch('courses', queryset=Course.objects.filter(status=True)))\
