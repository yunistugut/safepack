from django import forms
from .models import ContactMessage

PRODUCT_CHOICES = [
    ('eldivenler', '🧤 İş Eldivenleri'),
    ('baretler', '⛑️ Baretler'),
    ('ayakkabi', '👟 İş Ayakkabıları'),
    ('yangin', '🔥 Yangın Güvenliği'),
    ('solunum', '😷 Solunum Ekipmanları'),
    ('ambalaj', '📦 Ambalaj Malzemeleri'),
]


class ContactForm(forms.ModelForm):
    products_of_interest = forms.MultipleChoiceField(
        choices=PRODUCT_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='İlgilendiğiniz Ürünler',
    )
    kvkk = forms.BooleanField(
        required=True,
        label='KVKK Aydınlatma Metnini okudum ve onaylıyorum.',
        error_messages={'required': 'Devam edebilmek için KVKK metnini onaylamanız gerekmektedir.'}
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'company', 'phone', 'email', 'subject',
                  'products_of_interest', 'message']
        labels = {
            'name': 'Ad Soyad',
            'company': 'Şirket / Kurum',
            'phone': 'Telefon',
            'email': 'E-posta',
            'subject': 'Talep Konusu',
            'message': 'Mesajınız',
        }
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }

    def clean_products_of_interest(self):
        return list(self.cleaned_data.get('products_of_interest', []))
