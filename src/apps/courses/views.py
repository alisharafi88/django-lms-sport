from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Prefetch, Case, CharField, Value, When
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic, View
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from .forms import CourseCommentForm
from .models import Course, CourseComments, CourseMembership


class CourseListView(generic.ListView):
    model = Course
    template_name = 'courses/courses_list.html'
    paginate_by = 3
    context_object_name = 'courses'

    def get_queryset(self):
        queryset_courses = Course.objects.filter(status=True).annotate(num_members=Count('members'),
                                                                       num_videos=Count('videos'),
                                                                       type=Case(
                                                                           When(parent__isnull=False,
                                                                                then=Value('package')),
                                                                           default=Value('course'),
                                                                           output_field=CharField(),
                                                                       ),
                                                                       num_courses=Count('parent'),
                                                                       )

        return queryset_courses


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['comment_form'] = CourseCommentForm()
        return context

    def get_queryset(self, queryset=None):
        course = get_object_or_404(Course, pk=self.kwargs['pk'], slug=self.kwargs['slug'])

        return Course.objects.filter(pk=course.pk) \
            .select_related('instructor__user', ) \
            .prefetch_related(
            Prefetch(
                'comments',
                queryset=CourseComments.objects.filter(status=True).select_related('user')
            )
        ) \
            .annotate(
            num_videos=Count('videos'),
            num_members=Count('members'),
        )

    def post(self, request, *args, **kwargs):
        coment_form = CourseCommentForm(request.POST)
        if coment_form.is_valid():
            new_comment = coment_form.save(commit=False)
            new_comment.course = self.get_object()
            new_comment.user = self.request.user
            new_comment.save()
            return redirect('courses:course_detail', pk=self.kwargs['pk'], slug=self.kwargs['slug'])


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
