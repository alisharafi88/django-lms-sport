from django.urls import path, re_path

from . import views

app_name = 'instructors'
urlpatterns = [
    path('', views.InstructorListView.as_view(), name='instructor_list',),
    re_path(r'^instructors/(?P<pk>[0-9]+)/(?P<slug>[\w-]+)/$', views.InstructorDetailView.as_view(), name='instructor_detail'),
]
