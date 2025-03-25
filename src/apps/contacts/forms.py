from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('text',)
        widget = {
            'text': forms.Textarea(attrs={'placeholder': _('Enter Your Message')})
        }
