from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product, Category, Brand, Certificate


def product_list(request):
    """Ürün listesi — filtre ve arama destekli"""
    qs = Product.objects.filter(is_active=True).select_related('category', 'brand')

    # Filtreler
    category_slug = request.GET.get('kategori')
    brand_slugs = request.GET.getlist('marka')
    cert_ids = request.GET.getlist('sertifika')
    q = request.GET.get('q', '').strip()
    sort = request.GET.get('siralama', '')

    if category_slug:
        qs = qs.filter(category__slug=category_slug)
    if brand_slugs:
        qs = qs.filter(brand__slug__in=brand_slugs)
    if cert_ids:
        qs = qs.filter(certificates__id__in=cert_ids).distinct()
    if q:
        qs = qs.filter(
            Q(name__icontains=q) |
            Q(short_description__icontains=q) |
            Q(category__name__icontains=q)
        )

    # Sıralama
    sort_map = {
        'az': 'name',
        'za': '-name',
        'yeni': '-created_at',
    }
    qs = qs.order_by(sort_map.get(sort, '-is_featured'))

    # Sayfalama
    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get('sayfa'))

    context = {
        'page_obj': page_obj,
        'categories': Category.objects.filter(is_active=True, parent=None),
        'brands': Brand.objects.filter(is_active=True),
        'certificates': Certificate.objects.all(),
        'active_category': category_slug,
        'active_brands': brand_slugs,
        'active_certs': cert_ids,
        'query': q,
        'sort': sort,
        'total_count': qs.count(),
        # SEO
        'meta_title': 'Ürün Kataloğu | SafePackISG – İş Güvenliği Ekipmanları',
        'meta_description': 'CE belgeli iş güvenliği ekipmanları ve ambalaj malzemeleri kataloğu.',
    }
    return render(request, 'products/list.html', context)


def category_detail(request, slug):
    """Kategori sayfası — o kategorideki ürünler"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    qs = Product.objects.filter(
        category=category, is_active=True
    ).select_related('brand')

    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get('sayfa'))

    context = {
        'category': category,
        'page_obj': page_obj,
        'categories': Category.objects.filter(is_active=True, parent=None),
        'meta_title': category.meta_title or f'{category.name} | SafePackISG',
        'meta_description': category.meta_description or category.description[:160],
    }
    return render(request, 'products/category.html', context)


def product_detail(request, category_slug, slug):
    """Ürün detay sayfası"""
    product = get_object_or_404(
        Product,
        slug=slug,
        category__slug=category_slug,
        is_active=True
    )
    images = product.images.all()
    related = product.related_products.filter(is_active=True)[:4]

    # Spesifikasyonlar JSON → liste
    specs = []
    if isinstance(product.specifications, dict):
        specs = list(product.specifications.items())

    context = {
        'product': product,
        'images': images,
        'related': related,
        'specs': specs,
        'meta_title': product.get_meta_title,
        'meta_description': product.get_meta_description,
        # Schema.org için
        'schema_product': {
            'name': product.name,
            'description': product.short_description,
            'url': request.build_absolute_uri(product.get_absolute_url()),
            'category': product.category.name,
            'brand': product.brand.name if product.brand else 'SafePackISG',
        }
    }
    return render(request, 'products/detail.html', context)
