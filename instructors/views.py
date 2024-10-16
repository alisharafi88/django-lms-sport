from django.views import generic

from .queries import get_all_instructor, get_instructor_by_id_slug
from .utils import get_master_instructor_social_media


class InstructorListView(generic.ListView):
    template_name = 'instructors/instructor_list.html'
    context_object_name = 'instructors'
    queryset = get_all_instructor()


class InstructorDetailView(generic.DetailView):
    template_name = 'instructors/instructor_detail.html'
    context_object_name = 'instructor'

    def get_queryset(self):
        return get_instructor_by_id_slug(self.kwargs['pk'], self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(InstructorDetailView, self).get_context_data(**kwargs)

        master_social_media = get_master_instructor_social_media()
        if master_social_media:
            context.update(master_social_media)
        return context
