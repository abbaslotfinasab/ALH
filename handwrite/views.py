from rest_framework import viewsets

from .models import Snippet
from .serializers import SnippetWriteSerializer, SnippetReadSerializer

from django.conf import settings
from django.db.models import Q
from django.views.generic import ListView
from seo.models import SEOPage, Keyword


class SnippetListView(ListView):
    model = Snippet
    template_name = "handwrite.html"
    context_object_name = "snippets"
    paginate_by = 12

    def get_queryset(self):
        qs = Snippet.objects.filter(is_published=True).order_by("-order", "-created_at")

        # فیلتر براساس زبان برنامه‌نویسی
        lang = self.request.GET.get("lang")
        if lang:
            qs = qs.filter(language=lang)

        # فیلتر جستجو (اختیاری)
        search = self.request.GET.get("search")
        if search:
            qs = qs.filter(
                Q(title__icontains=search)
                | Q(short_description__icontains=search)
                | Q(full_code__icontains=search)
                | Q(lesson__icontains=search)
            )

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_path = self.request.path

        # مرحله ۱: بررسی اینکه سئوی اختصاصی برای این صفحه داریم یا نه
        seo_data = SEOPage.objects.filter(page_url=current_path).first()

        if seo_data:
            context["meta_title"] = seo_data.title
            context["meta_description"] = seo_data.description
            context["meta_keywords"] = ", ".join([
                kw.name for kw in seo_data.keywords.filter(category=Keyword.Category.HANDWRITING)
            ])
        else:
            # fallback از تنظیمات عمومی
            default = settings.SEO.get("handwrite", settings.SEO["default"])
            context["meta_title"] = default["title"]
            context["meta_description"] = default["description"]
            context["meta_keywords"] = ", ".join(default["keywords"])

        # بقیه داده‌ها
        context["canonical_url"] = self.request.build_absolute_uri()
        context["total_snippets"] = Snippet.objects.filter(is_published=True).count()
        context["keywords"] = Keyword.objects.filter(category=Keyword.Category.HANDWRITING).order_by("name")

        return context

class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all().order_by("-order", "-created_at")

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return SnippetWriteSerializer
        return SnippetReadSerializer