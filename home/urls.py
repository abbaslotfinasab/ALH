from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import AvailabilityViewSet

app_name = 'home'

router = DefaultRouter()
router.register(r'availability', AvailabilityViewSet)

urlpatterns = [
    path('', views.home_view, name='home-view'),
    path('api/', include(router.urls)),

]
