from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from experience.models import Project, Experience


class ExperienceSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Experience.objects.all()  # اگر فیلد انتشار دارید

    def location(self, obj):
        return reverse('experience:experience-view')

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else obj.created_at

class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Project.objects.all()  # اگر فیلد انتشار دارید

    def location(self, obj):
        return reverse('experience:experience-view')

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else obj.created_at