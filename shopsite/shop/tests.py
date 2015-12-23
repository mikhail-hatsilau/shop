from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase
from waffle.models import Flag
from datetime import date
from .models import Category, Product, Order


class UserCreator:
    def create_users(self):
        self.superName = 'admin'
        self.password = 'qwerty'
        self.superUser = User.objects.create_user(username=self.superName,
                                                  password=self.password)
        self.superUser.is_superuser = True
        self.superUser.save()

        self.staffName = 'staff'
        self.staff = User.objects.create_user(username=self.staffName,
                                              password=self.password)
        self.staff.is_staff = True
        self.staff.save()

        self.buyerName = 'buyer'
        self.buyer = User.objects.create_user(username=self.buyerName,
                                              password=self.password)

        self.details_url_super = '/api/v1/users/{0}/'.format(self.superUser.pk)
        self.details_url_staff = '/api/v1/users/{0}/'.format(self.staff.pk)
        self.details_url_buyer = '/api/v1/users/{0}/'.format(self.buyer.pk)

    def create_flags(self):
        Flag.objects.create(name='isSeller',
                            staff=True,
                            superusers=True)


class UserResourceTest(ResourceTestCase, UserCreator):
    def setUp(self):
        super(UserResourceTest, self).setUp()
        super(UserResourceTest, self).create_users()
        super(UserResourceTest, self).create_flags()

        self.data_user = {
            'username': 'person',
            'password': 'new'
        }

        self.url = '/api/v1/users/'

    def get_credentials(self, username, password):
        return self.create_basic(username=username,
                                 password=password)

    def test_get_users_list_super(self):
        auth = self.get_credentials(self.superName, self.password)
        resp = self.api_client.get(self.url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_get_users_list_staff(self):
        auth = self.get_credentials(self.staffName, self.password)
        resp = self.api_client.get(self.url,
                                   format='json',
                                   authentication=auth)
        deserialized_resp = self.deserialize(resp)

        self.assertValidJSONResponse(resp)
        self.assertEqual(len(deserialized_resp['objects']), 1)
        self.assertEqual(deserialized_resp['objects'][0]['id'], self.staff.pk)

    def test_get_users_list_buyer(self):
        auth = self.get_credentials(self.buyerName, self.password)
        resp = self.api_client.get(self.url,
                                   format='json',
                                   authentication=auth)
        deserialized_resp = self.deserialize(resp)

        self.assertValidJSONResponse(resp)
        self.assertEqual(len(deserialized_resp['objects']), 1)
        self.assertEqual(deserialized_resp['objects'][0]['id'], self.buyer.pk)

    def test_get_user_details_super(self):
        auth = self.get_credentials(self.superName, self.password)
        resp_own = self.api_client.get(self.details_url_super,
                                       format='json',
                                       authentication=auth)
        resp_other = self.api_client.get(self.details_url_buyer,
                                         format='json',
                                         authentication=auth)
        self.assertValidJSONResponse(resp_own)
        self.assertValidJSONResponse(resp_other)

    def test_get_user_details_staff(self):
        auth = self.get_credentials(self.staffName, self.password)
        resp_own = self.api_client.get(self.details_url_staff,
                                       format='json',
                                       authentication=auth)
        resp_other = self.api_client.get(self.details_url_buyer,
                                         format='json',
                                         authentication=auth)
        self.assertValidJSONResponse(resp_own)
        self.assertHttpUnauthorized(resp_other)

    def test_get_user_details_buyer(self):
        auth = self.get_credentials(self.buyerName, self.password)
        resp_own = self.api_client.get(self.details_url_buyer,
                                       format='json',
                                       authentication=auth)
        resp_other = self.api_client.get(self.details_url_staff,
                                         format='json',
                                         authentication=auth)
        self.assertValidJSONResponse(resp_own)
        self.assertHttpUnauthorized(resp_other)

    def test_post_users_super(self):
        auth = self.get_credentials(self.superName, self.password)
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=self.data_user,
                                    authentication=auth)
        self.assertHttpCreated(resp)

    def test_post_users_staff(self):
        auth = self.get_credentials(self.staffName, self.password)
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=self.data_user,
                                    authentication=auth)
        self.assertHttpUnauthorized(resp)

    def test_post_users_buyer(self):
        auth = self.get_credentials(self.buyerName, self.password)
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=self.data_user,
                                    authentication=auth)
        self.assertHttpUnauthorized(resp)

    def test_update_user_super(self):
        auth = self.get_credentials(self.superName, self.password)
        resp = self.api_client.put(self.details_url_buyer,
                                   format='json',
                                   data={},
                                   authentication=auth)
        self.assertHttpAccepted(resp)

    def test_update_user_staff(self):
        auth = self.get_credentials(self.staffName, self.password)
        resp = self.api_client.put(self.details_url_buyer,
                                   format='json',
                                   data={},
                                   authentication=auth)
        self.assertHttpUnauthorized(resp)

    def test_update_user_buyer(self):
        auth = self.get_credentials(self.buyerName, self.password)
        resp = self.api_client.put(self.details_url_staff,
                                   format='json',
                                   data={},
                                   authentication=auth)
        self.assertHttpUnauthorized(resp)

    def test_delete_user_staff(self):
        auth = self.get_credentials(self.staffName, self.password)
        resp = self.api_client.delete(self.details_url_buyer,
                                      format='json',
                                      authentication=auth)
        self.assertHttpUnauthorized(resp)

    def test_delete_user_buyer(self):
        auth = self.get_credentials(self.buyerName, self.password)
        resp = self.api_client.delete(self.details_url_staff,
                                      format='json',
                                      authentication=auth)
        self.assertHttpUnauthorized(resp)


