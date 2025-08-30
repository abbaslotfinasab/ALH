from django.contrib import admin
from .models import Company, Experience, Project

class ProjectInline(admin.TabularInline):
    model = Project
    extra = 0

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("company", "title", "start_date", "end_date")
    list_filter  = ("company", "employment_type")
    search_fields = ("title", "company__name", "description")
    inlines = [ProjectInline]

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "website", "is_active")
    search_fields = ("name",)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "experience", "role")
    list_filter  = ("experience__company",)
    search_fields = ("name", "description", "technologies")
