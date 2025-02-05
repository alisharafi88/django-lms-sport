from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.utils.translation import gettext as _

from .forms import MessageForm
from .models import ContactInfo


class ContactView(View):
    def get(self, request):
        primary_contactinfo = ContactInfo.objects.filter(is_primary=True).first()
        message_form = MessageForm()

        context = {
            'contact_info': primary_contactinfo,
            'message_form': message_form,
        }

        return render(request, 'contact/contact.html', context)

    def post(self, request):
        if request.user.is_authenticated:
            form = MessageForm(request.POST)
            if form.is_valid():
                new_message = form.save(commit=False)
                new_message.user = request.user
                new_message.save()
                messages.success(request, _('Your message sent successfully!'), 'success')
                return redirect(request.META.get('HTTP_REFERER', 'contact:contact'))
            messages.error(request, _('Your message was not sent, please try again.'), 'danger')
            return redirect(request.META.get('HTTP_REFERER', 'contact:contact'))
        messages.warning(request, _('You should be authenticated.'), 'warning')
        return redirect(request.META.get('HTTP_REFERER', 'contact:contact'))

