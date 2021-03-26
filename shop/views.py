from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from shop.models import Product, Return


class ProductListView(ListView):
    model = Product
    paginate_by = 100


class ReturnListView(ListView):
    model = Return
    paginate_by = 100


class ProductCreate(CreateView):
    model = Product
    fields = ['name', "description", 'price', 'image', ]
    success_url = reverse_lazy("product-list")
