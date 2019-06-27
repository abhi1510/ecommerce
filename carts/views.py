from django.shortcuts import render, redirect

from .models import Cart
from products.models import Product


def cart_home(request):
    cart_obj, is_new = Cart.objects.get_or_create_new(request)
    return render(request, 'carts/home.html', context={'cart': cart_obj})


def cart_update(request):
    product_id = request.POST.get('product_id')
    product_obj = Product.objects.get(id=product_id)
    cart_obj, is_new = Cart.objects.get_or_create_new(request)
    if product_obj in cart_obj.products.all():
        cart_obj.products.remove(product_obj)
    else:
        cart_obj.products.add(product_obj)
    request.session['cart_items'] = cart_obj.products.count()
    return redirect('cart:home')
