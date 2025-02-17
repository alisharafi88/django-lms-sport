from django.shortcuts import render
from django.views import View

from .queries import get_top_products, get_featured_instructors, get_latest_blogs


class HomeView(View):
    template_name = 'home/home.html'

    def get(self, request):
        top_courses_query = get_top_products()
        featured_instructors_query = get_featured_instructors()
        latest_blogs_query = get_latest_blogs()
        return render(
            request,
            self.template_name,
            {
                'products': top_courses_query,
                'instructors': featured_instructors_query,
                'blogs': latest_blogs_query,
            }
        )


class AboutUsView(View):
    template_name = 'home/aboutus.html'

    def get(self, request):
        featured_instructors_query = get_featured_instructors()
        return render(request, self.template_name, {'instructors': featured_instructors_query})
