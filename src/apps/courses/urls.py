from django.urls import path

from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course_list',),
    path('course/<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('package/<slug:slug>/', views.PackageDetailView.as_view(), name='package_detail'),
    path('<int:pk>/', views.StudentCourseCommentsView.as_view(), name='course_add_comment',),
]
