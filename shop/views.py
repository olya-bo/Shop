from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from shop.models import Product, Order, Return


class SuperuserRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated and not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class ProductListView(ListView):
    model = Product
    paginate_by = 100


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    paginate_by = 100

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        queryset = queryset.filter(customer=self.request.user)
        return queryset


class OrderCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Order
    fields = ["quantity"]
    success_url = reverse_lazy("order-list")
    success_message = "Product purchased"
    template_name = "shop/product_buy.html"

    def get_product_obj(self):
        return get_object_or_404(Product, pk=self.kwargs.get("pk"))

    def get(self, request, *args, **kwargs):
        self.product_obj = self.get_product_obj()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.product_obj = self.get_product_obj()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product = self.product_obj
        return super().form_valid(form)


class ProductCreate(SuperuserRequiredMixin, SuccessMessageMixin, CreateView):
    model = Product
    fields = ['name', "description", 'price', 'image', 'amount', ]
    success_url = reverse_lazy("product-list")
    success_message = "Product created"


class ProductUpdate(SuperuserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    fields = ['name', "description", 'price', 'image', 'amount', ]
    success_url = reverse_lazy("product-list")
    success_message = "Product updated"


class ReturnListView(SuperuserRequiredMixin, ListView):
    model = Return
    paginate_by = 100


class ReturnCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Return
    fields = []
    success_url = reverse_lazy("return-list")
    success_message = "Return created"

    def get_order_obj(self):
        return get_object_or_404(Order, pk=self.kwargs.get("pk"))

    def get(self, request, *args, **kwargs):
        self.order_obj = self.get_order_obj()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.order_obj = self.get_order_obj()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.order = self.order_obj
        return super().form_valid(form)


class DenyReturn(SuperuserRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Return
    success_url = reverse_lazy("return-list")
    template_name_suffix = '_confirm_deny'
    success_message = "Return denied"


class ApproveReturn(SuperuserRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Return
    success_url = reverse_lazy("return-list")
    template_name_suffix = '_confirm_approve'
    success_message = "Return approved"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        order_obj = obj.order
        product_obj = order_obj.product

        product_obj.amount += order_obj.quantity
        product_obj.save()

        response = super(ApproveReturn, self).delete(request, *args, **kwargs)

        order_obj.delete()

        return response
