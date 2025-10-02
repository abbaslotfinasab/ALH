# models.py
from django.db import models

class Availability(models.Model):
    STATUS_CHOICES = [
        ('available', 'آماده همکاری'),
        ('busy', 'مشغول'),
        ('sleep', 'استراحت'),
        ('travel', 'سفر'),
        ('off', 'خارج از دسترس'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    message = models.TextField(blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)
