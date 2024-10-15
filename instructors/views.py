from django.db.models import Prefetch
from django.shortcuts import render
from django.views import generic

from instructors.models import Instructor, InstructorHonor
from instructors.queries import get_all_instructor, get_instructor_by_id_slug


class InstructorListView(generic.ListView):
    template_name = 'instructors/instructor_list.html'
    context_object_name = 'instructors'
    queryset = get_all_instructor()


class InstructorDetailView(generic.DetailView):
    template_name = 'instructors/instructor_detail.html'
    context_object_name = 'instructor'

    def get_queryset(self):
        return get_instructor_by_id_slug(self.kwargs['pk'], self.kwargs['slug'])
