# SafePackISG — Django Projesi

İş güvenliği ekipmanları ve ambalaj malzemeleri e-ticaret/katalog sitesi.

## Proje Yapısı

```
safepackisg/
├── safepackisg/          # Ana Django ayarları
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── core/             # Anasayfa, hakkımızda, sertifikalar
│   ├── products/         # Ürünler, kategoriler, markalar
│   ├── blog/             # Blog yazıları
│   └── contact/          # İletişim formu
├── templates/            # HTML template'ler
│   ├── base.html
│   ├── includes/         # header, footer, topbar
│   ├── core/
│   ├── products/
│   ├── blog/
│   └── contact/
├── static/
│   ├── css/main.css
│   └── js/main.js
├── media/                # Kullanıcı yüklemeleri (gitignore'a ekleyin)
├── requirements.txt
└── .env.example
```

## Kurulum

### 1. Depoyu klonlayın ve sanal ortam oluşturun

```bash
git clone https://github.com/your-org/safepackisg.git
cd safepackisg
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 2. Bağımlılıkları yükleyin

```bash
pip install -r requirements.txt
```

### 3. Ortam değişkenlerini ayarlayın

```bash
cp .env.example .env
# .env dosyasını açıp SECRET_KEY ve diğer değerleri doldurun
```

### 4. Veritabanını oluşturun

```bash
python manage.py migrate
```

### 5. Superuser oluşturun (admin paneli için)

```bash
python manage.py createsuperuser
```

### 6. Statik dosyaları toplayın

```bash
python manage.py collectstatic
```

### 7. Geliştirme sunucusunu başlatın

```bash
python manage.py runserver
```

Tarayıcıda http://127.0.0.1:8000 adresine gidin.

**Admin paneli:** http://127.0.0.1:8000/admin

---

## İlk Veri Girişi (Admin Panelinden)

### Kategoriler ekleyin
Admin → Products → Kategoriler → Ekle
- İş Eldivenleri (icon: 🧤, slug: is-eldivenleri)
- Baretler (icon: ⛑️, slug: baretler)
- İş Ayakkabıları (icon: 👟, slug: is-ayakkabilari)
- Yangın Güvenliği (icon: 🔥, slug: yangin-guvenligi)
- Solunum Ekipmanları (icon: 😷, slug: solunum-ekipmanlari)
- Reflektif Giysiler (icon: 🦺, slug: reflektif-giysiler)
- Göz & Yüz Koruması (icon: 🥽, slug: goz-yuz-koruma)
- Ambalaj Malzemeleri (icon: 📦, slug: ambalaj-malzemeleri)
- İlk Yardım (icon: 🩺, slug: ilk-yardim)

### Sertifikalar ekleyin
Admin → Products → Sertifikalar
- CE Belgeli (kod: CE)
- EN 388 (İş Eldivenleri)
- EN 397 (Baretler)
- EN ISO 20345 (İş Ayakkabıları)
- TS EN 3 (Yangın Tüpleri)
- EN 149 (Solunum Maskeleri)
- EN 166 (Göz Koruması)

### Slider ekleyin
Admin → Products → Slider Öğeleri

### Blog kategorileri ekleyin
Admin → Blog → Blog Kategorileri
- KKD Rehberleri
- Mevzuat
- Yangın Güvenliği
- Ambalaj
- Sektör Haberleri

---

## URL Yapısı

| URL | Sayfa |
|-----|-------|
| / | Anasayfa |
| /urunler/ | Ürün Listesi |
| /urunler/\<kategori-slug\>/ | Kategori Sayfası |
| /urunler/\<kategori-slug\>/\<urun-slug\>/ | Ürün Detay |
| /blog/ | Blog Listesi |
| /blog/\<yazi-slug\>/ | Blog Detay |
| /blog/kategori/\<slug\>/ | Blog Kategorisi |
| /iletisim/ | İletişim Formu |
| /hakkimizda/ | Hakkımızda |
| /sertifikalar/ | Sertifikalar |
| /sitemap.xml | XML Sitemap |
| /robots.txt | Robots.txt |
| /admin/ | Yönetim Paneli |

---

## Üretim Ortamı (Production)

`.env` dosyasında şu değişiklikleri yapın:
```
DEBUG=False
ALLOWED_HOSTS=www.safepackisg.com,safepackisg.com
DATABASE_URL=postgres://kullanici:sifre@localhost:5432/safepackisg
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
```

Gunicorn ile çalıştırmak için:
```bash
gunicorn safepackisg.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

Nginx konfigürasyonu için proje wiki'sine bakın.

---

## Teknoloji Yığını

- **Backend:** Django 5.0, Python 3.11+
- **Veritabanı:** SQLite (geliştirme) / PostgreSQL (üretim)
- **Statik Dosyalar:** WhiteNoise
- **Görseller:** Pillow
- **Editör:** django-ckeditor
- **Form:** django-crispy-forms + crispy-bootstrap5
- **Deploy:** Gunicorn + Nginx

---

## Katkıda Bulunma

Geliştirmeler için bir branch açın, değişikliklerinizi commit edin ve PR gönderin.
