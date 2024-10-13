from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from courses.models import Course
from instructors.models import Instructor
from blogs.models import Blog


class HomeView(View):
    template_name = 'home/home.html'

    def get(self, request):
        courses_queryset = Course.objects.filter(status=True)[:3]
        instructors_queryset = Instructor.objects.select_related('user').filter(status=True)[:3]
        blogs_queryset = Blog.objects.select_related('author__user').filter(status=Blog.BLOG_STATUS_PUBLISHED)[:3]
        return render(
            request,
            self.template_name,
            {
                'courses': courses_queryset,
                'instructors': instructors_queryset,
                'blogs': blogs_queryset,
            }
        )


class AboutUsView(View):
    template_name = 'home/aboutus.html'

    def get(self, request):
        instructors_queryset = Instructor.objects.select_related('user').filter(status=True)[:3]
        return render(request, self.template_name, {'instructors': instructors_queryset,})
