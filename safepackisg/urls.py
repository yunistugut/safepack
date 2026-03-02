"""
SafePackISG — Ana URL Yapılandırması
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from apps.core.sitemaps import (
    StaticViewSitemap, ProductSitemap, CategorySitemap, BlogPostSitemap
)

sitemaps = {
    'static': StaticViewSitemap,
    'products': ProductSitemap,
    'categories': CategorySitemap,
    'blog': BlogPostSitemap,
}

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # CKEditor
    path('ckeditor/', include('ckeditor_uploader.urls')),

    # Uygulamalar
    path('', include('apps.core.urls')),
    path('urunler/', include('apps.products.urls')),
    path('blog/', include('apps.blog.urls')),
    path('iletisim/', include('apps.contact.urls')),

    # Sitemap & Robots
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', include('apps.core.urls_robots')),
]

# Geliştirme ortamında medya dosyalarını serve et
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Admin panel başlıkları
admin.site.site_header = 'SafePackISG Yönetim Paneli'
admin.site.site_title = 'SafePackISG Admin'
admin.site.index_title = 'Hoş Geldiniz'
