from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags

from .forms import ProjectForm, HireForm
from .models import ProjectRequest, HireRequest

def collab_page(request):
    # صفحه همکاری + فرم‌ها در یک صفحه
    return render(request, "collab.html", {
        "project_form": ProjectForm(),
        "hire_form": HireForm(),
    })

def _client_meta(request):
    # گرفتن IP و UA
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    ip = (xff.split(",")[0].strip() if xff else request.META.get("REMOTE_ADDR"))
    ua = request.META.get("HTTP_USER_AGENT","")[:500]
    return ip, ua

def submit_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ProjectRequest.objects.create(
                name=data["name"],
                email=data["email"],
                phone=data["phone"],
                project_type=data["type"],
                scopes=",".join(data.get("scope", [])),
                deadline=data["deadline"],
                budget=data["budget"],
                message=data["message"],
                nda=data["nda"],
                ip=request.META.get("REMOTE_ADDR"),
                user_agent=request.META.get("HTTP_USER_AGENT"),
            )
            return redirect("collab:thanks")
    else:
        form = ProjectForm()
    return render(request, "collab.html", {"form": form})

@require_POST
def submit_hire(request):
    if request.method == "POST":
        form = HireForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            HireRequest.objects.create(
                name=data["name"],
                email=data["email"],
                role=data["role"],
                mode=data["mode"],
                skills=data["skills"],
                message=data["message"],
                ip=request.META.get("REMOTE_ADDR"),
                user_agent=request.META.get("HTTP_USER_AGENT"),
            )
            return redirect("collab:thanks")
    else:
        form = HireForm()
    return render(request, "collab.html", {"form": form})


def thanks(request):
    return render(request, "collab_thanks.html")


def request_list(request):
    project_requests = ProjectRequest.objects.order_by('-created_at')[:50]
    hire_requests = HireRequest.objects.order_by('-created_at')[:50]
    return render(request, "request_list.html", {
        "project_requests": project_requests,
        "hire_requests": hire_requests
    })