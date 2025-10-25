from urllib.parse import quote
from django.db.models import Q
from django.utils.encoding import force_str

from ALH import settings
from blog.models import Blog
from seo.models import SEOPage

def seo_context(request):
    path = request.path

    # --- بررسی بلاگ ---
    if path.startswith("/blog/"):
        slug = path.rstrip("/").split("/")[-1]
        blog_post = Blog.objects.filter(slug=slug).first()
        if blog_post:
            return {
                'seo_title': blog_post.meta_title or blog_post.title,
                'seo_description': blog_post.meta_description or blog_post.content[:157] + "...",
                'seo_keywords': ", ".join([kw.name for kw in blog_post.keywords.all()]),
                'canonical_url': request.build_absolute_uri(),
            }

    # --- بررسی صفحات SEOPage ---
    seo_data = SEOPage.objects.prefetch_related('keywords').filter(
        Q(page_url=path) | Q(page_url=path.rstrip('/')) | Q(page_url=path + '/')
    ).first()

    if seo_data:
        return {
            'seo_title': seo_data.title,
            'seo_description': seo_data.description,
            'seo_keywords': ", ".join([kw.name for kw in seo_data.keywords.all()]),
            'canonical_url': request.build_absolute_uri()

        }

    # --- مقادیر پیش‌فرض ---
    return {
        'seo_title': force_str(settings.SEO['default']['title']),
        'seo_description': force_str(settings.SEO['default']['description']),
        'seo_keywords': ", ".join(settings.SEO['default']['keywords']),
        'canonical_url': request.build_absolute_uri()

    }
