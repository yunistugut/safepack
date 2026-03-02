# apps/core/context_processors.py
from apps.products.models import Category, Brand


def global_context(request):
    """
    Tüm template'lerde erişilebilir global değişkenler.
    Header navigasyonu ve footer için kullanılır.
    """
    return {
        'nav_categories': Category.objects.filter(
            is_active=True, parent=None
        ).order_by('order')[:10],
        'footer_brands': Brand.objects.filter(is_active=True).order_by('order')[:8],
        'SITE_NAME': 'SafePackISG',
        'CONTACT_PHONE': '0228 123 45 67',
        'CONTACT_EMAIL': 'info@safepackisg.com',
        'CONTACT_WHATSAPP': '90-5xx-xxx-xxxx',
        'CONTACT_ADDRESS': 'Bozüyük, Bilecik',
    }
