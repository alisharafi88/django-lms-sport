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
from ..instructors.models import Instructor


class CourseListView(generic.ListView):
    model = Course
    template_name = 'packages/courses_list.html'
    paginate_by = 3
    context_object_name = 'products'

    def get_queryset(self):
        course_content_type = ContentType.objects.get_for_model(Course)
        package_content_type = ContentType.objects.get_for_model(Package)
        default_avatar_url = staticfiles_storage.url('assets/img/avatar/default-avatar-icon.jpg')

        # Queryset for courses
        courses_queryset = Course.objects.filter(status=True).annotate(
            coach_profile=Case(
                    When(
                        coach__user__profile_photo__isnull=False,
                        then=Concat(
                            Value(settings.MEDIA_URL),
                            F("coach__user__profile_photo"),
                            output_field=CharField(),
                        ),
                    ),
                    default=Value(default_avatar_url),
                    output_field=CharField(),
                ),
            num_members=Count('memberships', filter=Q(memberships__content_type=course_content_type), distinct=True),
            num_videos=Count('seasons__videos'),
            product_type=Value(1, output_field=IntegerField()),  # 1 = course
            num_courses=Value(0, output_field=IntegerField()),
            discounted_price=F('price') - F('discount_amount'),
            avg_rate=Avg('comments__rate', default=0),
            num_comment=Count('comments', distinct=True),
        ).values(
            'id', 'title', 'coach_profile', 'num_members', 'num_videos', 'product_type',
            'num_courses', 'discounted_price', 'avg_rate', 'num_comment', 'date_created', 'date_modified', 'img'
        )

        # Queryset for packages
        packages_queryset = Package.objects.filter(status=True).annotate(
            coach_profile=Value(None, output_field=CharField()),
            num_members=Count('memberships', filter=Q(memberships__content_type=package_content_type), distinct=True),
            num_videos=Value(0, output_field=IntegerField()),
            product_type=Value(2, output_field=IntegerField()),  # 2 = package
            num_courses=Count('courses'),
            discounted_price=F('price') - F('discount_amount'),
            avg_rate=Avg('courses__comments__rate', default=0),
            num_comment=Count('courses__comments', distinct=True),
        ).values(
            'id', 'title', 'coach_profile', 'num_members', 'num_videos', 'product_type',
            'num_courses', 'discounted_price', 'avg_rate', 'num_comment', 'date_created', 'date_modified', 'img'
        )

        # Combine the querysets
        combined_queryset = courses_queryset.union(packages_queryset, all=True).order_by('-date_created', '-date_modified')
        return combined_queryset


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
