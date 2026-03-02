from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import BlogPost, BlogCategory


def blog_list(request):
    qs = BlogPost.objects.filter(status='published').select_related('category', 'author')

    category_slug = request.GET.get('kategori')
    q = request.GET.get('q', '').strip()

    if category_slug:
        qs = qs.filter(category__slug=category_slug)
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(excerpt__icontains=q))

    featured = qs.filter(is_featured=True).first()
    popular = BlogPost.objects.filter(status='published').order_by('-published_at')[:4]

    paginator = Paginator(qs.exclude(pk=featured.pk if featured else None), 6)
    page_obj = paginator.get_page(request.GET.get('sayfa'))

    context = {
        'featured': featured,
        'page_obj': page_obj,
        'popular': popular,
        'categories': BlogCategory.objects.all(),
        'active_category': category_slug,
        'query': q,
        'meta_title': 'Blog | SafePackISG – İş Güvenliği Rehberleri',
        'meta_description': 'KKD seçim rehberleri, iş güvenliği mevzuatı ve sektör haberleri.',
    }
    return render(request, 'blog/list.html', context)


def blog_category(request, slug):
    category = get_object_or_404(BlogCategory, slug=slug)
    qs = BlogPost.objects.filter(status='published', category=category)
    paginator = Paginator(qs, 6)
    page_obj = paginator.get_page(request.GET.get('sayfa'))

    context = {
        'category': category,
        'page_obj': page_obj,
        'categories': BlogCategory.objects.all(),
        'meta_title': f'{category.name} | SafePackISG Blog',
        'meta_description': f'SafePackISG blog - {category.name} kategorisi',
    }
    return render(request, 'blog/list.html', context)


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    recent = BlogPost.objects.filter(
        status='published'
    ).exclude(pk=post.pk).order_by('-published_at')[:3]

    context = {
        'post': post,
        'recent': recent,
        'meta_title': post.get_meta_title,
        'meta_description': post.get_meta_description,
    }
    return render(request, 'blog/detail.html', context)
