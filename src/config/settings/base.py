from django.urls import reverse_lazy
from django.utils.translation import pgettext_lazy
from django.utils.translation import gettext_lazy as _

import os
from pathlib import Path

# Define BASE_DIR

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_DIR = BASE_DIR.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

INSTALLED_APPS = [
    # 'jazzmin',
    'admin_confirm',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'phonenumber_field',
    'debug_toolbar',
    'django_ckeditor_5',
    'django_seed',
    'widget_tweaks',
    'jalali_date',
    'django_cleanup.apps.CleanupConfig',

    'apps.home.apps.HomeConfig',
    'apps.accounts.apps.AccountsConfig',
    'apps.courses.apps.CoursesConfig',
    'apps.blogs.apps.BlogsConfig',
    'apps.faq.apps.FaqConfig',
    'apps.contacts.apps.ContactsConfig',
    'apps.instructors.apps.InstructorsConfig',
    'apps.carts.apps.CartsConfig',
    'apps.orders.apps.OrdersConfig',
    'apps.utils.apps.UtilsConfig',
    'apps.tickets.apps.TicketsConfig'
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # Local
                'apps.contacts.context_processors.primary_contact',
                'apps.home.context_processors.counter',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization

LANGUAGE_CODE = 'fa'
TIME_ZONE = 'Asia/Tehran'

USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
    os.path.join(ROOT_DIR, 'locale'),
]
# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

CRISPY_TEMPLATE_PACK = 'bootstrap5'
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.CustomUser'
INSTRUCTOR_USER_MODEL = 'instructors.Instructor'

# auth

AUTHENTICATION_BACKENDS = [
    "apps.accounts.backends.PhoneAuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# ckeditor

customColorPalette = [
    {
        'color': 'hsl(4, 90%, 58%)',
        'label': 'Red'
    },
    {
        'color': 'hsl(340, 82%, 52%)',
        'label': 'Pink'
    },
    {
        'color': 'hsl(291, 64%, 42%)',
        'label': 'Purple'
    },
    {
        'color': 'hsl(262, 52%, 47%)',
        'label': 'Deep Purple'
    },
    {
        'color': 'hsl(231, 48%, 48%)',
        'label': 'Indigo'
    },
    {
        'color': 'hsl(207, 90%, 54%)',
        'label': 'Blue'
    },
]

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading', '|', 'bold', 'italic', 'link', 'bulletedList', 'numberedList', 'blockQuote', 'imageUpload',
            '|', 'fontSize', 'fontColor', 'highlight',
        ],

    },
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3',
            '|',
            'bulletedList', 'numberedList',
            '|',
            'blockQuote',
        ],
        'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
                    'code', 'subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing', 'insertImage',
                    'bulletedList', 'numberedList', 'todoList', '|', 'blockQuote', 'imageUpload', '|',
                    'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
                    'insertTable', ],
        'image': {
            'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
                        'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side', '|'],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ]

        },
        'table': {
            'contentToolbar': ['tableColumn', 'tableRow', 'mergeTableCells',
                               'tableProperties', 'tableCellProperties'],
            'tableProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            },
            'tableCellProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            }
        },
        'heading': {
            'options': [
                {'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph'},
                {'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1'},
                {'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2'},
                {'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3'}
            ]
        }
    },
    'list': {
        'properties': {
            'styles': 'true',
            'startIndex': 'true',
            'reversed': 'true',
        },
        'fontSize': {
            'options': [
                'tiny',
                'small',
                'big',
                'huge'
            ]
        },
        'fontColor': {
            'colors': [
                {
                    'color': 'hsl(4, 90%, 58%)',
                    'label': 'Red'
                },
                {
                    'color': 'hsl(340, 82%, 52%)',
                    'label': 'Pink'
                },
                ...
            ]
        },
        'highlight': {
            'options': [
                {
                    'model': 'yellowMarker',
                    'class': 'marker-yellow',
                    'title': 'Yellow marker',
                    'color': 'var(--ck-highlight-marker-yellow)',
                    'type': 'marker'
                },
                ...
            ]
        },
    }
}
CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_5_CUSTOM_CSS = 'assets/css/ckeditor_custom.css'

# logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# SMS Provider API

SMS_API_KEY = os.getenv('SMS_API_KEY')
SMS_SENDER = os.getenv('SMS_SENDER')
SMS_PATTERN_OTP_CODE = os.getenv('SMS_PATTERN_CODE')

# Zarinpal
MERCHANT = os.getenv('MERCHANT')

# Jalali date

JALALI_DATE_DEFAULTS = {
    'LIST_DISPLAY_AUTO_CONVERT': True,
    'Strftime': {
        'date': '%Y/%m/%d',
        'datetime': '%Y/%m/%d , %H:%M:%S',
    },
    'Static': {
        'js': [
            'admin/js/django_jalali.min.js',
        ],
        'css': {
            'all': [
                'assets/css/persian-admin.css',
            ]
        }
    },
}

# Login
LOGIN_URL = '/accounts/authenticate/'
