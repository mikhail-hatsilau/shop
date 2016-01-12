from django.db import models
from django.utils import timezone
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    discription = models.CharField(max_length=600)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/images',
                              default='static/images/default_product.png',
                              blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    from_date = models.DateTimeField(default=timezone.now())
    to_date = models.DateTimeField(default=timezone.now() + timezone.timedelta(days=7))

    def __unicode__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField()
