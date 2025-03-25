from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ContactsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.contacts'
    verbose_name = _('Contacts')

    def ready(self):
        import apps.contacts.signals
