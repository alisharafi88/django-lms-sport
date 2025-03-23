from .models import ContactInfo


def primary_contact(request):
    try:
        contact = ContactInfo.objects.filter(is_primary=True).first()
    except ContactInfo.DoesNotExist:
        contact = None
    return {
        'primary_contact': contact
    }
