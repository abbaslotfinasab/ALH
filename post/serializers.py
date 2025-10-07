# posts/serializers.py
from rest_framework import serializers
from .models import Post, Tag, Comment

class TagReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]

class TagWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]

class CommentReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "post", "name", "text", "created_at"]

class CommentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["post", "name", "text", "is_approved"]

class PostReadSerializer(serializers.ModelSerializer):
    tags = TagReadSerializer(many=True, read_only=True)
    liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id","slug","title","content","image","video",
            "tags","views","likes","comments_count","is_published","created_at", "liked"
        ]

    def get_liked(self, obj):
        request = self.context.get("request")
        if request:
            liked_posts = request.session.get("liked_posts")
            if not isinstance(liked_posts, dict):
                liked_posts = {}
            return str(obj.id) in liked_posts
        return False

class PostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title","content","image","video","tags","is_published"]
