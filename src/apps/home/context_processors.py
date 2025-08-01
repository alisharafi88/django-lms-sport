from .models import Counter


def counter(request):
    return {
        'counter': Counter.load()
    }
