import os
from pathlib import Path

import environ

# Define BASE_DIR
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Initialize environment variables
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = env('DJANGO_DEBUG_STATUS')

ALLOWED_HOSTS = []


INSTALLED_APPS = [
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

    'home.apps.HomeConfig',
    'accounts.apps.AccountsConfig',
    'courses.apps.CoursesConfig',
    'blogs.apps.BlogsConfig',
    'faq.apps.FaqConfig',
    'contacts.apps.ContactsConfig',
    'instructors.apps.InstructorsConfig',
    'carts.apps.CartsConfig',
    'orders.apps.OrdersConfig',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
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
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': env('DB_USER'),
        'NAME': env('DB_NAME'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [str(BASE_DIR.joinpath('static'))]
CRISPY_TEMPLATE_PACK = 'bootstrap5'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.CustomUser'
INSTRUCTOR_USER_MODEL = 'instructors.Instructor'

INTERNAL_IPS = [
    "127.0.0.1",
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
