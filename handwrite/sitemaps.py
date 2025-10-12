from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Snippet

class SnippetSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Snippet.objects.all()  # اگر فیلد انتشار دارید

    def location(self, obj):
        return reverse('handwrite:handwrite-view')

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else obj.created_at
