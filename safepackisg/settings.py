"""
SafePackISG — Django Ayarları
Geliştirme ve üretim için tek settings dosyası (environ ile kontrol edilir).
"""

from pathlib import Path
import os
import environ

# ─── Temel Yollar ─────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# environ ile .env dosyasını oku (.env yoksa (Render) ortam değişkenlerini kullan)
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ['localhost', '127.0.0.1']),
)
env_file = BASE_DIR / '.env'
if env_file.exists():
    environ.Env.read_env(env_file)

# ─── Güvenlik ─────────────────────────────────────
SECRET_KEY = env('SECRET_KEY', default='django-insecure-gecici-key-lutfen-degistirin')
DEBUG = env('DEBUG')

# ALLOWED_HOSTS: .env'den veya Render ortam değişkeninden oku
_allowed = env('ALLOWED_HOSTS', default='localhost,127.0.0.1')
if isinstance(_allowed, str):
    ALLOWED_HOSTS = [h.strip() for h in _allowed.split(',')]
else:
    ALLOWED_HOSTS = _allowed

# Render'ın otomatik verdiği hostname'i de ekle
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# ─── Uygulamalar ──────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.humanize',

    # 3. parti
    'crispy_forms',
    'crispy_bootstrap5',
    'ckeditor',
    'ckeditor_uploader',
    'django_cleanup.apps.CleanupConfig',

    # Proje uygulamaları
    'apps.core',
    'apps.products',
    'apps.blog',
    'apps.contact',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',       # Statik dosya servisi
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'safepackisg.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Tüm sayfalarda kullanılacak global context
                'apps.core.context_processors.global_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'safepackisg.wsgi.application'

# ─── Veritabanı ───────────────────────────────────
# Geliştirme: SQLite | Üretim: DATABASE_URL ile PostgreSQL
DATABASES = {
    'default': env.db(
        'DATABASE_URL',
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}'
    )
}

# ─── Şifre Doğrulama ──────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─── Uluslararasılaştırma ─────────────────────────
LANGUAGE_CODE = 'tr'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_TZ = True

# ─── Statik Dosyalar ──────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ─── Medya Dosyaları ──────────────────────────────
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ─── E-posta ──────────────────────────────────────
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='SafePackISG <info@safepackisg.com>')
CONTACT_EMAIL = env('CONTACT_EMAIL', default='info@safepackisg.com')

# ─── Crispy Forms ─────────────────────────────────
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# ─── CKEditor ─────────────────────────────────────
CKEDITOR_UPLOAD_PATH = 'uploads/ckeditor/'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent'],
            ['Link', 'Unlink'],
            ['Image', 'Table'],
            ['Source'],
        ],
        'height': 300,
    },
}

# ─── Site Bilgileri ───────────────────────────────
SITE_URL = env('SITE_URL', default='https://www.safepackisg.com')
SITE_NAME = env('SITE_NAME', default='SafePackISG')

# ─── Üretim Güvenlik Ayarları ─────────────────────
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
