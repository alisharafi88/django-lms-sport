from django.conf import settings

from apps.utils.numbers.convert_numbers import PersianNumberConverter


class PersianNumberMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.enabled = getattr(settings, 'PERSIAN_NUMBERS_ENABLED', False)

    def __call__(self, request):
        response = self.get_response(request)

        if self.enabled and response.status_code == 200 and 'text/html' in response.get('Content-Type', ''):
            content = response.content.decode('utf-8')
            response.content = PersianNumberConverter.to_persian(content).encode('utf-8')

        return response
