from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=120)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def tech_list(self):
        return [t.strip() for t in self.technology.split(",") if t.strip()]
