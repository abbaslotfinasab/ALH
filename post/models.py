# posts/models.py
from django.db import models
from django.utils.text import slugify

from seo.models import Keyword


class Post(models.Model):
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to="posts/images/", blank=True, null=True)
    video = models.FileField(upload_to="posts/videos/", blank=True, null=True)

    keywords = models.ManyToManyField(Keyword, related_name="posts", blank=True)

    is_published = models.BooleanField(default=False)

    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)


    slug = models.SlugField(max_length=280, unique=True, blank=True)
    # فیلدهای سئو:
    meta_title = models.CharField(max_length=70, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True ,help_text="حداکثر 160 کاراکتر")
    og_image = models.ImageField(upload_to="posts/og/", blank=True, null=True)
    canonical_url = models.URLField(blank=True)

    class Meta:
        ordering = ["-created_at"]


    def save(self, *a, **kw):
        if not self.slug:
            base = self.title or self.content[:60]
            self.slug = slugify(base, allow_unicode=True)[:270]
        # پیش‌فرض‌های سئو
        if not self.meta_title:
            self.meta_title = (self.title or self.content[:60])[:70]
        if not self.meta_description:
            self.meta_description = (self.content[:155]).replace("\n", " ")[:160]
        super().save(*a, **kw)


    def __str__(self):
        return self.title if self.title else self.content[:50]

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # یا user اگر لاگین داشته باشی
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
