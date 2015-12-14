from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.paginator import Paginator
from django.contrib.auth.models import User
from shop.models import Product, Order

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		resource_name = "users"
		fields = ['id', 'username', 'email']
		authentication = BasicAuthentication()
		authorization = DjangoAuthorization()

class ProductResource(ModelResource):
	users = fields.ToManyField(UserResource, "users", full = True)
	class Meta:
		queryset = Product.objects.all()
		resource_name = "products"
		authentication = BasicAuthentication()
		authorization = DjangoAuthorization()

	def dehydrate(self, bundle):
		current_user = bundle.request.user
		user_products = current_user.product_set.all()

		if bundle.obj in user_products:
			bundle.data['inOrder'] = True
		else:
			bundle.data['inOrder'] = False

		return bundle

class OrderResource(ModelResource):
	user = fields.ToOneField(UserResource, 'user', full = True)
	product = fields.ToOneField(ProductResource, 'product', full = True)
	class Meta:
		queryset = Order.objects.all()
		resource_name = "orders"
		authentication = BasicAuthentication()
		authorization = DjangoAuthorization()
	
	def authorized_read_list(self, object_list, bundle):
		return object_list.filter(user = bundle.request.user)

	def hydrate_user(self, bundle):
		bundle.obj.user = bundle.request.user
		return bundle
	