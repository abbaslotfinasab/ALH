from rest_framework import serializers
from .models import Service, Technology


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = ["id", "name", "slug", "icon", "description", "website"]
        read_only_fields = ["slug"]   # 👈 فقط خوندنی باشه



class ServiceSerializer(serializers.ModelSerializer):
    technology = TechnologySerializer(read_only=True)

    class Meta:
        model = Service
        fields = [
            "id", "title", "slug", "short_desc", "content",
            "icon", "image", "is_active", "technology"
        ]
        read_only_fields = ["slug"]   # 👈 فقط خوندنی باشه

