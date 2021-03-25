from decimal import Decimal

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    wallet = models.DecimalField(decimal_places=2, max_digits=10, default=Decimal("1000.00"))
