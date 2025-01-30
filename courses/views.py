from django.db.models import Count, Prefetch, Case, CharField, Value, When
from django.shortcuts import get_object_or_404, redirect

from django.views import generic

from courses.forms import CourseCommentForm
from courses.models import Course, CourseComments


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
            .prefetch_related(Prefetch('comments', queryset=CourseComments.objects.filter(status=True)
                                       .select_related('user', 'parent')
                                       .prefetch_related('replies__user'),
                                       ),
                              ) \
            .annotate(
            num_videos=Count('videos'),
            num_members=Count('members'),
        )

    def post(self, request, *args, **kwargs):
        coment_form = CourseCommentForm(request.POST)
        if coment_form.is_valid():
            parent_id = request.POST.get('parent_id')
            parent_comment = None
            if parent_id:
                try:
                    parent_comment = CourseComments.objects.get(id=parent_id)
                except CourseComments.DoesNotExist:
                    parent_comment = None
            new_comment = coment_form.save(commit=False)
            new_comment.course = self.get_object()
            new_comment.parent = parent_comment
            new_comment.user = self.request.user
            new_comment.save()
            return redirect('courses:course_detail', pk=self.kwargs['pk'], slug=self.kwargs['slug'])
