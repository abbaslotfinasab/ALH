from django.db import models
from django.utils import timezone


class Company(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True, blank=True, null=True)  # می‌تونه فارسی باشه
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name  # همین نام فارسی رو بذار
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Experience(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="experiences")
    title = models.CharField(max_length=120)  # مثل: Android Developer
    employment_type = models.CharField(max_length=50, blank=True, null=True)  # Full-time, Freelance, ...
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)  # اگر هنوز ادامه دارد خالی بماند
    description = models.TextField(blank=True, null=True)  # وظایف/دستاوردها
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.company.name} — {self.title}"

    @property
    def is_current(self):
        return self.end_date is None


class Project(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name="projects")
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=120, blank=True, null=True)  # مثل: Lead, Solo Dev
    description = models.TextField(blank=True, null=True)
    technology = models.CharField(max_length=200, blank=True, null=True)  # "Django, React, PostgreSQL"
    link_demo = models.URLField(blank=True, null=True)
    screenshot = models.ImageField(upload_to='project_shots/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def tech_list(self):
        return [t.strip() for t in self.technology.split(",") if t.strip()]
