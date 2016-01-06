"""shopsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls.static import static
from tastypie.api import Api
from shop.api.resources import ProductResource, OrderResource
from shop.api.resources import UserResource, CategoryResource
from shop.api.resources import LoginResource

api_v1 = Api(api_name='v1')
api_v1.register(ProductResource())
api_v1.register(OrderResource())
api_v1.register(UserResource())
api_v1.register(CategoryResource())
api_v1.register(LoginResource())

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^api/', include(api_v1.urls))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
