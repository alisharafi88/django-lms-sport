from django.shortcuts import render
from django.views import generic

from .models import QuestionAnswer


class FAQView(generic.ListView):
    template_name = 'faq/FAQ.html'
    queryset = QuestionAnswer.objects.filter(status=True).values('question', 'answer')
    context_object_name = 'questions_answers'
