from django.urls import path

from faq import views

app_name = 'faq'

urlpatterns = [
    path('', views.FAQView.as_view(), name='question_answer'),
]
