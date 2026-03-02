# apps/core/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.products.models import Product, Category
from apps.blog.models import BlogPost


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return ['core:home', 'core:about', 'core:certificates',
                'products:list', 'blog:list', 'contact:contact']

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Product.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Category.objects.filter(is_active=True)


class BlogPostSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return BlogPost.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at
