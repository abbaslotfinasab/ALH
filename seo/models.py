from django.db import models
from django.utils.text import slugify


class Keyword(models.Model):
    class Category(models.TextChoices):
        BLOG = "blog", "وبلاگ"
        POST = "post", "روزنوشت"
        HANDWRITING = "handwriting", "دستخط"
        SEO = "seo", "سئو"


    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=70, unique=True, blank=True)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.BLOG,
        verbose_name="دسته مربوطه"
    )

    class Meta:
        ordering = ["name"]

    def save(self, *a, **kw):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)[:70]
        super().save(*a, **kw)

    def __str__(self):
        return f"{self.name}"


class SEOPage(models.Model):
    page_url = models.CharField(max_length=255, unique=True, help_text="مسیر صفحه بدون دامنه، مثل /about/")
    title = models.CharField(max_length=255, help_text="عنوان صفحه (Title)")
    description = models.TextField(help_text="توضیحات متا (Meta Description)")
    keywords = models.ManyToManyField(Keyword, blank=True, help_text="کلمات کلیدی (Keywords)")

    def __str__(self):
        return self.title
