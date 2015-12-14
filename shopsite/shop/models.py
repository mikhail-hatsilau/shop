from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
	name = models.CharField(max_length = 200)
	discription = models.CharField(max_length = 600)
	price = models.CharField(max_length = 50)
	users = models.ManyToManyField(User, through='Order')
	image = models.ImageField(upload_to = 'static/images', default = 'static/images/default_product.png', blank = False)

	def __str__(self):
		return self.name

class Order(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	product = models.ForeignKey(Product, on_delete = models.CASCADE)
	date = models.DateField()

