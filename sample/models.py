from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from sample.model_manager import UserModelManager, BaseManager


class User(AbstractUser):
    objects = UserModelManager()

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(null=True)


class Address(models.Model):
    objects = BaseManager()

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ad')
    plain_address = models.TextField()
    postal_code = models.CharField(max_length=10, blank=True)
    lat = models.DecimalField(max_digits=17, decimal_places=14)
    long = models.DecimalField(max_digits=17, decimal_places=14)


class Product(models.Model):
    objects = BaseManager()

    name = models.CharField(max_length=128)
    code = models.CharField(max_length=64, blank=True)


class SalesDoc(models.Model):
    objects = BaseManager()

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_sd')
    payment_method = models.PositiveSmallIntegerField(choices=((1, "on_demand"), (2, "online"),))
    total_price = models.IntegerField()
    description = models.TextField()


class SalesDocItem(models.Model):
    objects = BaseManager()

    sale_doc = models.ForeignKey(SalesDoc, on_delete=models.CASCADE, related_name="sale_doc_sdi")
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name="product_sdi")
    quantity = models.FloatField()