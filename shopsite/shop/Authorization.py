from django.utils import timezone
from django.db.models import Q
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
            return object_list.filter(seller=bundle.request.user)

        if not waffle.flag_is_active(bundle.request, 'is_seller'):
            current_date = timezone.now()
            return object_list.filter(Q(Q(from_date__lte=current_date,
                                          to_date__gte=current_date) &
                                        Q(from_date__isnull=False,
                                          to_date__isnull=False)) |
                                      Q(Q(from_date__isnull=True,
                                          to_date__isnull=False) &
                                        Q(to_date__gte=current_date)) |
                                      Q(Q(from_date__isnull=False,
                                          to_date__isnull=True) &
                                        Q(from_date__lte=current_date)) |
                                      Q(from_date__isnull=True,
                                        to_date__isnull=True))
        return object_list

    def read_detail(self, object_list, bundle):
        if waffle.flag_is_active(bundle.request, 'is_seller') and not \
           bundle.request.user.is_superuser:
            return bundle.obj.seller == bundle.request.user

        if not waffle.flag_is_active(bundle.request, 'is_seller'):
            current_date = timezone.now()
            if bundle.obj.from_date is not None and \
               bundle.obj.to_date is not None:
                return current_date >= bundle.obj.from_date and \
                    current_date <= bundle.obj.to_date
            elif bundle.obj.from_date is None and \
                    bundle.obj.to_date is not None:
                    return current_date <= bundle.obj.to_date
            elif bundle.obj.from_date is not None and \
                    bundle.obj.to_date is None:
                    return current_date >= bundle.obj.from_date

        return True

    def create_list(self, object_list, bundle):
        if not waffle.flag_is_active(bundle.request, 'is_seller'):
            raise Unauthorized()
        elif not bundle.request.user.is_superuser:
            return object_list.filter(seller=bundle.request.user)

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
            return object_list.filter(seller=bundle.request.user)

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
            return object_list.filter(seller=bundle.request.user)

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
            return object_list.filter(user=bundle.request.user)
        return object_list

    def update_detail(self, object_list, bundle):
        if not bundle.request.user.is_superuser:
            return bundle.obj.user == bundle.request.user

        return True

    def delete_list(self, object_list, bundle):
        if not bundle.request.user.is_superuser:
            return object_list.filter(user=bundle.request.user)

        return object_list

    def delete_detail(self, object_list, bundle):
        if not bundle.request.user.is_superuser:
            return bundle.obj.user == bundle.request.user

        return True
