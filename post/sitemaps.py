from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from post.models import Post


class FeedSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return [None] + list(Post.objects.filter(is_published=True))

    def location(self, obj):
        if obj is None:
            # صفحه اصلی feed
            return reverse('post:feed-view')  # /post/ یا /feed/
        # اگر می‌خوای همه حالت‌ها رو داشته باشی، default فقط slug پست
        keyword_slug = obj.keywords.first().slug if obj.keywords.exists() else None
        if keyword_slug:
            return reverse('post:feed-with-slug-or-keyword', kwargs={'combined_slug': f"{obj.slug}/{keyword_slug}"})
        return reverse('post:feed-with-slug-or-keyword', kwargs={'combined_slug': obj.slug})

    def lastmod(self, obj):
        if obj is None:
            # آخرین بروزرسانی صفحه feed = آخرین پست منتشر شده
            last_post = Post.objects.filter(is_published=True).order_by('-updated_at').first()
            if last_post:
                return last_post.updated_at if hasattr(last_post, 'updated_at') else last_post.created_at
            return None  # اگه پستی نبود
        return obj.updated_at if hasattr(obj, 'updated_at') else obj.created_at
