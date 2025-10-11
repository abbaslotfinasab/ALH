from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from .models import SEOPage, Keyword
from .serializers import SEOPageSerializer, KeyWordSerializer

class SEOPageViewSet(viewsets.ModelViewSet):
    queryset = SEOPage.objects.all().order_by("page_url")
    serializer_class = SEOPageSerializer

    @action(detail=False, methods=["get"], url_path="meta")
    def get_meta(self, request):
        """
        بر اساس path فعلی صفحه، متا دیتا (title, description, keywords) برگردون
        ?url=/about/
        """
        page_url = request.GET.get("url")
        if not page_url:
            return Response({"error": "url query param is required"}, status=400)

        seo_page = SEOPage.objects.prefetch_related("keywords").filter(page_url=page_url).first()
        if not seo_page:
            return Response({
                "title": "Default Title",
                "description": "Default description",
                "keywords": []
            })

        return Response({
            "title": seo_page.title,
            "description": seo_page.description,
            "keywords": [kw.name for kw in seo_page.keywords.all()]
        })

class KeywordViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all().order_by("name")
    serializer_class = KeyWordSerializer

