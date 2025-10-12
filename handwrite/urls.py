from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'handwrite'

router = DefaultRouter()
router.register(r"snippets", SnippetViewSet, basename="snippet")

urlpatterns = [
    path("", SnippetListView.as_view(), name="handwrite-view"),
    re_path(r"^(?P<slug>[-\w\u0600-\u06FF]+)/$", SnippetListView.as_view(), name="snippet-with-popup"),

    path('api/', include(router.urls)),

]
