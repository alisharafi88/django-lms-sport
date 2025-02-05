from django import forms

from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('text',)
        widget = {
            'text': forms.Textarea(attrs={'placeholder': 'Enter Your Message'})
        }
