from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
import uuid
# Create your models here.
class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

class PizzCategory(BaseModel):
    category_name = models.CharField(max_length=120)

    def __str__(self) -> str:
        return self.category_name

class Pizza(BaseModel):
    category = models.ForeignKey(PizzCategory, on_delete=models.CASCADE, related_name='pizzas')
    pizza_name = models.CharField(max_length=100)
    price = models.IntegerField(default=100)
    pizza_img =  models.ImageField(upload_to='pizza')

    def __str__(self) -> str:
        return self.pizza_name

class Cart(BaseModel):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='cart')
    is_paid = models.BooleanField(default=False)
    instamojo_id = models.CharField(max_length=1000)
    def get_total(self):
        return CartItems.objects.filter(cart=self).aggregate(Sum('pizza__price'))['pizza__price__sum']

class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)