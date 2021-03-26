from django.urls import path
from django.views.generic import TemplateView

from shop.views import ProductListView, ReturnListView, ProductCreate, ProductUpdate, ApproveReturn, DenyReturn, OrderListView, OrderCreate, ReturnCreate

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name='home'),
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/add/", ProductCreate.as_view(), name="product-create"),
    path("products/<int:pk>/update/", ProductUpdate.as_view(), name="product-update"),
    path("products/<int:pk>/buy/", OrderCreate.as_view(), name="product-buy"),
    path("orders/", OrderListView.as_view(), name="order-list"),
    path("orders/<int:pk>/retutn/", ReturnCreate.as_view(), name="order-return"),
    path("returns/", ReturnListView.as_view(), name="return-list"),
    path("returns/<int:pk>/approve/", ApproveReturn.as_view(), name="return-approve"),
    path("returns/<int:pk>/deny/", DenyReturn.as_view(), name="return-deny"),
]
