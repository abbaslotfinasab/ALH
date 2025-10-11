from django.db import models
from django.utils.text import slugify



class Keyword(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=70, unique=True, blank=True)

    class Meta: ordering = ["name"]

    def save(self, *a, **kw):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)[:70]
        super().save(*a, **kw)

    def __str__(self): return self.name



class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)  # تاریخ انتشار
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)  # تصویر شاخص
    meta_title = models.CharField(max_length=255, blank=True, null=True)  # عنوان برای SEO
    meta_description = models.TextField(blank=True, null=True, help_text="توضیحات متا (Meta Description)")  # توضیحات برای SEO
    meta_keywords = models.ManyToManyField(Keyword, blank=True, help_text="کلمات کلیدی (Keywords)")  # کلمات کلیدی برای SEO

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

            while Blog.objects.filter(slug=self.slug).exists():
                self.slug = f"{slugify(self.title)}-{self.pk}"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/blog/{self.slug}/"

    def __str__(self):
        return self.title
