from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from ippanel import Client, Error, ResponseCode, HTTPError
import random
import logging

logger = logging.getLogger(__name__)


def send_otp_code(phone_number, code):
    try:
        client = Client(apikey=settings.SMS_API_KEY)
        phone_number_str = str(phone_number)
        pattern_code = settings.SMS_PATTERN_OTP_CODE
        sender = settings.SMS_SENDER
        response = client.send_pattern(
            pattern_code=pattern_code,
            sender=sender,
            recipient=phone_number_str,
            values={"OTP": code},
        )
        logger.info(response)
        logger.info(f"Verification code sent successfully to {phone_number}")
        return response
    except Error as e:
        logger.info("Error handled => code: %s, message: %s" % (e.code, e.message))

        if e.code == ResponseCode.ErrUnprocessableEntity.value:
            for field in e.message:
                logger.info("Field: %s , Errors: %s" % (field, e.message[field]))
    except HTTPError as e:
        logger.info("Error handled => code: %s" % (e))
    except Exception as e:
        logger.error(f"Failed to send verification code to {phone_number}: {e}")
        return None


def get_random_otp():
    return str(random.randint(100000, 999999))  # 6


def send_otp_save_session(request, phone_number, otp, expire):
    response = send_otp_code(phone_number, otp)
    if response:
        request.session['otp_code'] = otp
        request.session['phone_number'] = phone_number
        request.session['code_expiration'] = int((timezone.now() + timedelta(minutes=expire)).timestamp())
        return True
    return False
