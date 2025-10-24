from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from post.models import Post


class FeedSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Post.objects.all()  # اگر فیلد انتشار دارید

    def location(self, obj):
        return reverse('post:feed-view')  # صفحه اصلی

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else obj.created_at
