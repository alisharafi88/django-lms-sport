import os

DEBUG = True
# For Docker
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]
if DEBUG:
    import socket

    hostname, i, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + '1' for ip in ips]
    INTERNAL_IPS += ['172.17.0.1']  # Docker default gateway

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
