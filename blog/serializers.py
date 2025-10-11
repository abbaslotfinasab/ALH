from rest_framework import serializers

from seo.serializers import KeyWordSerializer
from .models import Blog


class BlogReadSerializer(serializers.ModelSerializer):
    keywords = KeyWordSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "slug",
            "content",
            "image",
            "meta_title",
            "meta_description",
            "keywords",
            "published_date",
        ]

    def get_meta_keywords(self, obj):
        """کلمات کلیدی رو از رشته جدا کن و تمیز بده بیرون"""
        if obj.meta_keywords:
            return [kw.strip() for kw in obj.meta_keywords.split(",")]
        return []


class BlogWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            "title",
            "content",
            "image",
            "meta_title",
            "meta_description",
            "keywords",
        ]

    def validate_meta_description(self, value):
        """توضیحات متا نباید بیش از ۱۶۰ کاراکتر باشه"""
        if value and len(value) > 160:
            raise serializers.ValidationError("Meta description باید حداکثر ۱۶۰ کاراکتر باشد.")
        return value
