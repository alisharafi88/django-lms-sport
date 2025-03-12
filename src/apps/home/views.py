from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from .queries import get_latest_blogs, get_top_comment
from ..carts.carts import Cart
from ..courses.queries import get_combined_course_package_queryset
from ..instructors.queries import get_all_instructor


class HomeView(View):
    template_name = 'home/home.html'

    def get(self, request):
        top_courses_query = get_combined_course_package_queryset()[:6]
        top_instructors_query = get_all_instructor()[:3]
        latest_blogs_query = get_latest_blogs()
        top_course_comment = get_top_comment()

        cart = Cart(request)
        cart_items = [(item['id'], item['type']) for item in cart.cart]

        return render(
            request,
            self.template_name,
            {
                'products': top_courses_query,
                'instructors': top_instructors_query,
                'blogs': latest_blogs_query,
                'comments': top_course_comment,
                'carts': cart_items,
            }
        )


class AboutUsView(View):
    template_name = 'home/aboutus.html'

    def get(self, request):
        top_instructors_query = get_all_instructor()[:3]
        top_course_comment = get_top_comment()
        return render(
            request,
            self.template_name,
            {
                'instructors': top_instructors_query,
                'comments': top_course_comment,
            }
        )


class BMIView(TemplateView):
    template_name = 'BMI/BMI.html'
