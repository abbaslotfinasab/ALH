from django.shortcuts import render

from experience.models import Company
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
