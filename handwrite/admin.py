# handwrite/admin.py
from django.contrib import admin
from .models import Snippet

@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ("title", "language", "project_name", "is_published", "created_at")
    search_fields = ("title", "short_description", "full_code", "project_name")
    list_filter = ("language", "is_published")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-created_at",)
