from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase
from waffle.models import Flag
from datetime import date
from .models import Category, Product, Order


class UserCreator:
    def create_users(self):
        self.super_name = 'admin'
        self.password = 'qwerty'
        self.super_user = User.objects.create_user(username=self.super_name,
                                                   password=self.password)
        self.super_user.is_superuser = True
        self.super_user.save()

        self.seller_name = 'seller'
        self.seller = User.objects.create_user(username=self.seller_name,
                                               password=self.password)
        self.seller.is_seller = True
        self.seller.save()

        self.buyer_name = 'buyer'
        self.buyer = User.objects.create_user(username=self.buyer_name,
                                              password=self.password)

        flag = Flag.objects.get(pk=1)
        flag.users.add(self.seller.pk)
        flag.save()

        self.url_super = '/api/v1/users/{0}/'.format(self.super_user.pk)
        self.url_seller = '/api/v1/users/{0}/'.format(self.seller.pk)
        self.url_buyer = '/api/v1/users/{0}/'.format(self.buyer.pk)


class UserResourceTest(ResourceTestCase, UserCreator):

    fixtures = ['tests_data.json']

    def setUp(self):
        super(UserResourceTest, self).setUp()
        super(UserResourceTest, self).create_users()

        self.data_user = {
            'username': 'person',
            'password': 'new'
        }

        self.url = '/api/v1/users/'

    def get_credentials(self, username, password):
        return self.create_basic(username=username,
                                 password=password)

    def test_get_users_list_super(self):
        auth = self.get_credentials(self.super_name, self.password)
        resp = self.api_client.get(self.url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_get_users_list_seller(self):
        auth = self.get_credentials(self.seller_name, self.password)
        resp = self.api_client.get(self.url,
                                   format='json',
                                   authentication=auth)
        deserialized_resp = self.deserialize(resp)

        self.assertValidJSONResponse(resp)
        self.assertEqual(len(deserialized_resp['objects']), 1)
        self.assertEqual(deserialized_resp['objects'][0]['id'], self.seller.pk)

    def test_get_users_list_buyer(self):
        auth = self.get_credentials(self.buyer_name, self.password)
        resp = self.api_client.get(self.url,
                                   format='json',
                                   authentication=auth)
        deserialized_resp = self.deserialize(resp)

        self.assertValidJSONResponse(resp)
        self.assertEqual(len(deserialized_resp['objects']), 1)
        self.assertEqual(deserialized_resp['objects'][0]['id'], self.buyer.pk)

    def test_get_user_details_super(self):
        auth = self.get_credentials(self.super_name, self.password)
        resp_own = self.api_client.get(self.url_super,
                                       format='json',
                                       authentication=auth)
        resp_other = self.api_client.get(self.url_buyer,
                                         format='json',
                                         authentication=auth)
        self.assertValidJSONResponse(resp_own)
        self.assertValidJSONResponse(resp_other)

    def test_get_user_details_seller(self):
        auth = self.get_credentials(self.seller_name, self.password)
        resp_own = self.api_client.get(self.url_seller,
                                       format='json',
                                       authentication=auth)
        resp_other = self.api_client.get(self.url_buyer,
                                         format='json',
                                         authentication=auth)
        self.assertValidJSONResponse(resp_own)
        self.assertHttpUnauthorized(resp_other)

    def test_get_user_details_buyer(self):
        auth = self.get_credentials(self.buyer_name, self.password)
        resp_own = self.api_client.get(self.url_buyer,
                                       format='json',
                                       authentication=auth)
        resp_other = self.api_client.get(self.url_seller,
                                         format='json',
                                         authentication=auth)
        self.assertValidJSONResponse(resp_own)
        self.assertHttpUnauthorized(resp_other)

    def test_post_users_super(self):
        auth = self.get_credentials(self.super_name, self.password)
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=self.data_user,
                                    authentication=auth)
        self.assertHttpCreated(resp)

    def test_post_users_seller(self):
        auth = self.get_credentials(self.seller_name, self.password)
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=self.data_user,
                                    authentication=auth)
        self.assertHttpUnauthorized(resp)

    def test_post_users_buyer(self):
        auth = self.get_credentials(self.buyer_name, self.password)
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=self.data_user,
                                    authentication=auth)
        self.assertHttpUnauthorized(resp)

    def test_update_user_super(self):
        auth = self.get_credentials(self.super_name, self.password)
        resp = self.api_client.put(self.url_buyer,
                                   format='json',
                                   data={},
                                   authentication=auth)
        self.assertHttpAccepted(resp)

    def test_update_user_seller(self):
        auth = self.get_credentials(self.seller_name, self.password)
        resp = self.api_client.put(self.url_buyer,
                                   format='json',
                                   data={},
                                   authentication=auth)
        self.assertHttpUnauthorized(resp)

    def test_update_user_buyer(self):
        auth = self.get_credentials(self.buyer_name, self.password)
        resp = self.api_client.put(self.url_seller,
                                   format='json',
                                   data={},
                                   authentication=auth)
        self.assertHttpUnauthorized(resp)

    def test_delete_user_seller(self):
        auth = self.get_credentials(self.seller_name, self.password)
        resp = self.api_client.delete(self.url_buyer,
                                      format='json',
                                      authentication=auth)
        self.assertHttpUnauthorized(resp)

    def test_delete_user_buyer(self):
        auth = self.get_credentials(self.buyer_name, self.password)
        resp = self.api_client.delete(self.url_seller,
                                      format='json',
                                      authentication=auth)
        self.assertHttpUnauthorized(resp)

    def test_delete_user_super(self):
        auth = self.get_credentials(self.super_name, self.password)
        resp = self.api_client.delete(self.url_buyer,
                                      format='json',
                                      authentication=auth)
        self.assertHttpAccepted(resp)


