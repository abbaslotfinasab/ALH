from django.contrib.sitemaps import Sitemap

from .models import Blog


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Blog.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()  # یا reverse('service:detail', args=[obj.slug])

    def lastmod(self, obj):
        return obj.published_date


