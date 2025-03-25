from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('phone_number',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('phone_number',)


class AthenticationForm(forms.Form):
    phone_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': _('Enter your phone number')}))

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        phone_number = phone_number.strip()

        if phone_number.startswith('0'):
            phone_number = phone_number[1:]
        if phone_number.startswith('98'):
            phone_number = '+' + phone_number
        elif not phone_number.startswith('+98'):
            phone_number = '+98' + phone_number

        if len(phone_number) != 13:
            raise ValidationError(_('Invalid Iranian phone number.'))
        return phone_number


class VerificationForm(forms.Form):
    otp = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'placeholder': _('Enter OTP')}))


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('profile_photo', 'first_name', 'last_name', 'email', 'phone_number', 'bio')
        readonly_fields = ('phone_number',)
        labels = {
            'profile_photo': _('Profile Picture'),
        }
