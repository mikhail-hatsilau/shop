from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    discription = models.CharField(max_length=600)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    users = models.ManyToManyField(User, through='Order')
    image = models.ImageField(upload_to='static/images',
                              default='static/images/default_product.png',
                              blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField()
