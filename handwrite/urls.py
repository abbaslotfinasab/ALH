from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'handwrite'

router = DefaultRouter()
# router.register(r'availability', AvailabilityViewSet)

urlpatterns = [
    path('', handwrite_view, name='handwrite-view'),
    path('api/', include(router.urls)),

]
