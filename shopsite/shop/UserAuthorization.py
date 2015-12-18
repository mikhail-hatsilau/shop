from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
from .models import User, Product, Order, Category
import waffle


class UserAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        model_class = object_list.model

        if model_class == User:
            if not waffle.flag_is_active(bundle.request, 'isSuperUser'):
                return object_list.filter(pk=bundle.request.user.pk)
        elif model_class == Order:
            return object_list.filter(user=bundle.request.user)

        return object_list

    def read_detail(self, object_list, bundle):
        model_class = object_list.model
        if model_class == User:
            if waffle.flag_is_active(bundle.request, 'isSuperUser'):
                return True
            else:
                return bundle.obj.pk == bundle.request.user.pk
        elif model_class == Order:
            if not waffle.flag_is_active(bundle.request, 'isSuperUser'):
                return bundle.obj.user == bundle.request.user

        return True

    def create_list(self, object_list, bundle):
        model_class = object_list.model

        if model_class == User:
            if not waffle.flag_is_active(bundle.request, 'isSuperUser'):
                raise Unauthorized()
        elif model_class == Product or model_class == Category:
            if not waffle.flag_is_active(bundle.request, 'isSeller'):
                raise Unauthorized()

        return object_list

    def create_detail(self, object_list, bundle):
        model_class = object_list.model

        if model_class == User:
            if not waffle.flag_is_active(bundle.request, 'isSuperUser'):
                raise Unauthorized()
        elif model_class == Product or model_class == Category:
            if not waffle.flag_is_active(bundle.request, 'isSeller'):
                raise Unauthorized()
        elif model_class == Order:
            return bundle.obj.user == bundle.request.user

        return True

    def update_list(self, object_list, bundle):
        model_class = object_list.model

        if model_class == Order:
            if not waffle.flag_is_active(bundle.request, 'isSuperUser'):
                allowed = []

                for obj in object_list:
                    if obj.user == bundle.request.user:
                        allowed.append(obj)

                return allowed
        elif model_class == User:
            if not waffle.flag_is_active(bundle.request, 'isSuperUser'):
                raise Unauthorized()
        elif model_class == Product or model_class == Category:
            if not waffle.flag_is_active(bundle.request, 'isSeller'):
                raise Unauthorized()

        return object_list

    def update_detail(self, object_list, bundle):
        model_class = object_list.model

        if model_class == User:
            if not waffle.flag_is_active(bundle.request, 'isSuperUser'):
                raise Unauthorized()
        elif model_class == Product or model_class == Category:
            if not waffle.flag_is_active(bundle.request, 'isSeller'):
                raise Unauthorized()
        elif model_class == Order:
            if not waffle.flag_is_active(bundle.request, 'isSuperUser'):
                return bundle.obj.user == bundle.request.user
        return True

    def delete_list(self, object_list, bundle):
        model_class = object_list.model

        if model_class == User:
            if not waffle.flag_is_active(bundle.request, 'isSuperUser'):
                raise Unauthorized()
        elif model_class == Product or model_class == Category:
            if not waffle.flag_is_active(bundle.request, 'isSeller'):
                raise Unauthorized()
        elif model_class == Order:
            if not waffle.flag_is_active(bundle.request, 'isSuperUser'):
                allowed = []

                for obj in object_list:
                    if obj.user == bundle.request.user:
                        allowed.append(obj)

                return allowed

        return object_list

    def delete_detail(self, object_list, bundle):
        model_class = object_list.model

        if model_class == User:
            if not waffle.flag_is_active(bundle.request, 'isSuperUser'):
                raise Unauthorized()
        elif model_class == Product or model_class == Category:
            if not waffle.flag_is_active(bundle.request, 'isSeller'):
                raise Unauthorized()
        elif model_class == Order:
            if not waffle.flag_is_active(bundle.request, 'isSuperUser'):
                return bundle.obj.user == bundle.request.user

        return True
