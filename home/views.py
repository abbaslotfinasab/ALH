from django.shortcuts import render

from experience.models import Company


def home(request):
    companies = (
        Company.objects.all()
        .prefetch_related("experiences__projects")
        .order_by("name")
    )
    return render(request, "home.html", {"companies": companies})
