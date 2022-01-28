# Create your models here.

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
from accounts.models import User
from products.models import ProductReal


class CartItem(models.Model):
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.id}, {self.product_real}"

    reg_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_real = models.ForeignKey(ProductReal, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField('수량', default=1,
                                                validators=[MinValueValidator(1), MaxValueValidator(100)])
