from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'blogs'

router = DefaultRouter()
router.register(r'blog', BlogPostViewSet, basename='blog')

urlpatterns = [
    path('api/', include(router.urls)),  # 👈 اول بیار بالا
    path('', BlogPostListView.as_view(), name='blog-view'),
    re_path(r'^(?P<slug>[-\w\u0600-\u06FF]+)/$', BlogPostDetailView.as_view(), name='detail'),
]
