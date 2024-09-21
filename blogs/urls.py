from django.urls import path

from blogs import views

app_name = 'blogs'

urlpatterns = [
    path('', views.PostListView.as_view(), name='blog_list'),
    path('<int:pk>/<slug:slug>/', views.PostDetailView.as_view(), name='blog_detail')
]
