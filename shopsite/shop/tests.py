from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase
from waffle.models import Flag
from django.utils import timezone
from .models import Category, Product, Order


class UserCreator:
    def create_users(self):
        self.password = 'gatik'
        self.super_name = 'super'
        self.super_user = User.objects.create_user(username=self.super_name,
                                                   password=self.password)
        self.super_user.is_superuser = True
        self.super_user.save()

        self.seller1_name = 'seller1'
        self.seller1 = User.objects.create_user(username=self.seller1_name,
                                                password=self.password)

        self.seller2_name = 'seller2'
        self.seller2 = User.objects.create_user(username=self.seller2_name,
                                                password=self.password)

        self.buyer_name = 'buyer'
        self.buyer = User.objects.create_user(username=self.buyer_name,
                                              password=self.password)

        flag = Flag.objects.get(pk=1)
        flag.users.add(self.seller1.pk)
        flag.users.add(self.seller2.pk)
        flag.save()

        self.url_super = '/api/v1/users/{0}/'.format(self.super_user.pk)
        self.url_seller1 = '/api/v1/users/{0}/'.format(self.seller1.pk)
        self.url_seller2 = '/api/v1/users/{0}/'.format(self.seller2.pk)
        self.url_buyer = '/api/v1/users/{0}/'.format(self.buyer.pk)


class UserResourceTest(ResourceTestCase, UserCreator):

    fixtures = ['tests_data.json']

    def setUp(self):
        super(UserResourceTest, self).setUp()
        super(UserResourceTest, self).create_users()

        self.user_delete = User.objects.create_user(username="user",
                                                    password="123")
        self.url_user_delete = '/api/v1/users/{0}/'.format(self.user_delete.pk)

        self.data_user = {
            'username': 'person',
            'password': 'new'
        }

        self.url = '/api/v1/users/'

    def set_session(self, username, password):
        self.api_client.client.login(username=username,
                                     password=password)

    def test_get_users_list_super(self):
        self.set_session(self.super_name, self.password)
        resp = self.api_client.get(self.url,
                                   format='json')
        self.assertValidJSONResponse(resp)

    def test_get_users_list_seller(self):
        self.set_session(self.seller1_name, self.password)
        resp = self.api_client.get(self.url,
                                   format='json')
        deserialized_resp = self.deserialize(resp)

        self.assertValidJSONResponse(resp)
        self.assertEqual(len(deserialized_resp['objects']), 1)
        self.assertEqual(deserialized_resp['objects'][0]['id'], self.seller1.pk)

    def test_get_users_list_buyer(self):
        self.set_session(self.buyer_name, self.password)
        resp = self.api_client.get(self.url,
                                   format='json')
        deserialized_resp = self.deserialize(resp)

        self.assertValidJSONResponse(resp)
        self.assertEqual(len(deserialized_resp['objects']), 1)
        self.assertEqual(deserialized_resp['objects'][0]['id'], self.buyer.pk)

    def test_get_user_details_super(self):
        self.set_session(self.super_name, self.password)
        resp_own = self.api_client.get(self.url_super,
                                       format='json')
        resp_other = self.api_client.get(self.url_buyer,
                                         format='json')
        self.assertValidJSONResponse(resp_own)
        self.assertValidJSONResponse(resp_other)

    def test_get_user_details_seller(self):
        self.set_session(self.seller1_name, self.password)
        resp_own = self.api_client.get(self.url_seller1,
                                       format='json')
        resp_other = self.api_client.get(self.url_buyer,
                                         format='json')
        self.assertValidJSONResponse(resp_own)
        self.assertHttpUnauthorized(resp_other)

    def test_get_user_details_buyer(self):
        self.set_session(self.buyer_name, self.password)
        resp_own = self.api_client.get(self.url_buyer,
                                       format='json')
        resp_other = self.api_client.get(self.url_seller1,
                                         format='json')
        self.assertValidJSONResponse(resp_own)
        self.assertHttpUnauthorized(resp_other)

    def test_post_users_super(self):
        self.set_session(self.super_name, self.password)
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=self.data_user)
        self.assertHttpCreated(resp)

    def test_post_users_seller(self):
        self.set_session(self.seller1_name, self.password)
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=self.data_user)
        self.assertHttpUnauthorized(resp)

    def test_post_users_buyer(self):
        self.set_session(self.buyer_name, self.password)
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=self.data_user)
        self.assertHttpUnauthorized(resp)

    def test_update_user_super(self):
        self.set_session(self.super_name, self.password)
        resp = self.api_client.put(self.url_user_delete,
                                   format='json',
                                   data={})
        self.assertHttpAccepted(resp)

    def test_update_user_seller(self):
        self.set_session(self.seller1_name, self.password)
        resp = self.api_client.put(self.url_user_delete,
                                   format='json',
                                   data={})
        self.assertHttpUnauthorized(resp)

    def test_update_user_buyer(self):
        self.set_session(self.buyer_name, self.password)
        resp = self.api_client.put(self.url_user_delete,
                                   format='json',
                                   data={})
        self.assertHttpUnauthorized(resp)

    def test_delete_user_seller(self):
        self.set_session(self.seller1_name, self.password)
        resp = self.api_client.delete(self.url_user_delete,
                                      format='json')
        self.assertHttpUnauthorized(resp)

    def test_delete_user_buyer(self):
        self.set_session(self.buyer_name, self.password)
        resp = self.api_client.delete(self.url_user_delete,
                                      format='json')
        self.assertHttpUnauthorized(resp)

    def test_delete_user_super(self):
        self.set_session(self.super_name, self.password)
        resp = self.api_client.delete(self.url_user_delete,
                                      format='json')
        self.assertHttpAccepted(resp)


