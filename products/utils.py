import os
import random
import string

from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase+string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    qs = instance.__class__.objects.filter(slug=slug)
    if qs.exists():
        new_slug = '{}-{}'.format(slug, random_string_generator(size=4))
        return unique_slug_generator(instance, new_slug)
    return slug


def get_filename_ext(file_path):
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    return name, ext


def get_image_upload_path(instance, filename):
    name, ext = get_filename_ext(filename)
    return '{}-{}{}'.format(instance.title, name, ext)