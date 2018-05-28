from django.urls import path, include
from rest_framework import routers
from .views import CoinViewSet


router = routers.DefaultRouter()
router.register(r'', CoinViewSet)

urlpatterns = [
    path('', include(router.urls), name='coins'),
]
