from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from .queries import get_featured_instructors, get_latest_blogs, get_top_comment
from ..courses.queries import get_combined_course_package_queryset


class HomeView(View):
    template_name = 'home/home.html'

    def get(self, request):
        top_courses_query = get_combined_course_package_queryset()[:6]
        featured_instructors_query = get_featured_instructors()
        latest_blogs_query = get_latest_blogs()
        top_course_comment = get_top_comment()
        return render(
            request,
            self.template_name,
            {
                'products': top_courses_query,
                'instructors': featured_instructors_query,
                'blogs': latest_blogs_query,
                'comments': top_course_comment,
            }
        )


class AboutUsView(View):
    template_name = 'home/aboutus.html'

    def get(self, request):
        featured_instructors_query = get_featured_instructors()
        return render(request, self.template_name, {'instructors': featured_instructors_query})


class BMIView(TemplateView):
    template_name = 'BMI/BMI.html'
