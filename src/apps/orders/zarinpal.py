from django.conf import settings

import requests
import json

if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'payment'


ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"


def send_request(amount, description, phone, callback_url,):
    request_data = {
        "merchant_id": settings.MERCHANT,
        "amount": amount,
        "description": description,
        "callback_url": callback_url,
        "metadata": {
            "mobile": phone,
        }
    }
    request_data = json.dumps(request_data)
    request_header = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'content-length': str(len(request_data))
    }
    try:
        response = requests.post(
            ZP_API_REQUEST,
            data=request_data,
            headers=request_header,
            timeout=10
        )
        if response.status_code == 200:
            response = response.json()
            return {
                'status': True,
                'data': response['data'],
            }
        return {'status': False, 'error': 'http_error'}
    except requests.exceptions.Timeout:
        return {'status': False, 'error': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'error': 'connection_error'}


def verify(authority, amount):
    data = {
        "merchant_id": settings.MERCHANT,
        "amount": amount,
        "authority": authority,
    }
    data = json.dumps(data)
    headers = {
        'content-type': 'application/json',
        'content-length': str(len(data)),
    }
    response = requests.post(
        ZP_API_VERIFY,
        data=data,
        headers=headers
    )
    if response.status_code == 200:
        return {
            'status': True,
            'res': response.json(),
        }
    return {'status': False, 'code': 'error'}
