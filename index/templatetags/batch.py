from django.template import Library

register = Library()

@register.filter
def batch(iterable, n):
    """Batch an iterable into chunks of size n."""
    iterable = list(iterable)  # Ensure the iterable is a list
    for i in range(0, len(iterable), n):
        yield iterable[i:i + n]
