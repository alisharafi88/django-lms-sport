from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.staticfiles.storage import staticfiles_storage
from django.db.models import Count, Prefetch, Case, CharField, Value, When, IntegerField, Q, ExpressionWrapper, F, Avg
from django.db.models.functions import Cast, Coalesce, Concat
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic, View
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from itertools import chain

from .forms import CourseCommentForm
from .models import Course, CourseComments, CourseMembership, Package, CourseSeason, CourseVideo
from .queries import get_combined_course_package_queryset
from ..carts.carts import Cart
from ..instructors.models import Instructor


class CourseListView(generic.ListView):
    model = Course
    template_name = 'packages/courses_list.html'
    paginate_by = 3
    context_object_name = 'products'

    def get_queryset(self):
        search = self.request.GET.get('search')
        queryset = get_combined_course_package_queryset(search)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        cart = Cart(self.request)
        cart_items = [(item['id'], item['type']) for item in cart.cart]
        context['carts'] = cart_items

        return context


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'packages/course_detail.html'
    context_object_name = 'course'

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset \
            .filter(
                status=True,
            ) \
            .select_related(
                'coach__user',
            ) \
            .prefetch_related(
                Prefetch(
                    'comments',
                    queryset=CourseComments.objects.filter(status=True).select_related('user'),
                ), Prefetch(
                    'seasons',
                    CourseSeason.objects.prefetch_related(
                        'videos',
                    )
                ), Prefetch(
                    'coach__courses',
                    queryset=Course.objects.filter(
                        status=True
                    ).annotate(
                        num_videos=Count('seasons__videos'),
                        num_members=Count(
                            'memberships',
                            filter=Q(memberships__content_type=ContentType.objects.get_for_model(Course)),
                            distinct=True
                        ),
                        avg_rate=Avg('comments__rate', default=0)

                    ).prefetch_related('comments')

                )
            ) \
            .annotate(
                num_videos=Count('seasons__videos'),
                num_members=Count('memberships', distinct=True),
                avg_rate=Avg('comments__rate', default=0)
            ) \
            .prefetch_related(

            )

        return queryset


class PackageDetailView(generic.DetailView):
    model = Package
    template_name = 'packages/package_detail.html'
    context_object_name = 'package'

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset \
            .filter(
                status=True,
            ) \
            .annotate(
                num_courses=Count('courses', distinct=True),
                num_members=Count('memberships'),
                num_videos=Count('courses__seasons__videos')
            ) \
            .prefetch_related(
                Prefetch(
                  'courses',
                  queryset=Course.objects.prefetch_related(
                      Prefetch(
                          'seasons',
                          CourseSeason.objects.prefetch_related(
                                  'videos',
                          )
                      )
                  )
                ),
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['coaches'] = Instructor.objects.filter(courses__in=self.object.courses.all()).select_related('user').distinct()
        return context


class StudentCourseCommentsView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=self.kwargs['pk'])

        if not CourseMembership.objects.filter(user=request.user, course=course).exists():
            return JsonResponse({
                'success': False,
                'message': _('You must be enrolled in this course to submit a comment.')
            }, status=403)

        comment_form = CourseCommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.course = course
            new_comment.save()

            return JsonResponse({
                'success': True,
                'message': _('Your comment has been submitted successfully!')
            })

        return JsonResponse({
            'success': False,
            'errors': comment_form.errors
        }, status=400)
