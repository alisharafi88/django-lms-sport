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
    'jazzmin',
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

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


CRISPY_TEMPLATE_PACK = 'bootstrap5'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.CustomUser'
INSTRUCTOR_USER_MODEL = 'instructors.Instructor'

# auth

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "apps.accounts.backends.PhoneAuthenticationBackend",
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
SMS_PATTERN_CODE = os.getenv('SMS_PATTERN_CODE')

# Jazzmin

JAZZMIN_SETTINGS = {

    "site_rtl": True,
    "language_chooser": False,

    "site_title": _("Site Management"),
    "site_header": _("Site Management"),
    "site_brand": _("Admin Panel"),
    "welcome_sign": _("Welcome to the Admin Panel"),

    "topmenu_links": [
        {"name": pgettext_lazy("Navigation", "Home"), "url": reverse_lazy("admin:index"),
         "permissions": ["auth.view_user"]},
        {"name": pgettext_lazy("Action", "Logout"), "url": reverse_lazy("admin:logout"),
         "permissions": ["auth.view_user"]},
    ],

    "font_family": "Vazir",
    "custom_css": "assets/css/persian-admin.css",

    "icons": {
        # Auth App
        "auth": "fas fa-users",
        "auth.Group": "fas fa-users",

        # Accounts App
        "accounts": "fas fa-users",
        "accounts.CustomUser": "fas fa-id-card",

        # Blogs App
        "blogs": "fas fa-book",
        "blogs.Blog": "fas fa-pen",
        "blogs.BlogComment": "fas fa-comments",

        # Courses App
        "courses": "fas fa-futbol",
        "courses.Coupon": "fas fa-ticket-alt",
        "courses.Session": "fas fa-clock",
        "courses.CourseVideo": "fas fa-video",
        "courses.Course": "fas fa-chalkboard-teacher",
        "courses.CourseMembership": "fas fa-user-check",
        "courses.CourseComments": "fas fa-comments",
        "courses.CourseLike": "fas fa-heart",

        # Contacts App
        "contacts": "fas fa-envelope",
        "contacts.ContactInfo": "fas fa-address-card",
        "contacts.Message": "fas fa-comment",

        # FAQ App
        "faq": "fas fa-question-circle",
        "faq.QuestionAnswer": "fas fa-comment-dots",

        # Instructors App
        "instructors": "fas fa-chalkboard-teacher",
        "instructors.Instructor": "fas fa-user-tie",
        "instructors.InstructorWidjet": "fas fa-tools",
        "instructors.InstructorHonor": "fas fa-award",

        # Orders App
        "orders": "fas fa-shopping-cart",
        "orders.Order": "fas fa-receipt",
        "orders.DVDOrderDetail": "fas fa-box",
        "orders.OrderItem": "fas fa-list-ul",
    },

    # UI Tweaks
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "navigation_expanded": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar": "navbar-dark bg-dark-green",
    "sidebar": "sidebar-dark bg-dark",
    "accent": "gold",
    "theme": "darkly",
}
