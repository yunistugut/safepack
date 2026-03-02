from django.contrib import admin
from django.utils.html import format_html
from .models import Brand, Category, Certificate, Product, ProductImage, SliderItem


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo_preview', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" height="30">', obj.logo.url)
        return '—'
    logo_preview.short_description = 'Logo'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'icon', 'product_count', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active', 'parent']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

    def product_count(self, obj):
        return obj.products.filter(is_active=True).count()
    product_count.short_description = 'Ürün Sayısı'


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ['image', 'alt_text', 'order']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['thumbnail_preview', 'name', 'category', 'brand',
                    'badge', 'is_active', 'is_featured', 'created_at']
    list_display_links = ['thumbnail_preview', 'name']
    list_editable = ['is_active', 'is_featured']
    list_filter = ['is_active', 'is_featured', 'category', 'brand', 'badge']
    search_fields = ['name', 'short_description']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['certificates', 'related_products']
    inlines = [ProductImageInline]
    save_on_top = True
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('name', 'slug', 'category', 'brand', 'badge',
                       'thumbnail', 'short_description')
        }),
        ('İçerik', {
            'fields': ('description', 'usage_areas', 'care_instructions')
        }),
        ('Teknik Özellikler', {
            'fields': ('specifications', 'certificates'),
            'description': 'Özellikler JSON formatında girilir: {"Standart": "EN 397"}'
        }),
        ('İlgili Ürünler', {
            'fields': ('related_products',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Durum', {
            'fields': ('is_active', 'is_featured')
        }),
    )

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" height="40" style="border-radius:6px;">', obj.thumbnail.url)
        return '—'
    thumbnail_preview.short_description = 'Görsel'


@admin.register(SliderItem)
class SliderItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'tag', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    fieldsets = (
        ('İçerik', {
            'fields': ('title', 'subtitle', 'tag', 'description')
        }),
        ('Görsel', {
            'fields': ('background_image', 'background_color')
        }),
        ('Butonlar', {
            'fields': (
                ('primary_btn_text', 'primary_btn_url'),
                ('secondary_btn_text', 'secondary_btn_url'),
            )
        }),
        ('Durum', {
            'fields': ('is_active', 'order')
        }),
    )
