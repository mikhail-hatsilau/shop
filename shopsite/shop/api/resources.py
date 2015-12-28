from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.authentication import BasicAuthentication
from django.contrib.auth.models import User
from shop.models import Product, Order, Category
from shop.Authorization import UserAuthorization, ProductCategoryAuthorization
from shop.Authorization import OrderAuthorization
import waffle


class UserResource(ModelResource):

    class Meta:
        queryset = User.objects.all()
        resource_name = "users"
        fields = ['id', 'username', 'email']
        authentication = BasicAuthentication()
        authorization = UserAuthorization()

    def dehydrate(self, bundle):
        bundle.data['isSeller'] = waffle.flag_is_active(bundle.request,
                                                        'is_seller')
        return bundle


class CategoryResource(ModelResource):

    class Meta:
        queryset = Category.objects.all()
        resource_name = 'categories'
        authentication = BasicAuthentication()
        authorization = ProductCategoryAuthorization()
        filtering = {
            'id': ALL
        }


class ProductResource(ModelResource):
    category = fields.ToOneField(CategoryResource, 'category', full=True)

    class Meta:
        queryset = Product.objects.all()
        resource_name = "products"
        always_return_data = True
        authentication = BasicAuthentication()
        authorization = ProductCategoryAuthorization()
        filtering = {
            'category': ALL_WITH_RELATIONS
        }

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
        authorization = OrderAuthorization()
