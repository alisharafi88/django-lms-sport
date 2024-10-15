from courses.models import Course
from instructors.models import Instructor
from blogs.models import Blog


def get_top_courses():
    return Course.objects.filter(status=True).only('title', 'parent__title', 'price', 'discount_amount', 'slug', 'id')[:3]


def get_featured_instructors():
    return Instructor.objects.select_related('user').filter(status=True).only('user__first_name', 'user__last_name', 'img', 'slug', 'id')[:3]


def get_latest_blogs():
    return Blog.objects.select_related('author__user').filter(status=Blog.BLOG_STATUS_PUBLISHED).only('title', 'date_created', 'img', 'author__user__first_name', 'author__user__last_name', 'id', 'slug',)[:3]
