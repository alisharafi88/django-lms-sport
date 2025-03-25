from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Order


class CheckoutForm(forms.Form):
    status = forms.ChoiceField(label='Shipping', choices=Order.AccessStatus.choices, initial=Order.AccessStatus.ONLINE, widget=forms.RadioSelect)
    shipping_city = forms.CharField(label='Shipping', required=False)
    shipping_address = forms.CharField(label='Shipping Address', required=False)
    first_name = forms.CharField(label='First Name', required=False)
    last_name = forms.CharField(label='Last Name', required=False)
    postal_code = forms.CharField(label='Postal Code', required=False)
    phone_number = forms.CharField(label='Phone Number', required=False)
    email = forms.EmailField(label='Email Address', required=False)
    order_note = forms.CharField(max_length=500, required=False, widget=forms.Textarea)

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        shipping_city = cleaned_data.get('shipping_city')
        shipping_address = cleaned_data.get('shipping_address')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        postal_code = cleaned_data.get('postal_code')
        phone_number = cleaned_data.get('phone_number')
        email = cleaned_data.get('email')

        if status == Order.AccessStatus.DVD:
            if not shipping_address:
                self.add_error('shipping_address', _('Please enter a shipping address'))
            if not shipping_city:
                self.add_error('shipping_city', _('Please enter a shipping city'))
            if not first_name:
                self.add_error('first_name', _('Please enter your first name'))
            if not last_name:
                self.add_error('last_name', _('Please enter your last name'))
            if not phone_number:
                self.add_error('phone_number', _('Please enter your phone number'))
            if not email:
                self.add_error('email', _('Please enter your email'))
            if not postal_code:
                self.add_error('postal_code', _('Please enter your postal code'))
        return cleaned_data
