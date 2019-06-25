from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save

from .utils import get_image_upload_path, unique_slug_generator


class ProductManager(models.Manager):

    def featured(self):
        return self.get_queryset().filter(featured=True)


class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20)
    image = models.ImageField(upload_to=get_image_upload_path, null=True, blank=True)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)

    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)
