from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from phonenumber_field.formfields import SplitPhoneNumberField


class CustomUserCreationForm(UserCreationForm):
    phone_number = SplitPhoneNumberField(region='IR')

    class Meta:
        model = get_user_model()
        fields = ('username', 'phone_number',)


class CustomUserChangeForm(UserChangeForm):
    phone_number = SplitPhoneNumberField(region='IR')

    class Meta:
        model = get_user_model()
        fields = ('username', 'phone_number',)
