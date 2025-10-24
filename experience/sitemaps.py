from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Company

class ExperienceSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        # ترکیبی: صفحه اصلی (None) + همه شرکت‌ها
        return [None] + list(Company.objects.filter(is_active=True))

    def location(self, obj):
        if obj is None:
            return reverse('experience:experience-view')  # صفحه اصلی
        return reverse('experience:experience-view-slug', kwargs={'slug': obj.slug})  # هر شرکت

    def lastmod(self, obj):
        if obj is None:
            # صفحه اصلی: آخرین تغییرات بین همه شرکت‌ها
            last_company = Company.objects.filter(is_active=True).order_by('-experiences__updated_at').first()
            if last_company and last_company.experiences.exists():
                return last_company.experiences.order_by('-updated_at').first().updated_at
            return None
        # هر شرکت: آخرین بروزرسانی تجربه‌ها
        if obj.experiences.exists():
            return obj.experiences.order_by('-updated_at').first().updated_at
        return None
