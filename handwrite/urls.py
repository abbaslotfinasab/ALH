from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'handwrite'

router = DefaultRouter()
router.register(r"snippets", SnippetViewSet, basename="snippet")

urlpatterns = [
    path("", SnippetListView.as_view(), name="handwrite-view"),
    path('api/', include(router.urls)),

]
