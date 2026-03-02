"""
SafePackISG — Ürün Modelleri

Tablolar:
  - Brand          : 3M, Honeywell, MSA Safety vb.
  - Category       : İş Eldivenleri, Baretler vb.
  - Product        : Ürün ana tablosu
  - ProductImage   : Ürün görselleri (çoklu)
  - Certificate    : CE, EN 388 vb. sertifikalar
  - SliderItem     : Anasayfa slider
"""

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField


class Brand(models.Model):
    name = models.CharField('Marka Adı', max_length=100)
    slug = models.SlugField('URL', unique=True, blank=True)
    logo = models.ImageField('Logo', upload_to='brands/', blank=True, null=True)
    website = models.URLField('Web Sitesi', blank=True)
    is_active = models.BooleanField('Aktif', default=True)
    order = models.PositiveSmallIntegerField('Sıra', default=0)

    class Meta:
        verbose_name = 'Marka'
        verbose_name_plural = 'Markalar'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField('Kategori Adı', max_length=150)
    slug = models.SlugField('URL', unique=True, blank=True)
    icon = models.CharField('İkon (emoji/fa)', max_length=50, blank=True,
                            help_text='Örnek: ⛑️ ya da fa-hard-hat')
    description = models.TextField('Açıklama', blank=True)
    image = models.ImageField('Görsel', upload_to='categories/', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL,
                               null=True, blank=True,
                               related_name='children',
                               verbose_name='Üst Kategori')
    is_active = models.BooleanField('Aktif', default=True)
    order = models.PositiveSmallIntegerField('Sıra', default=0)
    meta_title = models.CharField('SEO Başlık', max_length=60, blank=True)
    meta_description = models.CharField('SEO Açıklama', max_length=160, blank=True)

    class Meta:
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategoriler'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:category', kwargs={'slug': self.slug})

    @property
    def product_count(self):
        return self.products.filter(is_active=True).count()


class Certificate(models.Model):
    """CE, EN 388, EN 397, TS EN 3 gibi sertifikalar"""
    name = models.CharField('Sertifika', max_length=100)
    code = models.CharField('Kod', max_length=50, help_text='Örnek: EN 397')
    description = models.TextField('Açıklama', blank=True)

    class Meta:
        verbose_name = 'Sertifika'
        verbose_name_plural = 'Sertifikalar'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    BADGE_CHOICES = [
        ('', 'Rozetsiz'),
        ('yeni', 'Yeni'),
        ('populer', 'Popüler'),
        ('ce', 'CE Belgeli'),
    ]

    # Temel bilgiler
    name = models.CharField('Ürün Adı', max_length=200)
    slug = models.SlugField('URL', unique=True, blank=True, max_length=220)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,
                                 related_name='products', verbose_name='Kategori')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL,
                              null=True, blank=True,
                              related_name='products', verbose_name='Marka')

    # Açıklamalar
    short_description = models.TextField('Kısa Açıklama', max_length=300,
                                         help_text='Kart görünümünde gösterilir')
    description = RichTextField('Detaylı Açıklama', blank=True)
    usage_areas = RichTextField('Kullanım Alanları', blank=True)
    care_instructions = RichTextField('Bakım ve Depolama', blank=True)

    # Teknik özellikler (JSON olarak saklanır)
    specifications = models.JSONField(
        'Teknik Özellikler',
        default=dict,
        blank=True,
        help_text='{"Standart": "EN 397", "Materyal": "HDPE", ...}'
    )

    # İlişkiler
    certificates = models.ManyToManyField(Certificate, blank=True,
                                          verbose_name='Sertifikalar')
    related_products = models.ManyToManyField('self', blank=True,
                                              verbose_name='İlgili Ürünler')

    # Görsel ve rozet
    thumbnail = models.ImageField('Ana Görsel', upload_to='products/thumbnails/',
                                  null=True, blank=True)
    badge = models.CharField('Rozet', max_length=20, choices=BADGE_CHOICES,
                             default='', blank=True)

    # SEO
    meta_title = models.CharField('SEO Başlık', max_length=60, blank=True)
    meta_description = models.CharField('SEO Açıklama', max_length=160, blank=True)

    # Durum
    is_active = models.BooleanField('Aktif', default=True)
    is_featured = models.BooleanField('Öne Çıkan', default=False)
    created_at = models.DateTimeField('Oluşturuldu', auto_now_add=True)
    updated_at = models.DateTimeField('Güncellendi', auto_now=True)

    class Meta:
        verbose_name = 'Ürün'
        verbose_name_plural = 'Ürünler'
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={
            'category_slug': self.category.slug,
            'slug': self.slug,
        })

    @property
    def get_meta_title(self):
        return self.meta_title or f'{self.name} | SafePackISG'

    @property
    def get_meta_description(self):
        return self.meta_description or self.short_description[:160]

    @property
    def certificate_codes(self):
        return ', '.join(c.code for c in self.certificates.all())


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='images', verbose_name='Ürün')
    image = models.ImageField('Görsel', upload_to='products/gallery/')
    alt_text = models.CharField('Alt Metin', max_length=150, blank=True)
    order = models.PositiveSmallIntegerField('Sıra', default=0)

    class Meta:
        verbose_name = 'Ürün Görseli'
        verbose_name_plural = 'Ürün Görselleri'
        ordering = ['order']

    def __str__(self):
        return f'{self.product.name} — Görsel {self.order}'


class SliderItem(models.Model):
    title = models.CharField('Başlık', max_length=200)
    subtitle = models.CharField('Alt Başlık', max_length=300, blank=True)
    tag = models.CharField('Etiket', max_length=80, blank=True,
                           help_text='Örnek: ✅ CE Sertifikalı Ürünler')
    description = models.TextField('Açıklama', blank=True)
    background_image = models.ImageField('Arka Plan Görseli',
                                         upload_to='slider/', blank=True, null=True)
    background_color = models.CharField('Arka Plan Rengi (CSS)',
                                        max_length=200, blank=True,
                                        help_text='background CSS değeri')
    primary_btn_text = models.CharField('Birincil Buton Metni', max_length=60, blank=True)
    primary_btn_url = models.CharField('Birincil Buton URL', max_length=200, blank=True)
    secondary_btn_text = models.CharField('İkincil Buton Metni', max_length=60, blank=True)
    secondary_btn_url = models.CharField('İkincil Buton URL', max_length=200, blank=True)
    is_active = models.BooleanField('Aktif', default=True)
    order = models.PositiveSmallIntegerField('Sıra', default=0)

    class Meta:
        verbose_name = 'Slider'
        verbose_name_plural = 'Slider Öğeleri'
        ordering = ['order']

    def __str__(self):
        return self.title
