# apps/core/views.py
from django.shortcuts import render
from apps.products.models import Category, Product, SliderItem, Brand
from apps.blog.models import BlogPost


def homepage(request):
    context = {
        'sliders': SliderItem.objects.filter(is_active=True).order_by('order'),
        'categories': Category.objects.filter(is_active=True, parent=None).order_by('order'),
        'featured_products': Product.objects.filter(is_active=True, is_featured=True)[:4],
        'brands': Brand.objects.filter(is_active=True).order_by('order'),
        'recent_posts': BlogPost.objects.filter(status='published').order_by('-published_at')[:3],
        'meta_title': 'SafePackISG | İş Güvenliği ve Ambalaj Malzemeleri – Bilecik',
        'meta_description': 'SafePackISG; CE belgeli iş eldivenleri, baretler, iş ayakkabıları, yangın tüpleri ve ambalaj malzemeleri. Bilecik merkezli ISG ekipmanları tedarikçisi.',
    }
    return render(request, 'core/home.html', context)


def about(request):
    return render(request, 'core/about.html', {
        'meta_title': 'Hakkımızda | SafePackISG',
        'meta_description': 'SafePackISG hakkında bilgi edinin. Misyonumuz, vizyonumuz ve ekibimiz.',
    })


def certificates(request):
    from apps.products.models import Certificate
    context = {
        'certificates': Certificate.objects.all(),
        'meta_title': 'Sertifikalarımız | SafePackISG',
        'meta_description': 'CE, EN ve TS standartları. SafePackISG ürün sertifikasyonları.',
    }
    return render(request, 'core/certificates.html', context)


def handler404(request, exception):
    return render(request, 'core/404.html', status=404)


def handler500(request):
    return render(request, 'core/500.html', status=500)
