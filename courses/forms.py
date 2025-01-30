from django import forms
from django.utils.translation import gettext as _

from courses.models import CourseComments


class CourseCommentForm(forms.ModelForm):
    class Meta:
        model = CourseComments
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': _('Enter your comment ...')})
        }

