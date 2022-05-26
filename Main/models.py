from django.contrib.auth.models import AbstractUser
from django.db import models


# ToDO  карточки товаров исправить img
# ToDO фильтрацию товара
# ToDO Корзина

class UserNew(AbstractUser):
    time_create = models.DateTimeField(auto_now_add=True)
    NumPhone = models.DecimalField(max_digits=10, decimal_places=0,blank=True,null=True)


class Goods(models.Model):
    NameGoods = models.CharField(max_length=300)
    Price = models.DecimalField(max_digits=20, decimal_places=2)
    GoodsStock = models.DecimalField(max_digits=5, decimal_places=0)
    GoodsPhoto = models.ImageField(upload_to="photos/")
