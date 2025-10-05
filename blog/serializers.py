from rest_framework import serializers
from .models import BlogPost, Tag, BlogImage

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]
        read_only_fields = ["slug"]

class BlogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImage
        fields = ["id", "image", "caption"]

class BlogPostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    gallery = BlogImageSerializer(many=True, read_only=True)
    slug = serializers.CharField(read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            "id", "title", "slug", "excerpt", "content",
            "cover", "tags", "gallery",
            "views", "likes", "comments_count",
            "is_published", "created_at", "updated_at"
        ]
        read_only_fields = ["slug", "views", "likes", "comments_count", "created_at", "updated_at"]
