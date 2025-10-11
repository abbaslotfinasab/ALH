from django.contrib.sitemaps import Sitemap

from service.models import Service


class ServiceSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Service.objects.all()  # اگر فیلد انتشار دارید

    def location(self, obj):
        return obj.get_absolute_url()  # یا reverse('service:detail', args=[obj.slug])

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else obj.created_at
