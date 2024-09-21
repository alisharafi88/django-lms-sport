from django.db.models import Prefetch
from django.shortcuts import render
from django.views import generic

from instructors.models import Instructor, InstructorHonor


class InstructorListView(generic.ListView):
    template_name = 'instructors/instructor_list.html'
    context_object_name = 'instructors'
    queryset = Instructor.objects.select_related('user').all()

    def get_queryset(self):
        return Instructor.objects.select_related('user').filter(status=True)


class InstructorDetailView(generic.DetailView):
    template_name = 'instructors/instructor_detail.html'
    context_object_name = 'instructor'
    queryset = Instructor.objects.all()

    def get_queryset(self):
        return Instructor \
            .objects \
            .filter(
            pk=self.kwargs['pk'],
            slug=self.kwargs['slug'],
            status=True
        ) \
            .select_related('user')\
            .prefetch_related('widjets', Prefetch('honors', queryset=InstructorHonor.objects.filter(status=True)))
