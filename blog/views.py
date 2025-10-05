# api_views.py
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import F
from .models import BlogPost, Tag
from .serializers import BlogPostSerializer, TagSerializer
from django.views.generic import ListView, DetailView

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50

class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogPost.objects.filter(is_published=True).prefetch_related("tags", "gallery")
    serializer_class = BlogPostSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "excerpt", "content", "tags__name"]
    ordering_fields = ["created_at", "views", "likes"]

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        post = self.get_object()
        post.likes = F("likes") + 1
        post.save(update_fields=["likes"])
        post.refresh_from_db()
        return Response({"likes": post.likes})

    @action(detail=True, methods=["post"])
    def viewed(self, request, pk=None):
        post = self.get_object()
        post.views = F("views") + 1
        post.save(update_fields=["views"])
        post.refresh_from_db()
        return Response({"views": post.views})

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class BlogListView(ListView):
    model = BlogPost
    template_name = "blogs.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().filter(is_published=True)
        q = self.request.GET.get("q")
        tag = self.request.GET.get("tag")
        if q:
            qs = qs.filter(title__icontains=q)  # ساده؛ یا از SearchFilter استفاده کن
        if tag:
            qs = qs.filter(tags__slug=tag)
        return qs

class BlogDetailView(DetailView):
    model = BlogPost
    template_name = "blogpost.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        # افزایش بازدید (آسان، با توجه به concurrency میشه atomic کرد)
        obj.views = F('views') + 1
        obj.save(update_fields=["views"])
        obj.refresh_from_db()
        return obj
