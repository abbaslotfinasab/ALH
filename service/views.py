from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from .models import Service, Technology
from .serializers import ServiceSerializer, TechnologySerializer



from django.shortcuts import render, get_object_or_404
from .models import Service

def service_view(request, id=None, slug=None):
    if id:
        service = get_object_or_404(Service, id=id)
    elif slug:
        service = get_object_or_404(Service, slug=slug)
    else:
        # اگه هیچکدوم نبود خطا بده
        return render(request, "404.html", status=404)

    return render(request, "service.html", {"service": service})




class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.prefetch_related("technologies").all()
    serializer_class = ServiceSerializer
    lookup_field = "slug"


class TechnologyViewSet(viewsets.ModelViewSet):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    lookup_field = "slug"
