from django.db import models
from django.utils.text import slugify


class Technology(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام تکنولوژی")
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    icon = models.ImageField(
        upload_to='technologies/icons/',
        blank=True,
        null=True,
        verbose_name="آیکون"
    )
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    website = models.URLField(blank=True, null=True, verbose_name="وب‌سایت رسمی")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "تکنولوژی"
        verbose_name_plural = "تکنولوژی‌ها"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Service(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان سرویس")
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    short_desc = models.TextField(verbose_name="توضیح کوتاه")
    content = models.TextField(verbose_name="محتوای کامل")  # متن کامل صفحه
    icon = models.ImageField(upload_to='services/icons/', blank=True, null=True)
    image = models.ImageField(upload_to='services/images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    technologies = models.ManyToManyField(
        'service.Technology',  # یا فقط Technology در صورتی که مدل در همین اپ است
        blank=True,
        related_name='services'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
