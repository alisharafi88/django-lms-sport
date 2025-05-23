from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

    path('about/', views.AboutUsView.as_view(), name='about_us'),

    path('BMI/', views.BMIView.as_view(), name='BMI'),

    path('pishro/', views.PishroView.as_view(), name='pishro')
]
