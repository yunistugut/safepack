from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField


class BlogCategory(models.Model):
    name = models.CharField('Kategori', max_length=100)
    slug = models.SlugField('URL', unique=True, blank=True)
    order = models.PositiveSmallIntegerField('Sıra', default=0)

    class Meta:
        verbose_name = 'Blog Kategorisi'
        verbose_name_plural = 'Blog Kategorileri'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug})

    @property
    def post_count(self):
        return self.posts.filter(status='published').count()


class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Taslak'),
        ('published', 'Yayınlandı'),
    ]

    title = models.CharField('Başlık', max_length=200)
    slug = models.SlugField('URL', unique=True, blank=True, max_length=220)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 related_name='posts', verbose_name='Kategori')
    author = models.ForeignKey(User, on_delete=models.SET_NULL,
                               null=True, blank=True,
                               verbose_name='Yazar')
    excerpt = models.TextField('Özet', max_length=300,
                               help_text='Kart ve SEO açıklaması için kullanılır')
    content = RichTextUploadingField('İçerik')
    thumbnail = models.ImageField('Kapak Görseli', upload_to='blog/thumbnails/',
                                  null=True, blank=True)
    status = models.CharField('Durum', max_length=20, choices=STATUS_CHOICES,
                              default='draft')
    is_featured = models.BooleanField('Öne Çıkan', default=False)
    read_time = models.PositiveSmallIntegerField('Okuma Süresi (dk)', default=5)
    published_at = models.DateTimeField('Yayın Tarihi', null=True, blank=True)
    created_at = models.DateTimeField('Oluşturuldu', auto_now_add=True)
    updated_at = models.DateTimeField('Güncellendi', auto_now=True)

    # SEO
    meta_title = models.CharField('SEO Başlık', max_length=60, blank=True)
    meta_description = models.CharField('SEO Açıklama', max_length=160, blank=True)

    class Meta:
        verbose_name = 'Blog Yazısı'
        verbose_name_plural = 'Blog Yazıları'
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    @property
    def get_meta_title(self):
        return self.meta_title or f'{self.title} | SafePackISG Blog'

    @property
    def get_meta_description(self):
        return self.meta_description or self.excerpt[:160]
