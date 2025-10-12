# handwrite/models.py
from django.db import models
from django.utils.text import slugify
from django.urls import reverse


LANG_CHOICES = [
    ("python", "Python"),
    ("js", "JavaScript"),
    ("html", "HTML"),
    ("css", "CSS"),
    ("bash", "Bash"),
    ("sql", "SQL"),
    ("other", "Other"),
]


class Snippet(models.Model):
    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=260, unique=True, blank=True)
    short_description = models.CharField(max_length=255, blank=True)
    full_code = models.TextField(help_text="کد کامل یا مثال")
    language = models.CharField(max_length=30, choices=LANG_CHOICES, default="python")
    project_name = models.CharField(max_length=160, blank=True, null=True)
    lesson = models.TextField(blank=True, help_text="نکته‌ها یا درس‌آموخته‌ها")
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="ترتیب نمایش (کوچک‌تر اول)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-order", "-created_at"]
        verbose_name = "دست‌خط / Snippet"
        verbose_name_plural = "دست‌خط‌ها / Snippets"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("handwrite:handwrite-view")

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title, allow_unicode=True)[:240]
            slug = base
            counter = 1
            while Snippet.objects.filter(slug=slug).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def preview_code(self):
        # خلاصه‌ای از کد برای کارت (قابل تغییر)
        preview = self.full_code.strip().splitlines()
        preview = preview[:8]  # چند خط اول
        return "\n".join(preview)
