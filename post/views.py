# posts/views_api.py
from django.shortcuts import render
from rest_framework import viewsets
from .models import Post, Tag, Comment
from .serializers import PostSerializer, TagSerializer, CommentSerializer


def posts(request):
    return render(request, "feed.html", {"tags": Tag.objects.all().order_by("name")})


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
