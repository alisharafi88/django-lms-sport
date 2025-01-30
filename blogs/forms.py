from django import forms
from django.utils.translation import gettext as _

from .models import BlogComment


class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': _('Enter your comment ...')})
        }

