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

@require_POST
def submit_project(request):
    form = ProjectForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.error(request, "خطا در ارسال فرم پروژه. لطفاً موارد را بررسی کنید.")
        return redirect(reverse("collab:page") + "#project-form")

    ip, ua = _client_meta(request)
    scopes_csv = ",".join(form.cleaned_data.get("scope", []))
    obj = ProjectRequest.objects.create(
        name=form.cleaned_data["name"],
        email=form.cleaned_data["email"],
        phone=form.cleaned_data.get("phone",""),
        project_type={"web":"web","موبایل":"mobile","هر دو":"both"}.get(form.cleaned_data["type"], form.cleaned_data["type"]),
        scopes=scopes_csv,
        deadline=form.cleaned_data.get("deadline"),
        budget=form.cleaned_data.get("budget",""),
        message=form.cleaned_data["message"],
        nda=form.cleaned_data.get("nda", False),
        ip=ip, user_agent=ua,
    )

    # ایمیل اطلاع‌رسانی
    subject = "درخواست پروژه جدید"
    body = (
        f"نام: {obj.name}\n"
        f"ایمیل: {obj.email}\n"
        f"تلفن: {obj.phone}\n"
        f"نوع پروژه: {obj.project_type}\n"
        f"دامنه کار: {obj.scopes}\n"
        f"موعد: {obj.deadline}\n"
        f"بودجه: {obj.budget}\n\n"
        f"پیام:\n{strip_tags(obj.message)}\n\n"
        f"IP: {obj.ip}\nUA: {obj.user_agent}\n"
    )
    try:
        send_mail(subject, body, None, ["info@abbaslotfinasab.ir"], fail_silently=True)
    except Exception:
        pass

    messages.success(request, "درخواست پروژه با موفقیت ثبت شد. حداکثر تا ۲۴ ساعت کاری پاسخ می‌دهم.")
    return redirect("collab:thanks")

@require_POST
def submit_hire(request):
    form = HireForm(request.POST)
    if not form.is_valid():
        messages.error(request, "خطا در ارسال درخواست مصاحبه. لطفاً موارد را بررسی کنید.")
        return redirect(reverse("collab:page") + "#hire-form")

    ip, ua = _client_meta(request)
    obj = HireRequest.objects.create(
        name=form.cleaned_data["name"],
        email=form.cleaned_data["email"],
        role=form.cleaned_data.get("role",""),
        mode=form.cleaned_data.get("mode",""),
        skills=form.cleaned_data.get("skills",""),
        message=form.cleaned_data.get("message",""),
        ip=ip, user_agent=ua,
    )

    subject = "درخواست مصاحبه جدید"
    body = (
        f"نام: {obj.name}\n"
        f"ایمیل: {obj.email}\n"
        f"نقش: {obj.role}\n"
        f"نوع همکاری: {obj.mode}\n"
        f"مهارت‌ها: {obj.skills}\n\n"
        f"پیام:\n{strip_tags(obj.message)}\n\n"
        f"IP: {obj.ip}\nUA: {obj.user_agent}\n"
    )
    try:
        send_mail(subject, body, None, ["info@abbaslotfinasab.ir"], fail_silently=True)
    except Exception:
        pass

    messages.success(request, "درخواست مصاحبه ثبت شد. هماهنگی زمان جلسه از طریق ایمیل انجام می‌شود.")
    return redirect("collab:thanks")

def thanks(request):
    return render(request, "collab_thanks.html")
