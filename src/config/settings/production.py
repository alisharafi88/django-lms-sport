import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# === DEBUG ===
DEBUG = False

# === ALLOWED_HOSTS ===
ALLOWED_HOSTS = [
    'wizardly-thompson-6zjh0x5fw0.liara.run',
    'fastball.ir',
    'www.fastball.ir',
]

# === Database ===
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}

# === Security ===
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

STATICFILES_DIRS = [str(BASE_DIR.joinpath('static'))]


# === Faraz sms ===
SANDBOX = True
