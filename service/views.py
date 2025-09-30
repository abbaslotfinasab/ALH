from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from .models import Service, Technology
from .serializers import ServiceSerializer, TechnologySerializer



def service_view(request,pk):
    service = get_object_or_404(Service,pk=pk)
    return render(request, "service.html", {"service": service})



class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.prefetch_related("technologies").all()
    serializer_class = ServiceSerializer
    lookup_field = "slug"


class TechnologyViewSet(viewsets.ModelViewSet):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    lookup_field = "slug"
