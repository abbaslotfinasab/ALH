from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r"companies", CompanyViewSet, basename="company")
router.register(r"experiences", ExperienceViewSet, basename="experience")
router.register(r"projects", ProjectViewSet, basename="project")

app_name = 'experience'

urlpatterns = [
    path('', views.experience, name='experience-view'),
    path('api/', include(router.urls)),

]
