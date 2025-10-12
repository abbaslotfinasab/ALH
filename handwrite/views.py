from django.views.generic import ListView
from rest_framework import viewsets

from .models import Snippet
from .serializers import SnippetWriteSerializer, SnippetReadSerializer


# Django Template Views
class SnippetListView(ListView):
    model = Snippet
    template_name = "handwrite.html"   # بعداً این تمپلیت رو می‌سازی
    context_object_name = "snippets"
    paginate_by = 12

    def get_queryset(self):
        qs = Snippet.objects.all().order_by("-order", "-created_at")
        # optional: filter by language or tag via GET params
        lang = self.request.GET.get("lang")
        if lang:
            qs = qs.filter(language=lang)
        return qs


class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all().order_by("-order", "-created_at")

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return SnippetWriteSerializer
        return SnippetReadSerializer