from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import ContactInfo


@receiver(pre_save, sender=ContactInfo)
def ensure_single_primary(sender, instance, **kwargs):
    if instance.is_primary:
        ContactInfo.objects.filter(is_primary=True).exclude(pk=instance.pk).update(is_primary=False)
