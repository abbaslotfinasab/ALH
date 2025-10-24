from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from experience.models import Experience


class ExperienceQuerySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Experience.objects.all()

    def location(self, obj):
        base_url = reverse('experience:experience-view')
        return f"{base_url}?slug={obj.company.name.replace(' ', '-')}"

    def lastmod(self, obj):
        return obj.updated_at
