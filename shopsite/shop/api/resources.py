from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import Authorization
from django.contrib.auth.models import User
from shop.models import Product, Order


class UserResource(ModelResource):

    class Meta:
        queryset = User.objects.all()
        resource_name = "users"
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        fields = ['id', 'username', 'email']
        authentication = BasicAuthentication()
        authorization = Authorization()

    def get_object_list(self, request):
        object_list = super(UserResource, self).get_object_list(request)
        return object_list.filter(pk=request.user.pk)


class ProductResource(ModelResource):
    users = fields.ToManyField(UserResource, "users", full=True)

    class Meta:
        queryset = Product.objects.all()
        resource_name = "products"
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        authentication = BasicAuthentication()
        authorization = Authorization()

    def dehydrate(self, bundle):
        current_user = bundle.request.user
        user_products = current_user.product_set.all()

        if bundle.obj in user_products:
            bundle.data['inOrder'] = True
        else:
            bundle.data['inOrder'] = False

        return bundle


class OrderResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user', full=True)
    product = fields.ToOneField(ProductResource, 'product', full=True)

    class Meta:
        queryset = Order.objects.all()
        resource_name = "orders"
        authentication = BasicAuthentication()
        authorization = Authorization()

    def get_object_list(self, request):
        object_list = super(OrderResource, self).get_object_list(request)
        return object_list.filter(user=request.user)
