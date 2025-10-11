from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from seo.models import Keyword


class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)

    # --- SEO Fields ---
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True ,help_text="حداکثر 160 کاراکتر")
    keywords = models.ManyToManyField(Keyword, related_name="blogs", blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":
            self.slug = slugify(self.title, allow_unicode=True)
        if not self.meta_title:
            self.meta_title = self.title
        if not self.meta_description:
            self.meta_description = (self.content[:157] + "...") if self.content else ""
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/blogs/{self.slug}/"

    def __str__(self):
        return self.title
