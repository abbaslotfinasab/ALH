# posts/api_urls.py
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import *

app_name = "post"

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(r"tags", TagViewSet, basename="tag")
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = [
    path('api/', include(router.urls)),
    path("", feed, name="feed-view"),  # فید
    re_path(r"^(?P<slug>[-\w\u0600-\u06FF]+)/$", feed, name="feed-with-popup"),
]
