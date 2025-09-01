from django.contrib import admin
from .models import ProjectRequest, HireRequest

@admin.register(ProjectRequest)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name","email","project_type","created_at","is_read")
    list_filter  = ("project_type","created_at","is_read")
    search_fields= ("name","email","message","scopes","budget","ip")

@admin.register(HireRequest)
class HireAdmin(admin.ModelAdmin):
    list_display = ("name","email","role","mode","created_at","is_read")
    list_filter  = ("mode","created_at","is_read")
    search_fields= ("name","email","role","skills","message","ip")
