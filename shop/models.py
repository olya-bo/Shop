from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to="products", blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name}'


class Order(models.Model):
    customer = models.ForeignKey("authorization.User", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} {self.product}"


class Return(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order} {self.created_at}"