class ProductResourceTest(ResourceTestCase, UserCreator):

    fixtures = ['tests_data.json']

    def setUp(self):
        super(ProductResourceTest, self).setUp()
        super(ProductResourceTest, self).create_users()

        self.category = Category.objects.get(pk=1)

        category_uri = '/api/v1/categories/{0}/'.format(self.category.pk)

        self.product = Product.objects.create(name='product22',
                                              discription='discription',
                                              price=120,
                                              category=self.category)

        self.post_add_product = {
            'name': 'product',
            'discription': 'discription',
            'price': '120',
            'category': category_uri
        }

        self.url = '/api/v1/products/'
        self.details_url = '/api/v1/products/{0}/'.format(self.product.pk)

    def get_credentials(self, username, password):
        return self.create_basic(username=username,
                                 password=password)

    def test_get_products_list_super(self):
        auth = self.get_credentials(self.super_name, self.password)
        resp = self.api_client.get(self.url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_get_products_list_seller(self):
        auth = self.get_credentials(self.seller_name, self.password)
        resp = self.api_client.get(self.url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_get_products_list_buyer(self):
        auth = self.get_credentials(self.buyer_name, self.password)
        resp = self.api_client.get(self.url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_get_product_details_super(self):
        auth = self.get_credentials(self.super_name, self.password)
        resp = self.api_client.get(self.details_url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_get_product_details_seller(self):
        auth = self.get_credentials(self.seller_name, self.password)
        resp = self.api_client.get(self.details_url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_get_product_details_buyer(self):
        auth = self.get_credentials(self.buyer_name, self.password)
        resp = self.api_client.get(self.details_url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_post_products_super(self):
        auth = self.get_credentials(self.super_name, self.password)
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=self.post_add_product,
                                    authentication=auth)
        self.assertHttpCreated(resp)

    def test_post_products_seller(self):
        auth = self.get_credentials(self.seller_name, self.password)
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=self.post_add_product,
                                    authentication=auth)
        self.assertHttpCreated(resp)

    def test_post_products_buyer(self):
        auth = self.get_credentials(self.buyer_name, self.password)
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=self.post_add_product,
                                    authentication=auth)
        self.assertHttpUnauthorized(resp)

    def test_update_product_super(self):
        auth = self.get_credentials(self.super_name, self.password)
        resp = self.api_client.put(self.details_url,
                                   format='json',
                                   data={},
                                   authentication=auth)
        self.assertHttpOK(resp)

    def test_update_product_seller(self):
        auth = self.get_credentials(self.seller_name, self.password)
        resp = self.api_client.put(self.details_url,
                                   format='json',
                                   data={},
                                   authentication=auth)
        self.assertHttpOK(resp)

    def test_update_product_buyer(self):
        auth = self.get_credentials(self.buyer_name, self.password)
        resp = self.api_client.put(self.details_url,
                                   format='json',
                                   data={},
                                   authentication=auth)
        self.assertHttpUnauthorized(resp)

    def test_delete_product_super(self):
        auth = self.get_credentials(self.super_name, self.password)
        resp = self.api_client.delete(self.details_url,
                                      format='json',
                                      authentication=auth)
        self.assertHttpAccepted(resp)

    def test_delete_product_seller(self):
        auth = self.get_credentials(self.seller_name, self.password)
        resp = self.api_client.delete(self.details_url,
                                      format='json',
                                      authentication=auth)
        self.assertHttpAccepted(resp)

    def test_delete_product_buyer(self):
        auth = self.get_credentials(self.buyer_name, self.password)
        resp = self.api_client.delete(self.details_url,
                                      format='json',
                                      authentication=auth)
        self.assertHttpUnauthorized(resp)


class CategoryResourceTest(ResourceTestCase, UserCreator):

    fixtures = ['tests_data.json']

    def setUp(self):
        super(CategoryResourceTest, self).setUp()
        super(CategoryResourceTest, self).create_users()

        self.category = Category.objects.create(name='Phones')

        self.url = '/api/v1/categories/'
        self.details_url = '/api/v1/categories/{0}/'.format(self.category.pk)

        self.post_category = {
            'name': 'Games',
        }

    def get_credentials(self, username, password):
        return self.create_basic(username=username,
                                 password=password)

    def test_get_categories_list_super(self):
        auth = self.get_credentials(self.super_name, self.password)
        resp = self.api_client.get(self.url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_get_categories_list_seller(self):
        auth = self.get_credentials(self.seller_name, self.password)
        resp = self.api_client.get(self.url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_get_categories_list_buyer(self):
        auth = self.get_credentials(self.buyer_name, self.password)
        resp = self.api_client.get(self.url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_get_category_details_super(self):
        auth = self.get_credentials(self.super_name, self.password)
        resp = self.api_client.get(self.details_url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_get_category_details_seller(self):
        auth = self.get_credentials(self.seller_name, self.password)
        resp = self.api_client.get(self.details_url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_get_category_details_buyer(self):
        auth = self.get_credentials(self.buyer_name, self.password)
        resp = self.api_client.get(self.details_url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_post_categories_super(self):
        auth = self.get_credentials(self.super_name, self.password)
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=self.post_category,
                                    authentication=auth)
        self.assertHttpCreated(resp)

    def test_post_categories_seller(self):
        auth = self.get_credentials(self.seller_name, self.password)
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=self.post_category,
                                    authentication=auth)
        self.assertHttpCreated(resp)

    def test_post_categories_buyer(self):
        auth = self.get_credentials(self.buyer_name, self.password)
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=self.post_category,
                                    authentication=auth)
        self.assertHttpUnauthorized(resp)

    def test_update_category_super(self):
        auth = self.get_credentials(self.super_name, self.password)
        resp = self.api_client.put(self.details_url,
                                   format='json',
                                   data={},
                                   authentication=auth)
        self.assertHttpAccepted(resp)

    def test_update_category_seller(self):
        auth = self.get_credentials(self.seller_name, self.password)
        resp = self.api_client.put(self.details_url,
                                   format='json',
                                   data={},
                                   authentication=auth)
        self.assertHttpAccepted(resp)

    def test_update_category_buyer(self):
        auth = self.get_credentials(self.buyer_name, self.password)
        resp = self.api_client.put(self.details_url,
                                   format='json',
                                   data={},
                                   authentication=auth)
        self.assertHttpUnauthorized(resp)

    def test_delete_category_super(self):
        auth = self.get_credentials(self.super_name, self.password)
        resp = self.api_client.delete(self.details_url,
                                      format='json',
                                      authentication=auth)
        self.assertHttpAccepted(resp)

    def test_delete_category_seller(self):
        auth = self.get_credentials(self.seller_name, self.password)
        resp = self.api_client.delete(self.details_url,
                                      format='json',
                                      authentication=auth)
        self.assertHttpAccepted(resp)

    def test_delete_category_buyer(self):
        auth = self.get_credentials(self.buyer_name, self.password)
        resp = self.api_client.delete(self.details_url,
                                      format='json',
                                      authentication=auth)
        self.assertHttpUnauthorized(resp)


class OrderResourceTest(ResourceTestCase, UserCreator):

    fixtures = ['tests_data.json']

    def setUp(self):
        super(OrderResourceTest, self).setUp()
        super(OrderResourceTest, self).create_users()

        self.category = Category.objects.get(pk=1)
        self.product = Product.objects.get(pk=1)
        self.super_order = Order.objects.create(user=self.super_user,
                                                product=self.product,
                                                date=date.today())
        self.seller_order = Order.objects.create(user=self.seller,
                                                 product=self.product,
                                                 date=date.today())
        self.buyer_order = Order.objects.create(user=self.buyer,
                                                product=self.product,
                                                date=date.today())
        self.url = '/api/v1/orders/'

        self.details_super = '/api/v1/orders/{0}/'.format(self.super_order.pk)
        self.details_seller = '/api/v1/orders/{0}/'.format(self.seller_order.pk)
        self.details_buyer = '/api/v1/orders/{0}/'.format(self.buyer_order.pk)

        self.post_order_super = {
            'user': self.url_super,
            'product': '/api/v1/products/{0}/'.format(self.product.pk),
            'date': date(2015, 07, 05)
        }

        self.post_order_seller = {
            'user': self.url_seller,
            'product': '/api/v1/products/{0}/'.format(self.product.pk),
            'date': date(2015, 07, 05)
        }

        self.post_order_buyer = {
            'user': self.url_buyer,
            'product': '/api/v1/products/{0}/'.format(self.product.pk),
            'date': date(2015, 07, 05)
        }

    def get_credentials(self, username, password):
        return self.create_basic(username=username,
                                 password=password)

    def test_get_orders_list_own(self):
        auth = self.get_credentials(self.buyer_name, self.password)
        resp = self.api_client.get(self.url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

        deserialized_obj = self.deserialize(resp)

        for order in deserialized_obj['objects']:
            self.assertEqual(order['user']['resource_uri'],
                             self.url_buyer)

    def test_get_orders_list_super(self):
        auth = self.get_credentials(self.super_name, self.password)
        resp = self.api_client.get(self.url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_get_orders_list_seller(self):
        auth = self.get_credentials(self.seller_name, self.password)
        resp = self.api_client.get(self.url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_get_orders_list_buyer(self):
        auth = self.get_credentials(self.buyer_name, self.password)
        resp = self.api_client.get(self.url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_get_order_details_super(self):
        auth = self.get_credentials(self.super_name, self.password)
        resp_own = self.api_client.get(self.details_super,
                                       format='json',
                                       authentication=auth)
        resp_other = self.api_client.get(self.details_buyer,
                                         format='json',
                                         authentication=auth)
        self.assertValidJSONResponse(resp_own)
        self.assertValidJSONResponse(resp_other)

    def test_get_order_details_seller(self):
        auth = self.get_credentials(self.seller_name, self.password)
        resp_own = self.api_client.get(self.details_seller,
                                       format='json',
                                       authentication=auth)
        resp_other = self.api_client.get(self.details_buyer,
                                         format='json',
                                         authentication=auth)
        self.assertValidJSONResponse(resp_own)
        self.assertHttpUnauthorized(resp_other)

    def test_get_order_details_buyer(self):
        auth = self.get_credentials(self.buyer_name, self.password)
        resp_own = self.api_client.get(self.details_buyer,
                                       format='json',
                                       authentication=auth)
        resp_other = self.api_client.get(self.details_seller,
                                         format='json',
                                         authentication=auth)
        self.assertValidJSONResponse(resp_own)
        self.assertHttpUnauthorized(resp_other)

    def test_post_orders_super(self):
        auth = self.get_credentials(self.super_name, self.password)
        resp_own = self.api_client.post(self.url,
                                        format='json',
                                        data=self.post_order_super,
                                        authentication=auth)
        resp_other = self.api_client.post(self.url,
                                          format='json',
                                          data=self.post_order_buyer,
                                          authentication=auth)
        self.assertHttpCreated(resp_own)
        self.assertHttpCreated(resp_other)

    def test_post_orders_seller(self):
        auth = self.get_credentials(self.seller_name, self.password)
        resp_own = self.api_client.post(self.url,
                                        format='json',
                                        data=self.post_order_seller,
                                        authentication=auth)
        resp_other = self.api_client.post(self.url,
                                          format='json',
                                          data=self.post_order_buyer,
                                          authentication=auth)
        self.assertHttpCreated(resp_own)
        self.assertHttpUnauthorized(resp_other)

    def test_post_orders_buyer(self):
        auth = self.get_credentials(self.buyer_name, self.password)
        resp_own = self.api_client.post(self.url,
                                        format='json',
                                        data=self.post_order_buyer,
                                        authentication=auth)
        resp_other = self.api_client.post(self.url,
                                          format='json',
                                          data=self.post_order_seller,
                                          authentication=auth)
        self.assertHttpCreated(resp_own)
        self.assertHttpUnauthorized(resp_other)

    def test_update_orders_super(self):
        auth = self.get_credentials(self.super_name, self.password)
        resp_own = self.api_client.put(self.details_super,
                                       format='json',
                                       data={},
                                       authentication=auth)
        resp_other = self.api_client.put(self.details_buyer,
                                         format='json',
                                         data={},
                                         authentication=auth)
        self.assertHttpAccepted(resp_own)
        self.assertHttpAccepted(resp_other)

    def test_update_orders_seller(self):
        auth = self.get_credentials(self.seller_name, self.password)
        resp_own = self.api_client.put(self.details_seller,
                                       format='json',
                                       data={},
                                       authentication=auth)
        resp_other = self.api_client.put(self.details_buyer,
                                         format='json',
                                         data=self.post_order_seller,
                                         authentication=auth)
        self.assertHttpAccepted(resp_own)
        self.assertHttpUnauthorized(resp_other)

    def test_update_orders_buyer(self):
        auth = self.get_credentials(self.buyer_name, self.password)
        resp_own = self.api_client.put(self.details_buyer,
                                       format='json',
                                       data={},
                                       authentication=auth)
        resp_other = self.api_client.put(self.details_seller,
                                         format='json',
                                         data={},
                                         authentication=auth)
        self.assertHttpAccepted(resp_own)
        self.assertHttpUnauthorized(resp_other)

    def test_delete_orders_super(self):
        auth = self.get_credentials(self.super_name, self.password)
        resp_own = self.api_client.delete(self.details_super,
                                          format='json',
                                          data={},
                                          authentication=auth)
        resp_other = self.api_client.delete(self.details_buyer,
                                            format='json',
                                            data=self.post_order_seller,
                                            authentication=auth)
        self.assertHttpAccepted(resp_own)
        self.assertHttpAccepted(resp_other)

    def test_delete_orders_seller(self):
        auth = self.get_credentials(self.seller_name, self.password)
        resp_own = self.api_client.delete(self.details_seller,
                                          format='json',
                                          data={},
                                          authentication=auth)
        resp_other = self.api_client.delete(self.details_buyer,
                                            format='json',
                                            data=self.post_order_seller,
                                            authentication=auth)
        self.assertHttpAccepted(resp_own)
        self.assertHttpUnauthorized(resp_other)

    def test_delete_orders_buyer(self):
        auth = self.get_credentials(self.buyer_name, self.password)
        resp_own = self.api_client.delete(self.details_buyer,
                                          format='json',
                                          data={},
                                          authentication=auth)
        resp_other = self.api_client.delete(self.details_seller,
                                            format='json',
                                            data=self.post_order_seller,
                                            authentication=auth)
        self.assertHttpAccepted(resp_own)
        self.assertHttpUnauthorized(resp_other)
