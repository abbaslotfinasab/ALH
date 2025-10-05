from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"posts", BlogPostViewSet, basename="api-posts")
router.register(r"tags", TagViewSet, basename="api-tags")

app_name = "blogs"

urlpatterns = [
    # API
    path("api/", include(router.urls)),
    # Frontend
    path("", BlogListView.as_view(), name="blogs_view"),
    path("<slug:slug>/", BlogDetailView.as_view(), name="post_detail"),
]
