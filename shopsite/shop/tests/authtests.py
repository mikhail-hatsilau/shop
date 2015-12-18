from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase
from waffle.models import Flag
import logging


logger = logging.getLogger(__name__)


class UserResourceTest(ResourceTestCase):
    def setUp(self):
        super(UserResourceTest, self).setUp()

        self.superUser = User.objects.create_user(username='admin',
                                                  password='qwerty')
        self.superUser.is_superuser = True
        self.staff = User.objects.create_user(username='staff',
                                              password='qwerty')
        self.staff.is_staff = True
        self.buyer = User.objects.create_user(username='user',
                                              password='qwerty')

        Flag.objects.create(name='isSuperUser', superusers=True)
        Flag.objects.create(name='isStaff',
                            staff=True,
                            superusers=True)

    def get_credentials(self, user):
        return self.create_basic(username=user.username,
                                 password=user.password)

    def test_get_list_super_user(self):
        auth = self.get_credentials(self.superUser)
        resp = self.api_client.get('/api/v1/users/',
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_get_list_staff(self):
        auth = self.get_credentials(self.staff)
        resp = self.api_client.get('/api/v1/users/',
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)

    def test_get_list_user(self):
        auth = self.get_credentials(self.buyer)
        resp = self.api_client.get('/api/v1/users/',
                                   format='json',
                                   authentication=auth)
        self.assertValidJSONResponse(resp)
