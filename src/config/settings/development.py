import os
import socket
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEBUG = True


# For Docker
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
    '0.0.0.0',
    '172.17.0.1',  # Docker default gateway
]

hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS += [ip for ip in ips]

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ["*"]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': os.getenv('DB_USER'),
        'NAME': os.getenv('DB_NAME'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0

# static
STATICFILES_DIRS = [str(BASE_DIR.joinpath('static'))]
