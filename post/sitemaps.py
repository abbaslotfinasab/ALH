from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from post.models import Post


class FeedSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Post.objects.filter(is_published=True)

    def location(self, obj):
        # اگر می‌خوای همه حالت‌ها رو داشته باشی، default فقط slug پست
        keyword_slug = obj.keywords.first().slug if obj.keywords.exists() else None
        if keyword_slug:
            return reverse('feed:feed-with-slug-or-keyword', kwargs={'combined_slug': f"{obj.slug}/{keyword_slug}"})
        return reverse('feed:feed-with-slug-or-keyword', kwargs={'combined_slug': obj.slug})

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else obj.created_at
