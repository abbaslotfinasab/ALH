from django.shortcuts import render
from django.views.decorators.http import require_POST

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
    ua = request.META.get("HTTP_USER_AGENT", "")[:500]
    return ip, ua


from django.http import JsonResponse


@require_POST
def submit_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ProjectRequest.objects.create(
                name=data["name"],
                email=data["email"],
                phone=data.get("phone", ""),
                project_type=data["type"],
                scopes=",".join(data.get("scope", [])),
                deadline=data.get("deadline"),
                budget=data.get("budget", ""),
                message=data["message"],
                nda=data.get("nda", False),
                ip=request.META.get("REMOTE_ADDR"),
                user_agent=request.META.get("HTTP_USER_AGENT"),
            )
            return JsonResponse({"success": True, "message": "درخواست با موفقیت ثبت شد."})
        else:
            # تبدیل خطاها به دیکشنری خوانا
            errors = {field: error_list[0] for field, error_list in form.errors.items()}
            return JsonResponse({"success": False, "errors": errors}, status=400)
    return JsonResponse({"error": "Invalid method"}, status=405)


@require_POST
def submit_hire(request):
    if request.method == "POST":
        form = HireForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            HireRequest.objects.create(
                name=data["name"],
                email=data["email"],
                phone=data.get("phone", ""),
                role=data["role"],
                mode=data["mode"],
                skills=data["skills"],
                message=data["message"],
                ip=request.META.get("REMOTE_ADDR"),
                user_agent=request.META.get("HTTP_USER_AGENT"),
            )
            return JsonResponse({"success": True, "message": "درخواست با موفقیت ثبت شد."})
        else:
            errors = {field: error_list[0] for field, error_list in form.errors.items()}
            return JsonResponse({"success": False, "errors": errors}, status=400)
    return JsonResponse({"error": "Invalid method"}, status=405)


def thanks(request):
    return render(request, "collab_thanks.html")


def request_list(request):
    project_requests = ProjectRequest.objects.order_by('-created_at')[:50]
    hire_requests = HireRequest.objects.order_by('-created_at')[:50]
    return render(request, "request_list.html", {
        "project_requests": project_requests,
        "hire_requests": hire_requests
    })
