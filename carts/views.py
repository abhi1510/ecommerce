from django.shortcuts import render, redirect

from .models import Cart
from products.models import Product


def cart_home(request):
    cart_obj, is_new = Cart.objects.get_or_create_new(request)
    return render(request, 'carts/home.html', context={})


def cart_update(request):
    product_id = 1
    product_obj = Product.objects.get(id=product_id)
    cart_obj, is_new = Cart.objects.get_or_create_new(request)
    cart_obj.products.add(product_obj)
    return redirect(product_obj.get_absolute_url())
