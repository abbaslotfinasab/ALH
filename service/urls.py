from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from . import views
from .views import ServiceViewSet, TechnologyViewSet


app_name='service'


router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'technologies', TechnologyViewSet, basename='technology')


urlpatterns = [
    path('api/', include(router.urls)),
    path('<int:pk>/', views.service_view, name='service-view'),

    re_path(r'^(?P<slug>[-\w\u0600-\u06FF]+)/$', views.service_view, name='service-view'),

]
