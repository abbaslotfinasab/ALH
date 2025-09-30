from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import ServiceViewSet, TechnologyViewSet


app_name='service'


router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'technologies', TechnologyViewSet, basename='technology')


urlpatterns = [
    path('<int:pk>/', views.service_view, name='service-view'),
    path('api/', include(router.urls)),

]