class ProductResourceTest(ResourceTestCase, UserCreator):

    fixtures = ['tests_data.json']

    def setUp(self):
        super(ProductResourceTest, self).setUp()
        super(ProductResourceTest, self).create_users()

        self.category = Category.objects.get(pk=1)

        category_uri = '/api/v1/categories/{0}/'.format(self.category.pk)

        self.product1 = Product.objects.create(name='product11',
                                               discription='discription',
                                               price=120,
                                               category=self.category,
                                               seller=self.seller1)
        self.product2 = Product.objects.create(name='product22',
                                               discription='discription',
                                               price=15,
                                               category=self.category,
                                               seller=self.seller2)

        self.post_product_seller1 = {
            'name': 'product',
            'discription': 'discription',
            'price': '120',
            'category': category_uri,
            'seller': self.url_seller1
        }

        self.post_product_seller2 = {
            'name': 'product21',
            'discription': 'discription',
            'price': '1',
            'category': category_uri,
            'seller': self.url_seller2
        }

        self.url = '/api/v1/products/'
        self.details_url1 = '/api/v1/products/{0}/'.format(self.product1.pk)
        self.details_url2 = '/api/v1/products/{0}/'.format(self.product2.pk)

    def set_session(self, username, password):
        self.api_client.client.login(username=username,
                                     password=password)

    def test_get_products_list_super(self):
        self.set_session(self.super_name, self.password)
        resp = self.api_client.get(self.url,
                                   format='json')
        self.assertValidJSONResponse(resp)

    def test_get_products_list_seller(self):
        self.set_session(self.seller1_name, self.password)
        resp = self.api_client.get(self.url,
                                   format='json')
        deserialized_resp = self.deserialize(resp)
        for obj in deserialized_resp['objects']:
            self.assertEqual(obj['seller']['id'], self.seller1.pk)

    def test_get_products_list_buyer(self):
        self.set_session(self.buyer_name, self.password)
        resp = self.api_client.get(self.url,
                                   format='json')
        self.assertValidJSONResponse(resp)

    def test_get_product_details_super(self):
        self.set_session(self.super_name, self.password)
        resp = self.api_client.get(self.details_url1,
                                   format='json')
        self.assertValidJSONResponse(resp)

    def test_get_product_details_seller(self):
        self.set_session(self.seller1_name, self.password)
        resp_own = self.api_client.get(self.details_url1,
                                       format='json')
        resp_other = self.api_client.get(self.details_url2,
                                         format='json')
        self.assertValidJSONResponse(resp_own)
        self.assertHttpUnauthorized(resp_other)

    def test_get_product_details_buyer(self):
        self.set_session(self.buyer_name, self.password)
        resp_seller1 = self.api_client.get(self.details_url1,
                                           format='json')
        resp_seller2 = self.api_client.get(self.details_url2,
                                           format='json')
        self.assertValidJSONResponse(resp_seller1)
        self.assertValidJSONResponse(resp_seller2)

    def test_post_products_super(self):
        self.set_session(self.super_name, self.password)
        resp_own = self.api_client.post(self.url,
                                        format='json',
                                        data=self.post_product_seller1)
        resp_other = self.api_client.post(self.url,
                                          format='json',
                                          data=self.post_product_seller2)
        self.assertHttpCreated(resp_own)
        self.assertHttpCreated(resp_other)

    def test_post_products_seller(self):
        self.set_session(self.seller1_name, self.password)
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=self.post_product_seller1)
        self.assertHttpCreated(resp)

    def test_post_products_buyer(self):
        self.set_session(self.buyer_name, self.password)
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=self.post_product_seller1)
        self.assertHttpUnauthorized(resp)

    def test_update_product_super(self):
        self.set_session(self.super_name, self.password)
        resp_own = self.api_client.put(self.details_url1,
                                       format='json',
                                       data={})
        resp_other = self.api_client.put(self.details_url2,
                                         format='json',
                                         data={})
        self.assertHttpOK(resp_own)
        self.assertHttpOK(resp_other)

    def test_update_product_seller(self):
        self.set_session(self.seller1_name, self.password)
        resp_own = self.api_client.put(self.details_url1,
                                       format='json',
                                       data={})
        resp_other = self.api_client.put(self.details_url2,
                                         format='json',
                                         data={})
        self.assertHttpOK(resp_own)
        self.assertHttpUnauthorized(resp_other)

    def test_update_product_buyer(self):
        self.set_session(self.buyer_name, self.password)
        resp = self.api_client.put(self.details_url1,
                                   format='json',
                                   data={})
        self.assertHttpUnauthorized(resp)

    def test_delete_product_super(self):
        self.set_session(self.super_name, self.password)
        resp = self.api_client.delete(self.details_url1,
                                      format='json')
        self.assertHttpAccepted(resp)

    def test_delete_product_seller(self):
        self.set_session(self.seller1_name, self.password)
        resp_own = self.api_client.delete(self.details_url1,
                                          format='json')
        resp_other = self.api_client.delete(self.details_url2,
                                            format='json')
        self.assertHttpAccepted(resp_own)
        self.assertHttpUnauthorized(resp_other)

    def test_delete_product_buyer(self):
        self.set_session(self.buyer_name, self.password)
        resp = self.api_client.delete(self.details_url1,
                                      format='json')
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

    def set_session(self, username, password):
        self.api_client.client.login(username=username,
                                     password=password)

    def test_get_categories_list_super(self):
        self.set_session(self.super_name, self.password)
        resp = self.api_client.get(self.url,
                                   format='json')
        self.assertValidJSONResponse(resp)

    def test_get_categories_list_seller(self):
        self.set_session(self.seller1_name, self.password)
        resp = self.api_client.get(self.url,
                                   format='json')
        self.assertValidJSONResponse(resp)

    def test_get_categories_list_buyer(self):
        self.set_session(self.buyer_name, self.password)
        resp = self.api_client.get(self.url,
                                   format='json')
        self.assertValidJSONResponse(resp)

    def test_get_category_details_super(self):
        self.set_session(self.super_name, self.password)
        resp = self.api_client.get(self.details_url,
                                   format='json')
        self.assertValidJSONResponse(resp)

    def test_get_category_details_seller(self):
        self.set_session(self.seller1_name, self.password)
        resp = self.api_client.get(self.details_url,
                                   format='json')
        self.assertValidJSONResponse(resp)

    def test_get_category_details_buyer(self):
        self.set_session(self.buyer_name, self.password)
        resp = self.api_client.get(self.details_url,
                                   format='json')
        self.assertValidJSONResponse(resp)

    def test_post_categories_super(self):
        self.set_session(self.super_name, self.password)
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=self.post_category)
        self.assertHttpCreated(resp)

    def test_post_categories_seller(self):
        self.set_session(self.seller1_name, self.password)
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=self.post_category)
        self.assertHttpCreated(resp)

    def test_post_categories_buyer(self):
        self.set_session(self.buyer_name, self.password)
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=self.post_category)
        self.assertHttpUnauthorized(resp)

    def test_update_category_super(self):
        self.set_session(self.super_name, self.password)
        resp = self.api_client.put(self.details_url,
                                   format='json',
                                   data={})
        self.assertHttpAccepted(resp)

    def test_update_category_seller(self):
        self.set_session(self.seller1_name, self.password)
        resp = self.api_client.put(self.details_url,
                                   format='json',
                                   data={})
        self.assertHttpAccepted(resp)

    def test_update_category_buyer(self):
        self.set_session(self.buyer_name, self.password)
        resp = self.api_client.put(self.details_url,
                                   format='json',
                                   data={})
        self.assertHttpUnauthorized(resp)

    def test_delete_category_super(self):
        self.set_session(self.super_name, self.password)
        resp = self.api_client.delete(self.details_url,
                                      format='json')
        self.assertHttpAccepted(resp)

    def test_delete_category_seller(self):
        self.set_session(self.seller1_name, self.password)
        resp = self.api_client.delete(self.details_url,
                                      format='json')
        self.assertHttpAccepted(resp)

    def test_delete_category_buyer(self):
        self.set_session(self.buyer_name, self.password)
        resp = self.api_client.delete(self.details_url,
                                      format='json')
        self.assertHttpUnauthorized(resp)


