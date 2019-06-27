from django.views.generic import ListView, DetailView


from .models import Product
from carts.models import Cart


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'products/list.html'


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'products/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        cart_obj, is_new = Cart.objects.get_or_create_new(self.request)
        context['cart'] = cart_obj
        return context
