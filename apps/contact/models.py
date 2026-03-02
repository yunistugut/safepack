# apps/contact/models.py
from django.db import models


class ContactMessage(models.Model):
    SUBJECT_CHOICES = [
        ('teklif', 'Fiyat Teklifi'),
        ('urun-bilgi', 'Ürün Bilgisi'),
        ('kurumsal', 'Kurumsal Sözleşme'),
        ('danismanlik', 'ISG Danışmanlığı'),
        ('sertifika', 'Sertifika Talebi'),
        ('diger', 'Diğer'),
    ]

    STATUS_CHOICES = [
        ('new', 'Yeni'),
        ('in_progress', 'İşlemde'),
        ('done', 'Tamamlandı'),
    ]

    name = models.CharField('Ad Soyad', max_length=150)
    company = models.CharField('Şirket', max_length=150, blank=True)
    phone = models.CharField('Telefon', max_length=20)
    email = models.EmailField('E-posta')
    subject = models.CharField('Konu', max_length=30, choices=SUBJECT_CHOICES)
    products_of_interest = models.JSONField('İlgilenilen Ürünler', default=list, blank=True)
    message = models.TextField('Mesaj')
    status = models.CharField('Durum', max_length=20, choices=STATUS_CHOICES, default='new')
    note = models.TextField('Admin Notu', blank=True)
    created_at = models.DateTimeField('Gönderildi', auto_now_add=True)

    class Meta:
        verbose_name = 'İletişim Mesajı'
        verbose_name_plural = 'İletişim Mesajları'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.get_subject_display()} ({self.created_at.strftime("%d.%m.%Y")})'
