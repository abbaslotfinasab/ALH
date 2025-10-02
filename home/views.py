from django.shortcuts import render
from rest_framework import viewsets

from experience.models import Company
from home.models import Availability
from home.serializers import AvailabilitySerializer
from service.models import Service


def home_view(request):
    companies = (
        Company.objects.all()
        .prefetch_related("experiences__projects")
        .order_by("name")
    )

    services = (
        Service.objects.all()
        .prefetch_related("technologies")
        .order_by("id")
    )
    return render(request, "home.html", {"companies": companies, "services": services})


class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all().order_by('-updated_at')
    serializer_class = AvailabilitySerializer