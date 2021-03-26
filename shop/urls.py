from django.urls import path
from django.views.generic import TemplateView

from shop.views import ProductListView, ReturnListView, ProductCreate

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name='home'),
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/add/", ProductCreate.as_view(), name="product-create"),
    path("returns/", ReturnListView.as_view(), name="return-list"),
]
