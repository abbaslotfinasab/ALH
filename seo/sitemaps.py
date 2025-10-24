from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    def items(self):
        return [
            {'name': 'home:home-view', 'priority': 1.0, 'changefreq': 'daily'},
            {'name': 'about', 'priority': 0.7, 'changefreq': 'yearly'},
            {'name': 'collab:collab-view', 'priority': 0.8, 'changefreq': 'monthly'},
        ]

    def location(self, item):
        return reverse(item['name'])

    def priority(self, item):
        return item['priority']

    def changefreq(self, item):
        return item['changefreq']
