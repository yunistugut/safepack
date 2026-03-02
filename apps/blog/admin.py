# apps/blog/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import BlogCategory, BlogPost


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'post_count', 'order']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}

    def post_count(self, obj):
        return obj.posts.filter(status='published').count()
    post_count.short_description = 'Yazı Sayısı'


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['thumbnail_preview', 'title', 'category', 'status',
                    'is_featured', 'read_time', 'published_at']
    list_display_links = ['thumbnail_preview', 'title']
    list_editable = ['status', 'is_featured']
    list_filter = ['status', 'is_featured', 'category']
    search_fields = ['title', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    save_on_top = True
    date_hierarchy = 'published_at'

    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'slug', 'category', 'author', 'thumbnail',
                       'excerpt', 'read_time')
        }),
        ('İçerik', {
            'fields': ('content',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Yayın', {
            'fields': ('status', 'is_featured', 'published_at')
        }),
    )

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" height="40" style="border-radius:6px;">', obj.thumbnail.url)
        return '—'
    thumbnail_preview.short_description = 'Görsel'
