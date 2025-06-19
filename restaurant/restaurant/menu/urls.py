from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'dishes', views.DishViewSet, basename='dish')
router.register(r'orders', views.OrderViewSet, basename='order')

urlpatterns = router.urls
