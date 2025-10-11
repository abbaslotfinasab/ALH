from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from blog.serializers import *
from seo.models import SEOPage, Keyword  # ← اپ سئو که ساختی
from django.conf import settings


# لیست مقالات
class BlogPostListView(ListView):
    model = Blog
    template_name = "blogs.html"
    context_object_name = "blog_posts"
    paginate_by = 10

    def get_queryset(self):
        queryset = Blog.objects.all().order_by("-published_date")
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(content__icontains=search))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_posts"] = Blog.objects.count()

        # داده‌های سئو برای صفحه لیست بلاگ‌ها
        seo_data = SEOPage.objects.filter(page_url=self.request.path).first()
        if seo_data:
            context["meta_title"] = seo_data.title
            context["meta_description"] = seo_data.description
            context["meta_keywords"] = ", ".join([kw.name for kw in seo_data.keywords.all()])
        else:
            # fallback از settings
            default = settings.SEO["default"]
            context["meta_title"] = default["title"]
            context["meta_description"] = default["description"]
            context["meta_keywords"] = ", ".join(default["keywords"])

        context["canonical_url"] = self.request.build_absolute_uri()
        context["keywords"] = Keyword.objects.all()

        return context


# جزئیات مقاله
class BlogPostDetailView(DetailView):
    model = Blog
    template_name = "blogpost.html"
    context_object_name = "blog_post"

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")
        return get_object_or_404(Blog, slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_post = self.get_object()
        current_path = self.request.path

        # مرحله ۱: بررسی در SEOPage
        seo_data = SEOPage.objects.filter(page_url=current_path).first()

        if seo_data:
            context["meta_title"] = seo_data.title
            context["meta_description"] = seo_data.description
            context["meta_keywords"] = ", ".join([kw.name for kw in seo_data.keywords.all()])
        else:
            # مرحله ۲: بررسی فیلدهای خود مدل بلاگ
            context["meta_title"] = blog_post.meta_title or blog_post.title
            context["meta_description"] = (
                    blog_post.meta_description
                    or (blog_post.content[:157] + "..." if blog_post.content else "")
            )
            context["meta_keywords"] = ", ".join([kw.name for kw in blog_post.keywords.all()])

        context["canonical_url"] = self.request.build_absolute_uri()
        context["page_title"] = blog_post.title
        context["page_content"] = blog_post.content
        context["page_image"] = blog_post.image.url if blog_post.image else None

        return context


# برای API
class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all().order_by('-published_date')

    def get_serializer_class(self):
        """
        هوشمند انتخاب Serializer:
        - خواندنی (GET, LIST, RETRIEVE) => BlogReadSerializer
        - نوشتنی (POST, PUT, PATCH, DELETE) => BlogWriteSerializer
        """
        if self.action in ['list', 'retrieve']:
            return BlogReadSerializer
        return BlogWriteSerializer
