from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CartsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.carts'
    verbose_name = _('Carts')
