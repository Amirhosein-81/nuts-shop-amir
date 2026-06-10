from django.utils.text import slugify
import unicodedata
import re

def unique_slugify(instance, value, slug_field_name='slug'):
    """
    Creates a unique slug for a model instance.
    """
    slug_field = getattr(instance, slug_field_name)
    slug = slugify(value)

    # ensure slug is not empty (for Persian titles)
    if not slug:
        slug = re.sub(r'\s+', '-', value.strip())

    ModelClass = instance.__class__
    unique_slug = slug
    counter = 2

    while ModelClass.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{slug}-{counter}"
        counter += 1

    return unique_slug
