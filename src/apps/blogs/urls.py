from django.urls import path, re_path

from . import views

app_name = 'blogs'

urlpatterns = [
    path('', views.PostListView.as_view(), name='blog_list'),
    re_path(r'^(?P<pk>[0-9]+)/(?P<slug>[\w-]+)/$', views.PostDetailView.as_view(), name='blog_detail')
]
