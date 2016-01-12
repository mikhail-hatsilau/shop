from django.utils import timezone
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
import waffle


class UserAuthorization(Authorization):

    def read_list(self, object_list, bundle):
        if not bundle.request.user.is_superuser:
            return object_list.filter(pk=bundle.request.user.pk)

        return object_list

    def read_detail(self, object_list, bundle):
        if not bundle.request.user.is_superuser:
            return bundle.obj.pk == bundle.request.user.pk

        return True

    def create_list(self, object_list, bundle):
        if not bundle.request.user.is_superuser:
            raise Unauthorized()

        return object_list

    def create_detail(self, object_list, bundle):
        if not bundle.request.user.is_superuser:
            raise Unauthorized()

        return True

    def update_list(self, object_list, bundle):
        if not bundle.request.user.is_superuser:
            raise Unauthorized()

        return object_list

    def update_detail(self, object_list, bundle):
        if not bundle.request.user.is_superuser:
            raise Unauthorized()

        return True

    def delete_list(self, object_list, bundle):
        if not bundle.request.user.is_superuser:
            raise Unauthorized()

        return object_list

    def delete_detail(self, object_list, bundle):
        if not bundle.request.user.is_superuser:
            raise Unauthorized()

        return True


class CategoryAuthorization(Authorization):

    def read_list(self, object_list, bundle):
        return object_list

    def read_detail(self, object_list, bundle):
        return True

    def create_list(self, object_list, bundle):
        if not waffle.flag_is_active(bundle.request, 'is_seller'):
            raise Unauthorized()

        return object_list

    def create_detail(self, object_list, bundle):
        if not waffle.flag_is_active(bundle.request, 'is_seller'):
            raise Unauthorized()

        return True

    def update_list(self, object_list, bundle):
        if not waffle.flag_is_active(bundle.request, 'is_seller'):
            raise Unauthorized()

        return object_list

    def update_detail(self, object_list, bundle):
        if not waffle.flag_is_active(bundle.request, 'is_seller'):
            raise Unauthorized()

        return True

    def delete_list(self, object_list, bundle):
        if not waffle.flag_is_active(bundle.request, 'is_seller'):
            raise Unauthorized()

        return object_list

    def delete_detail(self, object_list, bundle):
        if not waffle.flag_is_active(bundle.request, 'is_seller'):
            raise Unauthorized()

        return True


class ProductAuthorization(Authorization):

    def read_list(self, object_list, bundle):
        if waffle.flag_is_active(bundle.request, 'is_seller') and not \
           bundle.request.user.is_superuser:
            allowed = []

            for obj in object_list:
                if obj.seller == bundle.request.user:
                    allowed.append(obj)

            return allowed

        if not waffle.flag_is_active(bundle.request, 'is_seller'):
            allowed = []
            current_date = timezone.now()
            for obj in object_list:
                if current_date >= obj.from_date and \
                   current_date <= obj.to_date:
                    allowed.append(obj)

            return allowed

        return object_list

    def read_detail(self, object_list, bundle):
        if waffle.flag_is_active(bundle.request, 'is_seller') and not \
           bundle.request.user.is_superuser:
            return bundle.obj.seller == bundle.request.user

        if not waffle.flag_is_active(bundle.request, 'is_seller'):
            current_date = timezone.now()
            return current_date >= bundle.obj.from_date and \
                current_date <= bundle.obj.to_date

        return True

    def create_list(self, object_list, bundle):
        if not waffle.flag_is_active(bundle.request, 'is_seller'):
            raise Unauthorized()
        elif not bundle.request.user.is_superuser:
            allowed = []

            for obj in object_list:
                if obj.seller == bundle.request.user:
                    allowed.append(obj)

            return allowed

        return object_list

    def create_detail(self, object_list, bundle):
        if not waffle.flag_is_active(bundle.request, 'is_seller'):
            raise Unauthorized()
        elif not bundle.request.user.is_superuser:
            return bundle.obj.seller == bundle.request.user

        return True

    def update_list(self, object_list, bundle):
        if not waffle.flag_is_active(bundle.request, 'is_seller'):
            raise Unauthorized()
        elif not bundle.request.user.is_superuser:
            allowed = []

            for obj in object_list:
                if obj.seller == bundle.request.user:
                    allowed.append(obj)

            return allowed

        return object_list

    def update_detail(self, object_list, bundle):
        if not waffle.flag_is_active(bundle.request, 'is_seller'):
            raise Unauthorized()
        elif not bundle.request.user.is_superuser:
            return bundle.obj.seller == bundle.request.user

        return True

    def delete_list(self, object_list, bundle):
        if not waffle.flag_is_active(bundle.request, 'is_seller'):
            raise Unauthorized()
        elif not bundle.request.user.is_superuser:
            allowed = []

            for obj in object_list:
                if obj.seller == bundle.request.user:
                    allowed.append(obj)

            return allowed

        return object_list

    def delete_detail(self, object_list, bundle):
        if not waffle.flag_is_active(bundle.request, 'is_seller'):
            raise Unauthorized()
        elif not bundle.request.user.is_superuser:
            return bundle.obj.seller == bundle.request.user

        return True


class OrderAuthorization(Authorization):

    def read_list(self, object_list, bundle):
        return object_list.filter(user=bundle.request.user)

    def read_detail(self, object_list, bundle):
        if not bundle.request.user.is_superuser:
            return bundle.obj.user == bundle.request.user

        return True

    def create_list(self, object_list, bundle):
        return object_list

    def create_detail(self, object_list, bundle):
        if not bundle.request.user.is_superuser:
            return bundle.obj.user == bundle.request.user

        return True

    def update_list(self, object_list, bundle):
        if not bundle.request.user.is_superuser:
            allowed = []

            for obj in object_list:
                if obj.user == bundle.request.user:
                    allowed.append(obj)

            return allowed

        return object_list

    def update_detail(self, object_list, bundle):
        if not bundle.request.user.is_superuser:
            return bundle.obj.user == bundle.request.user

        return True

    def delete_list(self, object_list, bundle):
        if not bundle.request.user.is_superuser:
            allowed = []

            for obj in object_list:
                if obj.user == bundle.request.user:
                    allowed.append(obj)

            return allowed

        return object_list

    def delete_detail(self, object_list, bundle):
        if not bundle.request.user.is_superuser:
            return bundle.obj.user == bundle.request.user

        return True
