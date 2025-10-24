from django.urls import path, include, re_path
from . import views
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r"companies", CompanyViewSet, basename="company")
router.register(r"experiences", ExperienceViewSet, basename="experience")
router.register(r"projects", ProjectViewSet, basename="project")

app_name = 'experience'

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.experience, name='experience-view'),
    re_path(
        r'^experience/(?P<slug>[-\u0600-\u06FFa-zA-Z0-9_]+)/$',
        views.experience,
        name='experience-view-slug'
    )

]
