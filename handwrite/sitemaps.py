from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Snippet

class SnippetSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        # None اضافه کنیم برای URL اصلی صفحه دست‌خط‌ها
        return [None] + list(Snippet.objects.filter(is_published=True))

    def location(self, obj):
        if obj is None:
            # URL اصلی لیست Snippet
            return reverse('handwrite:handwrite-view')
        # URL منحصر به فرد برای هر Snippet با slug
        return reverse('handwrite:snippet-with-popup', kwargs={'slug': obj.slug})

    def lastmod(self, obj):
        if obj is None:
            # آخرین بروزرسانی صفحه اصلی = آخرین Snippet منتشر شده
            last_snippet = Snippet.objects.filter(is_published=True).order_by('-updated_at').first()
            return last_snippet.updated_at if last_snippet else None
        return obj.updated_at if hasattr(obj, 'updated_at') else obj.created_at
