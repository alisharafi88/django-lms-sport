from datetime import timedelta, datetime

from django.contrib.auth.views import LogoutView
from django.http import HttpResponseNotAllowed
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.utils.translation import gettext_lazy as _

import logging

from ..sms_api import get_random_otp, send_otp_save_session
from ..forms import AthenticationForm, VerificationForm
from ..models import CustomUser
User = CustomUser

logger = logging.getLogger(__name__)

CODE_EXPIRATION_MINUTES = 2


class AuthenticationView(View):
    form_class = AthenticationForm
    template_name = 'accounts/authentication.html'

    def get(self, request):
        logger.debug('Rendering authentication form.')
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        logger.debug('Handling authentication form submission.')
        form = self.form_class(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            otp = get_random_otp()
            logger.info(f'Generated OTP {otp} for phone number {phone_number}.')

            if self.process_user(phone_number, otp, request):
                request.session['otp_code'] = otp # delete it
                request.session['phone_number'] = phone_number # delete it
                request.session['code_expiration'] = int((timezone.now() + timedelta(minutes=CODE_EXPIRATION_MINUTES)).timestamp()) # delete it
                messages.success(request, 'Verification code sent successfully.', 'success')
                logger.info(f'OTP sent successfully to {phone_number}.')
                return redirect('accounts:verify_otp')
            else:
                messages.error(request, 'Failed to send verification code. Please try again.', 'error')
                logger.error(f'Failed to send OTP to {phone_number}.')

        return render(request, self.template_name, {'form': form})

    def process_user(self, phone_number, otp, request):
        try:
            user = User.objects.get(phone_number=phone_number)
            print(user.phone_number)
            logger.info(f'User found for phone number {phone_number}.')
            return True
            # return send_otp_save_session(request, phone_number, otp, CODE_EXPIRATION_MINUTES)
        except User.DoesNotExist:
            user = User.objects.create_user(phone_number=phone_number)
            user.is_active = False
            user.save()
            logger.info(f'Created new user for phone number {phone_number}.')
            # return send_otp_save_session(request, phone_number, otp, CODE_EXPIRATION_MINUTES)
            return True
        except Exception as e:
            logger.error(f'Error processing user with phone number {phone_number}: {e}')
            return False


class VerifyOTPView(View):
    template_name = 'accounts/verification_otp.html'
    form_class = VerificationForm

    def get(self, request):
        logger.debug('Rendering OTP verification form.')
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        logger.debug('Handling OTP verification form submission.')
        form = self.form_class(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            stored_otp = request.session.get('otp_code')
            phone_number = request.session.get('phone_number')
            code_expiration = timezone.make_aware(datetime.fromtimestamp(request.session['code_expiration']))

            if not stored_otp or not phone_number or not code_expiration:
                messages.error(request, 'Verification process not initiated or session expired.')
                logger.warning('Session data missing or expired during OTP verification.')
                return render(request, self.template_name, {'form': form})

            if timezone.now() > code_expiration:
                messages.error(request, 'The verification code has expired.')
                logger.warning(f'OTP expired for phone number {phone_number}.')
                return render(request, self.template_name, {'form': form})

            if otp == stored_otp:
                try:
                    user = User.objects.get(phone_number=phone_number)
                    user.is_active = True
                    user.save()
                    del request.session['otp_code']
                    del request.session['phone_number']
                    del request.session['code_expiration']
                    messages.success(request, 'Your phone number has been verified successfully.')
                    logger.info(f'Phone number {phone_number} verified successfully.')
                    return redirect('home:home')
                except User.DoesNotExist:
                    messages.error(request, 'User  does not exist.')
                    logger.error(f'User  does not exist for phone number {phone_number}.')
            else:
                messages.error(request, 'Invalid verification code.')
                logger.warning(f'Invalid OTP entered for phone number {phone_number}., otp: {stored_otp} {type(stored_otp)}, sent otp : {otp} {type(otp)}')

        return render(request, self.template_name, {'form': form})


class ResendOTPView(View):
    def post(self, request):
        phone_number = request.session.get('phone_number')
        if not phone_number:
            messages.error(request, 'Session expired. Please start the verification process again.')
            logger.warning('Attempted to resend OTP with expired session.')
            return redirect('authentication')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home:home')

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() != 'post':
            return HttpResponseNotAllowed(['POST'])

        messages.success(request, _('You have been successfully logged out.'))
        return super().dispatch(request, *args, **kwargs)