class ProductResourceTest(ResourceTestCase, UserCreator):
    def setUp(self):
        super(ProductResourceTest, self).setUp()
        super(ProductResourceTest, self).create_users()
        super(ProductResourceTest, self).create_flags()

        self.category = Category.objects.create(name='Books')

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
        auth = self.get_credentials(self.superName, self.password)
        resp = self.api_client.get(self.url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_get_products_list_staff(self):
        auth = self.get_credentials(self.staffName, self.password)
        resp = self.api_client.get(self.url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_get_products_list_buyer(self):
        auth = self.get_credentials(self.buyerName, self.password)
        resp = self.api_client.get(self.url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_get_product_details_super(self):
        auth = self.get_credentials(self.superName, self.password)
        resp = self.api_client.get(self.details_url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_get_product_details_staff(self):
        auth = self.get_credentials(self.staffName, self.password)
        resp = self.api_client.get(self.details_url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_get_product_details_buyer(self):
        auth = self.get_credentials(self.buyerName, self.password)
        resp = self.api_client.get(self.details_url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_post_products_super(self):
        auth = self.get_credentials(self.superName, self.password)
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=self.post_add_product,
                                    authentication=auth)
        self.assertHttpCreated(resp)

    def test_post_products_staff(self):
        auth = self.get_credentials(self.staffName, self.password)
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=self.post_add_product,
                                    authentication=auth)
        self.assertHttpCreated(resp)

    def test_post_products_buyer(self):
        auth = self.get_credentials(self.buyerName, self.password)
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=self.post_add_product,
                                    authentication=auth)
        self.assertHttpUnauthorized(resp)

    def test_update_product_super(self):
        auth = self.get_credentials(self.superName, self.password)
        resp = self.api_client.put(self.details_url,
                                   format='json',
                                   data={},
                                   authentication=auth)
        self.assertHttpOK(resp)

    def test_update_product_staff(self):
        auth = self.get_credentials(self.staffName, self.password)
        resp = self.api_client.put(self.details_url,
                                   format='json',
                                   data={},
                                   authentication=auth)
        self.assertHttpOK(resp)

    def test_update_product_buyer(self):
        auth = self.get_credentials(self.buyerName, self.password)
        resp = self.api_client.put(self.details_url,
                                   format='json',
                                   data={},
                                   authentication=auth)
        self.assertHttpUnauthorized(resp)

    def test_delete_product_super(self):
        auth = self.get_credentials(self.superName, self.password)
        resp = self.api_client.delete(self.details_url,
                                      format='json',
                                      authentication=auth)
        self.assertHttpAccepted(resp)

    def test_delete_product_staff(self):
        auth = self.get_credentials(self.staffName, self.password)
        resp = self.api_client.delete(self.details_url,
                                      format='json',
                                      authentication=auth)
        self.assertHttpAccepted(resp)

    def test_delete_product_buyer(self):
        auth = self.get_credentials(self.buyerName, self.password)
        resp = self.api_client.delete(self.details_url,
                                      format='json',
                                      authentication=auth)
        self.assertHttpUnauthorized(resp)


class CategoryResourceTest(ResourceTestCase, UserCreator):
    def setUp(self):
        super(CategoryResourceTest, self).setUp()
        super(CategoryResourceTest, self).create_users()
        super(CategoryResourceTest, self).create_flags()

        self.category = Category.objects.create(name='Books')

        self.url = '/api/v1/categories/'
        self.details_url = '/api/v1/categories/{0}/'.format(self.category.pk)

        self.post_category = {
            'name': 'product',
        }

    def get_credentials(self, username, password):
        return self.create_basic(username=username,
                                 password=password)

    def test_get_categories_list_super(self):
        auth = self.get_credentials(self.superName, self.password)
        resp = self.api_client.get(self.url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_get_categories_list_staff(self):
        auth = self.get_credentials(self.staffName, self.password)
        resp = self.api_client.get(self.url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_get_categories_list_buyer(self):
        auth = self.get_credentials(self.buyerName, self.password)
        resp = self.api_client.get(self.url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_get_category_details_super(self):
        auth = self.get_credentials(self.superName, self.password)
        resp = self.api_client.get(self.details_url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_get_category_details_staff(self):
        auth = self.get_credentials(self.staffName, self.password)
        resp = self.api_client.get(self.details_url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_get_category_details_buyer(self):
        auth = self.get_credentials(self.buyerName, self.password)
        resp = self.api_client.get(self.details_url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_post_categories_super(self):
        auth = self.get_credentials(self.superName, self.password)
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=self.post_category,
                                    authentication=auth)
        self.assertHttpCreated(resp)

    def test_post_categories_seller(self):
        auth = self.get_credentials(self.staffName, self.password)
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=self.post_category,
                                    authentication=auth)
        self.assertHttpCreated(resp)

    def test_post_categories_buyer(self):
        auth = self.get_credentials(self.buyerName, self.password)
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=self.post_category,
                                    authentication=auth)
        self.assertHttpUnauthorized(resp)

    def test_update_category_super(self):
        auth = self.get_credentials(self.superName, self.password)
        resp = self.api_client.put(self.details_url,
                                   format='json',
                                   data={},
                                   authentication=auth)
        self.assertHttpAccepted(resp)

    def test_update_category_staff(self):
        auth = self.get_credentials(self.staffName, self.password)
        resp = self.api_client.put(self.details_url,
                                   format='json',
                                   data={},
                                   authentication=auth)
        self.assertHttpAccepted(resp)

    def test_update_category_buyer(self):
        auth = self.get_credentials(self.buyerName, self.password)
        resp = self.api_client.put(self.details_url,
                                   format='json',
                                   data={},
                                   authentication=auth)
        self.assertHttpUnauthorized(resp)

    def test_delete_category_super(self):
        auth = self.get_credentials(self.superName, self.password)
        resp = self.api_client.delete(self.details_url,
                                      format='json',
                                      authentication=auth)
        self.assertHttpAccepted(resp)

    def test_delete_category_staff(self):
        auth = self.get_credentials(self.staffName, self.password)
        resp = self.api_client.delete(self.details_url,
                                      format='json',
                                      authentication=auth)
        self.assertHttpAccepted(resp)

    def test_delete_category_buyer(self):
        auth = self.get_credentials(self.buyerName, self.password)
        resp = self.api_client.delete(self.details_url,
                                      format='json',
                                      authentication=auth)
        self.assertHttpUnauthorized(resp)


class OrderResourceTest(ResourceTestCase, UserCreator):
    def setUp(self):
        super(OrderResourceTest, self).setUp()
        super(OrderResourceTest, self).create_users()
        super(OrderResourceTest, self).create_flags()

        self.category = Category.objects.create(name='Books')
        self.product = Product.objects.create(name='Js',
                                              discription='bla',
                                              price=120,
                                              category=self.category)
        self.superOrder = Order.objects.create(user=self.superUser,
                                               product=self.product,
                                               date=date.today())
        self.staffOrder = Order.objects.create(user=self.staff,
                                               product=self.product,
                                               date=date.today())
        self.buyerOrder = Order.objects.create(user=self.buyer,
                                               product=self.product,
                                               date=date.today())
        self.url = '/api/v1/orders/'

        self.details_super = '/api/v1/orders/{0}/'.format(self.superOrder.pk)
        self.details_staff = '/api/v1/orders/{0}/'.format(self.staffOrder.pk)
        self.details_buyer = '/api/v1/orders/{0}/'.format(self.buyerOrder.pk)

        self.post_order_super = {
            'user': self.details_url_super,
            'product': '/api/v1/products/{0}/'.format(self.product.pk),
            'date': date(2015, 07, 05)
        }

        self.post_order_staff = {
            'user': self.details_url_staff,
            'product': '/api/v1/products/{0}/'.format(self.product.pk),
            'date': date(2015, 07, 05)
        }

        self.post_order_buyer = {
            'user': self.details_url_buyer,
            'product': '/api/v1/products/{0}/'.format(self.product.pk),
            'date': date(2015, 07, 05)
        }

    def get_credentials(self, username, password):
        return self.create_basic(username=username,
                                 password=password)

    def test_get_orders_list_own(self):
        auth = self.get_credentials(self.buyerName, self.password)
        resp = self.api_client.get(self.url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

        deserialized_obj = self.deserialize(resp)

        for order in deserialized_obj['objects']:
            self.assertEqual(order['user']['resource_uri'],
                             self.details_url_buyer)

    def test_get_orders_list_super(self):
        auth = self.get_credentials(self.superName, self.password)
        resp = self.api_client.get(self.url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_get_orders_list_staff(self):
        auth = self.get_credentials(self.staffName, self.password)
        resp = self.api_client.get(self.url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_get_orders_list_buyer(self):
        auth = self.get_credentials(self.buyerName, self.password)
        resp = self.api_client.get(self.url,
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_get_order_details_super(self):
        auth = self.get_credentials(self.superName, self.password)
        resp_own = self.api_client.get(self.details_super,
                                       format='json',
                                       authentication=auth)
        resp_other = self.api_client.get(self.details_buyer,
                                         format='json',
                                         authentication=auth)
        self.assertValidJSONResponse(resp_own)
        self.assertValidJSONResponse(resp_other)

    def test_get_order_details_staff(self):
        auth = self.get_credentials(self.staffName, self.password)
        resp_own = self.api_client.get(self.details_staff,
                                       format='json',
                                       authentication=auth)
        resp_other = self.api_client.get(self.details_buyer,
                                         format='json',
                                         authentication=auth)
        self.assertValidJSONResponse(resp_own)
        self.assertHttpUnauthorized(resp_other)

    def test_get_order_details_buyer(self):
        auth = self.get_credentials(self.buyerName, self.password)
        resp_own = self.api_client.get(self.details_buyer,
                                       format='json',
                                       authentication=auth)
        resp_other = self.api_client.get(self.details_staff,
                                         format='json',
                                         authentication=auth)
        self.assertValidJSONResponse(resp_own)
        self.assertHttpUnauthorized(resp_other)

    def test_post_orders_super(self):
        auth = self.get_credentials(self.superName, self.password)
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

    def test_post_orders_staff(self):
        auth = self.get_credentials(self.staffName, self.password)
        resp_own = self.api_client.post(self.url,
                                        format='json',
                                        data=self.post_order_staff,
                                        authentication=auth)
        resp_other = self.api_client.post(self.url,
                                          format='json',
                                          data=self.post_order_buyer,
                                          authentication=auth)
        self.assertHttpCreated(resp_own)
        self.assertHttpUnauthorized(resp_other)

    def test_post_orders_buyer(self):
        auth = self.get_credentials(self.buyerName, self.password)
        resp_own = self.api_client.post(self.url,
                                        format='json',
                                        data=self.post_order_buyer,
                                        authentication=auth)
        resp_other = self.api_client.post(self.url,
                                          format='json',
                                          data=self.post_order_staff,
                                          authentication=auth)
        self.assertHttpCreated(resp_own)
        self.assertHttpUnauthorized(resp_other)

    def test_update_orders_super(self):
        auth = self.get_credentials(self.superName, self.password)
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

    def test_update_orders_staff(self):
        auth = self.get_credentials(self.staffName, self.password)
        resp_own = self.api_client.put(self.details_staff,
                                       format='json',
                                       data={},
                                       authentication=auth)
        resp_other = self.api_client.put(self.details_buyer,
                                         format='json',
                                         data=self.post_order_staff,
                                         authentication=auth)
        self.assertHttpAccepted(resp_own)
        self.assertHttpUnauthorized(resp_other)

    def test_update_orders_buyer(self):
        auth = self.get_credentials(self.buyerName, self.password)
        resp_own = self.api_client.put(self.details_buyer,
                                       format='json',
                                       data={},
                                       authentication=auth)
        resp_other = self.api_client.put(self.details_staff,
                                         format='json',
                                         data={},
                                         authentication=auth)
        self.assertHttpAccepted(resp_own)
        self.assertHttpUnauthorized(resp_other)

    def test_delete_orders_super(self):
        auth = self.get_credentials(self.superName, self.password)
        resp_own = self.api_client.delete(self.details_super,
                                          format='json',
                                          data={},
                                          authentication=auth)
        resp_other = self.api_client.delete(self.details_buyer,
                                            format='json',
                                            data=self.post_order_staff,
                                            authentication=auth)
        self.assertHttpAccepted(resp_own)
        self.assertHttpAccepted(resp_other)

    def test_delete_orders_staff(self):
        auth = self.get_credentials(self.staffName, self.password)
        resp_own = self.api_client.delete(self.details_staff,
                                          format='json',
                                          data={},
                                          authentication=auth)
        resp_other = self.api_client.delete(self.details_buyer,
                                            format='json',
                                            data=self.post_order_staff,
                                            authentication=auth)
        self.assertHttpAccepted(resp_own)
        self.assertHttpUnauthorized(resp_other)

    def test_delete_orders_buyer(self):
        auth = self.get_credentials(self.buyerName, self.password)
        resp_own = self.api_client.delete(self.details_buyer,
                                          format='json',
                                          data={},
                                          authentication=auth)
        resp_other = self.api_client.delete(self.details_staff,
                                            format='json',
                                            data=self.post_order_staff,
                                            authentication=auth)
        self.assertHttpAccepted(resp_own)
        self.assertHttpUnauthorized(resp_other)
