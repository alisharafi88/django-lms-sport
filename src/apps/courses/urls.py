from django.urls import path, re_path

from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course_list',),
    re_path(r'^course/(?P<slug>[\w-]+)/$', views.CourseDetailView.as_view(), name='course_detail'),
    re_path(r'^package/(?P<slug>[\w-]+)/$', views.PackageDetailView.as_view(), name='package_detail'),
    path('<int:pk>/', views.StudentCourseCommentsView.as_view(), name='course_add_comment',),
]
