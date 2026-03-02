# apps/contact/admin.py
from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'phone', 'email',
                    'get_subject_display', 'status', 'created_at']
    list_filter = ['status', 'subject', 'created_at']
    search_fields = ['name', 'company', 'email', 'phone']
    list_editable = ['status']
    readonly_fields = ['name', 'company', 'phone', 'email', 'subject',
                       'products_of_interest', 'message', 'created_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Gönderen Bilgileri', {
            'fields': ('name', 'company', 'phone', 'email', 'created_at')
        }),
        ('Talep', {
            'fields': ('subject', 'products_of_interest', 'message')
        }),
        ('Durum', {
            'fields': ('status', 'note')
        }),
    )

    def has_add_permission(self, request):
        return False  # Manuel ekleme kapalı, sadece formdan gelir
