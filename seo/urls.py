from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = "seo"

router = DefaultRouter()


urlpatterns = [
    path('api/', include(router.urls)),
]