class OrderResourceTest(ResourceTestCase, UserCreator):

    fixtures = ['tests_data.json']

    def setUp(self):
        super(OrderResourceTest, self).setUp()
        super(OrderResourceTest, self).create_users()

        self.category = Category.objects.get(pk=1)
        self.product = Product.objects.create(name='python',
                                              discription='Discr',
                                              price=120,
                                              category=self.category,
                                              seller=self.seller1)
        self.super_order = Order.objects.create(user=self.super_user,
                                                product=self.product,
                                                date=timezone.now())
        self.seller1_order = Order.objects.create(user=self.seller1,
                                                  product=self.product,
                                                  date=timezone.now())
        self.buyer_order = Order.objects.create(user=self.buyer,
                                                product=self.product,
                                                date=timezone.now())
        self.url = '/api/v1/orders/'

        self.details_super = '/api/v1/orders/{0}/'.format(self.super_order.pk)
        self.details_seller1 = '/api/v1/orders/{0}/'.format(self.seller1_order.pk)
        self.details_buyer = '/api/v1/orders/{0}/'.format(self.buyer_order.pk)

        self.post_order_super = {
            'user': self.url_super,
            'product': '/api/v1/products/{0}/'.format(self.product.pk),
            'date': timezone.now()
        }

        self.post_order_seller1 = {
            'user': self.url_seller1,
            'product': '/api/v1/products/{0}/'.format(self.product.pk),
            'date': timezone.now()
        }

        self.post_order_buyer = {
            'user': self.url_buyer,
            'product': '/api/v1/products/{0}/'.format(self.product.pk),
            'date': timezone.now()
        }

    def set_session(self, username, password):
        self.api_client.client.login(username=username,
                                     password=password)

    def test_get_orders_list_own(self):
        self.set_session(self.buyer_name, self.password)
        resp = self.api_client.get(self.url,
                                   format='json')
        self.assertValidJSONResponse(resp)

        deserialized_obj = self.deserialize(resp)

        for order in deserialized_obj['objects']:
            self.assertEqual(order['user']['resource_uri'],
                             self.url_buyer)

    def test_get_orders_list_super(self):
        self.set_session(self.super_name, self.password)
        resp = self.api_client.get(self.url,
                                   format='json')
        self.assertValidJSONResponse(resp)

    def test_get_orders_list_seller(self):
        self.set_session(self.seller1_name, self.password)
        resp = self.api_client.get(self.url,
                                   format='json')
        self.assertValidJSONResponse(resp)

    def test_get_orders_list_buyer(self):
        self.set_session(self.buyer_name, self.password)
        resp = self.api_client.get(self.url,
                                   format='json')
        self.assertValidJSONResponse(resp)

    def test_get_order_details_super(self):
        self.set_session(self.super_name, self.password)
        resp_own = self.api_client.get(self.details_super,
                                       format='json')
        resp_other = self.api_client.get(self.details_buyer,
                                         format='json')
        self.assertValidJSONResponse(resp_own)
        self.assertValidJSONResponse(resp_other)

    def test_get_order_details_seller(self):
        self.set_session(self.seller1_name, self.password)
        resp_own = self.api_client.get(self.details_seller1,
                                       format='json')
        resp_other = self.api_client.get(self.details_buyer,
                                         format='json')
        self.assertValidJSONResponse(resp_own)
        self.assertHttpUnauthorized(resp_other)

    def test_get_order_details_buyer(self):
        self.set_session(self.buyer_name, self.password)
        resp_own = self.api_client.get(self.details_buyer,
                                       format='json')
        resp_other = self.api_client.get(self.details_seller1,
                                         format='json')
        self.assertValidJSONResponse(resp_own)
        self.assertHttpUnauthorized(resp_other)

    def test_post_orders_super(self):
        self.set_session(self.super_name, self.password)
        resp_own = self.api_client.post(self.url,
                                        format='json',
                                        data=self.post_order_super)
        resp_other = self.api_client.post(self.url,
                                          format='json',
                                          data=self.post_order_buyer)
        self.assertHttpCreated(resp_own)
        self.assertHttpCreated(resp_other)

    def test_post_orders_seller(self):
        self.set_session(self.seller1_name, self.password)
        resp_own = self.api_client.post(self.url,
                                        format='json',
                                        data=self.post_order_seller1)
        resp_other = self.api_client.post(self.url,
                                          format='json',
                                          data=self.post_order_buyer)
        self.assertHttpCreated(resp_own)
        self.assertHttpUnauthorized(resp_other)

    def test_post_orders_buyer(self):
        self.set_session(self.buyer_name, self.password)
        resp_own = self.api_client.post(self.url,
                                        format='json',
                                        data=self.post_order_buyer)
        resp_other = self.api_client.post(self.url,
                                          format='json',
                                          data=self.post_order_seller1)
        self.assertHttpCreated(resp_own)
        self.assertHttpUnauthorized(resp_other)

    def test_update_orders_super(self):
        self.set_session(self.super_name, self.password)
        resp_own = self.api_client.put(self.details_super,
                                       format='json',
                                       data={})
        resp_other = self.api_client.put(self.details_buyer,
                                         format='json',
                                         data={})
        self.assertHttpAccepted(resp_own)
        self.assertHttpAccepted(resp_other)

    def test_update_orders_seller(self):
        self.set_session(self.seller1_name, self.password)
        resp_own = self.api_client.put(self.details_seller1,
                                       format='json',
                                       data={})
        resp_other = self.api_client.put(self.details_buyer,
                                         format='json',
                                         data=self.post_order_seller1)
        self.assertHttpAccepted(resp_own)
        self.assertHttpUnauthorized(resp_other)

    def test_update_orders_buyer(self):
        self.set_session(self.buyer_name, self.password)
        resp_own = self.api_client.put(self.details_buyer,
                                       format='json',
                                       data={})
        resp_other = self.api_client.put(self.details_seller1,
                                         format='json',
                                         data={})
        self.assertHttpAccepted(resp_own)
        self.assertHttpUnauthorized(resp_other)

    def test_delete_orders_super(self):
        self.set_session(self.super_name, self.password)
        resp_own = self.api_client.delete(self.details_super,
                                          format='json',
                                          data={})
        resp_other = self.api_client.delete(self.details_buyer,
                                            format='json',
                                            data=self.post_order_seller1)
        self.assertHttpAccepted(resp_own)
        self.assertHttpAccepted(resp_other)

    def test_delete_orders_seller(self):
        self.set_session(self.seller1_name, self.password)
        resp_own = self.api_client.delete(self.details_seller1,
                                          format='json',
                                          data={})
        resp_other = self.api_client.delete(self.details_buyer,
                                            format='json',
                                            data=self.post_order_seller1)
        self.assertHttpAccepted(resp_own)
        self.assertHttpUnauthorized(resp_other)

    def test_delete_orders_buyer(self):
        self.set_session(self.buyer_name, self.password)
        resp_own = self.api_client.delete(self.details_buyer,
                                          format='json',
                                          data={})
        resp_other = self.api_client.delete(self.details_seller1,
                                            format='json',
                                            data=self.post_order_seller1)
        self.assertHttpAccepted(resp_own)
        self.assertHttpUnauthorized(resp_other)
