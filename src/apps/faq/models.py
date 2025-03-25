from django.db import models
from django.utils.translation import gettext_lazy as _

from django_ckeditor_5.fields import CKEditor5Field


class QuestionAnswer(models.Model):
    question = models.CharField(_('question'), max_length=150)
    answer = CKEditor5Field(_('answer'))

    slug = models.SlugField(_('slug'))

    date_created = models.DateTimeField(_('date created'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    status = models.BooleanField(_('status'), default=True)

    class Meta:
        ordering = ('date_modified',)

        verbose_name = _('question and answer')
        verbose_name_plural = _('questions and answers')
