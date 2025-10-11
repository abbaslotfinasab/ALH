from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    priority = 0.9
    changefreq = 'monthly'

    def items(self):
        return ['home:home-view', 'about', 'collab:collab-view']

    def location(self, item):
        return reverse(item)