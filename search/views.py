from django.shortcuts import render
from django.views.generic import ListView

from products.models import Product

class SearchProductView(ListView):
    queryset = Product.objects.all()
    template_name = 'products/list.html'
