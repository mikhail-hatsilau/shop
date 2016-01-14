from django.conf.urls import url
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.http import HttpForbidden, HttpNotFound
from shop.models import Product, Order, Category
from shop.Authorization import UserAuthorization, ProductAuthorization
from shop.Authorization import OrderAuthorization, CategoryAuthorization
import waffle


class UserResource(ModelResource):

    class Meta:
        queryset = get_user_model().objects.all()
        resource_name = "users"
        fields = ['id', 'username', 'email']
        authentication = SessionAuthentication()
        authorization = UserAuthorization()

    def dehydrate(self, bundle):
        bundle.data['isSeller'] = waffle.flag_is_active(bundle.request,
                                                        'is_seller')
        return bundle

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/logged/$" % self._meta.resource_name,
                self.wrap_view('get_logged_user'), name="logged")
        ]

    def get_logged_user(self, request, **kwargs):
        self.method_check(request, allowed=['get'])

        user_bundle = self.build_bundle(request=request, obj=request.user)
        user_json = self.full_dehydrate(user_bundle)
        return self.create_response(request, user_json)


class LoginResource(ModelResource):

    class Meta:
        resource_name = "login"

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login/$" % self._meta.resource_name,
                self.wrap_view('user_login'), name="login"),
            url(r"^(?P<resource_name>%s)/logout/$" % self._meta.resource_name,
                self.wrap_view('user_logout'), name="logout")
        ]

    def user_login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body)
        username = data.get('login', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                res = UserResource()

                user_bundle = res.build_bundle(request=request, obj=user)
                user_json = res.full_dehydrate(user_bundle)

                return self.create_response(request, user_json)
            else:
                not_active = {
                    'success': False,
                    'reason': 'Account is not active'
                }
                return self.create_response(request, not_active, HttpForbidden)
        else:
            not_found = {
                'success': False,
                'reason': 'Wrong login or password'
            }
            return self.create_response(request, not_found, HttpNotFound)

    def user_logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])

        if request.user is not None and request.user.is_authenticated():
            logout(request)

        return self.create_response(request, {'success': True})


class CategoryResource(ModelResource):

    class Meta:
        queryset = Category.objects.all()
        resource_name = 'categories'
        authentication = SessionAuthentication()
        authorization = CategoryAuthorization()
        filtering = {
            'id': ALL
        }


class ProductResource(ModelResource):
    category = fields.ForeignKey(CategoryResource, 'category', full=True)
    seller = fields.ForeignKey(UserResource, 'seller', full=True)

    class Meta:
        queryset = Product.objects.all()
        resource_name = "products"
        always_return_data = True
        authentication = SessionAuthentication()
        authorization = ProductAuthorization()
        filtering = {
            'category': ALL_WITH_RELATIONS
        }

    def dehydrate(self, bundle):
        current_user = bundle.request.user
        user_orders = current_user.order_set.all()

        for order in user_orders:
            if bundle.obj == order.product:
                bundle.data['inOrder'] = True
                break
        else:
            bundle.data['inOrder'] = False

        return bundle


class OrderResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=True)
    product = fields.ForeignKey(ProductResource, 'product', full=True)

    class Meta:
        queryset = Order.objects.all()
        resource_name = "orders"
        authentication = SessionAuthentication()
        authorization = OrderAuthorization()
