# posts/views_api.py
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .serializers import *
from .permissions import IsStaffOrReadOnly


def feed(request):
    tags = Tag.objects.all().order_by("name")
    return render(request, "feed.html", {"tags": tags})

def detail(request, slug):
    post = get_object_or_404(Post.objects.prefetch_related("tags"), slug=slug, is_published=True)

    # افزایش بازدید یک‌بار برای هر session+post
    viewed_key = f"viewed_post_{post.id}"
    if not request.session.get(viewed_key):
        Post.objects.filter(id=post.id).update(views=F("views") + 1)
        request.session[viewed_key] = True
        post.refresh_from_db(fields=["views"])

    # پست‌های مرتبط با تگ مشترک (به‌جز خودش)
    related = Post.objects.filter(
        is_published=True, tags__in=post.tags.all()
    ).exclude(id=post.id).distinct().order_by("-created_at")[:6]

    return render(request, "detail.html", {
        "post": post,
        "related": related,
    })

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(is_published=True).prefetch_related("tags")
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {"tags__id": ["exact"], "tags__name": ["exact"], "is_published": ["exact"]}
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "views", "likes"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return PostWriteSerializer
        return PostReadSerializer

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        post = self.get_object()
        liked = request.session.get("liked_posts", [])
        if post.id not in liked:
            post.likes = (post.likes or 0) + 1
            post.save(update_fields=["likes"])
            liked.append(post.id)
            request.session["liked_posts"] = liked
        return Response({"likes": post.likes})

    @action(detail=True, methods=["post"])
    def viewed(self, request, pk=None):
        post = self.get_object()
        viewed = request.session.get("viewed_posts", [])
        if post.id not in viewed:
            post.views = (post.views or 0) + 1
            post.save(update_fields=["views"])
            viewed.append(post.id)
            request.session["viewed_posts"] = viewed
        return Response({"views": post.views})


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {"post": ["exact"], "is_approved": ["exact"]}
    search_fields = ["name", "text"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        qs = Comment.objects.select_related("post")
        # GET عمومی فقط کامنت‌های تاییدشده را برگرداند
        if self.request.method in ("GET",):
            return qs.filter(is_approved=True)
        return qs

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return CommentWriteSerializer
        return CommentReadSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by("name")
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return TagWriteSerializer
        return TagReadSerializer
