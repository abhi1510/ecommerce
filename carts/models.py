from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, m2m_changed

from products.models import Product

User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def get_or_create_new(self, request):
        cart_id = request.session.get('cart_id', None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            is_new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated() and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            is_new_obj = True
            cart_obj = Cart.objects.create_new(user=request.user)
            request.session['cart_id'] = cart_obj.id
        return cart_obj, is_new_obj

    def create_new(self, user=None):
        return self.model.objects.create(user=user)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    products = models.ManyToManyField(Product, blank=True)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    subtotal = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)


def cart_m2m_changed_save_receiver(sender, instance, action, *args, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        products = instance.products.all()
        instance.subtotal = sum([x.price for x in products])
        instance.save()


def cart_pre_save_receiver(sender, instance, *args, **kwargs):
    instance.total = instance.subtotal + 20


pre_save.connect(cart_pre_save_receiver, sender=Cart)
m2m_changed.connect(cart_m2m_changed_save_receiver, sender=Cart.products.through)

