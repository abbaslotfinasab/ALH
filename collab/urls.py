from django.urls import path
from . import views

app_name = "collab"

urlpatterns = [
    path("", views.collab_page, name="collab-view"),     # صفحهٔ همکاری (GET)
    path("project/", views.submit_project, name="project"),  # POST فرم پروژه
    path("hire/", views.submit_hire, name="hire"),           # POST فرم استخدام
    path("thanks/", views.thanks, name="thanks"),            # صفحهٔ تشکر
]
