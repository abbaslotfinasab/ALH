from django.db import models

SCOPE_CHOICES = [
    ("UI/UX", "UI/UX"),
    ("Front-end", "Front-end"),
    ("Back-end", "Back-end"),
    ("CI/CD", "CI/CD"),
    ("SEO", "SEO"),
]

MODE_CHOICES = [
    ("fulltime", "تمام‌وقت"),
    ("parttime", "پاره‌وقت"),
    ("contract", "پروژه‌ای"),
    ("remote", "دورکاری"),
]

class ProjectRequest(models.Model):
    name       = models.CharField(max_length=120)
    email      = models.EmailField()
    phone      = models.CharField(max_length=32, blank=True)
    project_type = models.CharField(max_length=20, choices=[("web","وب"),("mobile","موبایل"),("both","هر دو")], default="web")
    scopes     = models.CharField(max_length=255, blank=True)  # CSV ساده: "UI/UX,Front-end"
    deadline   = models.DateField(null=True, blank=True)
    budget     = models.CharField(max_length=60, blank=True)
    message    = models.TextField()
    nda        = models.BooleanField(default=False)

    # متادیتا
    ip         = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read    = models.BooleanField(default=False)

    def __str__(self):
        return f"[Project] {self.name} - {self.email}"

class HireRequest(models.Model):
    name       = models.CharField(max_length=120)
    email      = models.EmailField()
    role       = models.CharField(max_length=120, blank=True)
    mode       = models.CharField(max_length=20, choices=MODE_CHOICES, blank=True)
    skills     = models.CharField(max_length=255, blank=True)
    message    = models.TextField(blank=True)

    ip         = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read    = models.BooleanField(default=False)

    def __str__(self):
        return f"[Hire] {self.name} - {self.email}"
