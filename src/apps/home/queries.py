from apps.courses.models import CourseComments
from apps.instructors.models import Instructor
from apps.blogs.models import Blog


def get_featured_instructors():
    return Instructor.objects.select_related(
        'user'
    ).filter(
        is_active=True
    ).only(
        'user__first_name',
        'user__last_name',
        'user__profile_photo',
        'slug',
        'id',
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
        'id',
        'slug',
    )[:3]
    
def get_top_comment():
    comments_queryset = CourseComments.objects.select_related('course', 'user').filter(status=True).order_by('rate')[:5]
    return comments_queryset
    
