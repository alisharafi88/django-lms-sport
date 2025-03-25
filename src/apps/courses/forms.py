from django import forms
from django.utils.translation import gettext_lazy as _

from .models import CourseComments


class CourseCommentForm(forms.ModelForm):
    class Meta:
        model = CourseComments
        fields = ['text', 'rate']
        widgets = {
            'text': forms.Textarea(attrs={
                'placeholder': _('Write your feedback here...'),
                'rows': 4,
                'cols': 40
            }),
        }
        labels = {
            'text': _('Feedback'),
            'rate': _('Rating'),
        }
        help_texts = {
            'text': _('Please provide constructive feedback.'),
        }
        error_messages = {
            'rate': {
                'required': _('Please select a rating.'),
            },
            'text': {
                'required': _('Please enter your feedback.'),
            },
        }
