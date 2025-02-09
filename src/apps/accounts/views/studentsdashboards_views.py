from django.db.models import Subquery
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.courses.models import Course, CourseLike


class StudentsDashboard(LoginRequiredMixin, View):
    template_name = 'accounts/dashboards/student_dashboard.html'
    
    def get(self, request):
        liked_course_queryset = Course.objects.filter(id__in=Subquery(CourseLike.objects.filter(user_id=request.user.id).values('course')))

        context = {
            'liked_courses': liked_course_queryset,
        }

        return render(
            request,
            self.template_name,
            context,
        )
