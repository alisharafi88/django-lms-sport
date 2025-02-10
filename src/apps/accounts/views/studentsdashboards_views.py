from django.db.models import Subquery
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.carts.carts import Cart
from apps.courses.models import Course


class StudentsDashboard(LoginRequiredMixin, View):
    template_name = 'accounts/dashboards/student_dashboard.html'
    
    def get(self, request):
        # Student Courses
        courses_queryset = Course.objects.filter(members__user=request.user.id, status=True)

        # Cart
        cart = Cart(request)
        total_price, total_discounted_price = cart.get_total_price()

        context = {
            # Cart
            'carts': cart,
            'total_price': total_price,
            'total_discounted_price': total_discounted_price,

            # Student Courses
            'courses': courses_queryset,
        }

        return render(
            request,
            self.template_name,
            context,
        )
