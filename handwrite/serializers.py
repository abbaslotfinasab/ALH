# handwrite/serializers.py
from rest_framework import serializers
from .models import Snippet

class SnippetReadSerializer(serializers.ModelSerializer):
    preview_code = serializers.CharField(read_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = Snippet
        fields = [
            "id",
            "title",
            "slug",
            "short_description",
            "full_code",
            "preview_code",
            "language",
            "project_name",
            "lesson",
            "is_published",
            "created_at",
            "updated_at",
            "url",
        ]

    def get_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.get_absolute_url())
        return obj.get_absolute_url()


class SnippetWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = [
            "title",
            "short_description",
            "full_code",
            "language",
            "project_name",
            "lesson",
            "is_published",
            "order",
        ]
