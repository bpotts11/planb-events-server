from django.conf import settings
from django.urls.conf import include
from django import urls
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from planbapi.views import register_user, login_user, EventViewSet, ProductViewSet
from planbapi.models import *

# pylint: disable=invalid-name
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'events', EventViewSet, 'event')
router.register(r'products', ProductViewSet, 'product')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls,)),
    path('admin/', admin.site.urls),
    path('register', register_user),
    path('login', login_user),
    path('api-token-auth', obtain_auth_token),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework',)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
