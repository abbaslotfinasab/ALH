from django.db.models import F
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import *
from .permissions import IsStaffOrReadOnly


def feed(request, combined_slug=None):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    canonical_url = request.build_absolute_uri()  # پیش‌فرض URL فعلی

    tag = request.GET.get("tag")
    if tag:
        posts = posts.filter(keywords__name=tag)  # یا keywords__slug=tag اگه slug داری
        canonical_url = f"https://abbaslotfinasab.ir/post/?tag={tag}"

    # حالت قدیمی بر اساس slug
    post = None
    if combined_slug:
        parts = combined_slug.strip("/").split("/")
        post_slug = parts[0] if len(parts) > 0 else None
        keyword_slug = parts[1] if len(parts) > 1 else None

        if post_slug and keyword_slug:
            post = get_object_or_404(Post, slug=post_slug, keywords__slug=keyword_slug, is_published=True)
        elif post_slug:
            post = get_object_or_404(Post, slug=post_slug, is_published=True)
        elif keyword_slug:
            post = get_object_or_404(Post, keywords__slug=keyword_slug, is_published=True)

        posts = [post] if post else []

    context = {
        "posts": posts,
        "canonical_url": canonical_url,
    }
    return render(request, "feed.html", context)



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().prefetch_related("keywords")
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {"keywords__id": ["exact"], "keywords__name": ["exact"], "is_published": ["exact"],
                        "created_at": ["date", "date__gte", "date__lte"]}
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
        # اطمینان از اینکه liked_posts یه dict هست
        liked = request.session.get("liked_posts")
        if not isinstance(liked, dict):
            liked = {}

        if str(post.id) in liked:
            # آنلایک
            post.likes = max(post.likes - 1, 0)
            del liked[str(post.id)]
            liked_state = False
        else:
            # لایک جدید
            post.likes = (post.likes or 0) + 1
            liked[str(post.id)] = True
            liked_state = True

        post.save(update_fields=["likes"])
        request.session["liked_posts"] = liked
        return Response({"likes": post.likes, "liked": liked_state})

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

    @action(detail=True, methods=["POST"])
    def add_view(self, request, pk=None):
        post = self.get_object()
        ip = get_client_ip(request)

        # جلوگیری از تکرار ویو از یه آی‌پی
        viewed_key = f"viewed_{ip}_{post.id}"
        from django.core.cache import cache

        if not cache.get(viewed_key):
            post.views = F('views') + 1
            post.save(update_fields=["views"])
            post.refresh_from_db()
            cache.set(viewed_key, True, 60 * 60 * 6)  # هر آی‌پی هر ۶ ساعت فقط ۱ بار
        return Response({"views": post.views})


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {"post": ["exact"]}
    search_fields = ["name", "text"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        qs = Comment.objects.select_related("post")
        # فقط کامنت‌های تأییدشده برای کاربران عادی
        if self.request.method == "GET":
            return qs.all()
        return qs

    def get_serializer_class(self):
        if self.action == "create":
            return CommentWriteSerializer
        return CommentReadSerializer

    def perform_create(self, serializer):
        """در زمان ساخت، IP رو از request بفرستیم به serializer"""
        serializer.save()