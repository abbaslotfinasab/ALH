from django.urls import path, include
from rest_framework.routers import DefaultRouter

from seo.views import SEOPageViewSet, KeywordViewSet

app_name = "seo"

router = DefaultRouter()
router.register(r'seo-pages', SEOPageViewSet, basename='seo-page')
router.register(r'keywords', KeywordViewSet, basename='keyword')


urlpatterns = [
    path('api/', include(router.urls)),
]
