/**
 * SafePackISG — Ana JavaScript Dosyası
 * static/js/main.js
 */

document.addEventListener('DOMContentLoaded', () => {

  // ── Header scroll shadow ──────────────────────────
  const header = document.querySelector('header');
  if (header) {
    window.addEventListener('scroll', () => {
      header.classList.toggle('scrolled', window.scrollY > 10);
    }, { passive: true });
  }

  // ── Hamburger menü ───────────────────────────────
  const hamburger = document.querySelector('.hamburger');
  const mainNav = document.querySelector('nav[aria-label="Ana navigasyon"]');
  if (hamburger && mainNav) {
    hamburger.addEventListener('click', () => {
      const isOpen = hamburger.getAttribute('aria-expanded') === 'true';
      hamburger.setAttribute('aria-expanded', String(!isOpen));
      hamburger.textContent = isOpen ? '☰' : '✕';
      if (isOpen) {
        mainNav.removeAttribute('style');
      } else {
        Object.assign(mainNav.style, {
          display: 'flex',
          flexDirection: 'column',
          position: 'fixed',
          top: '70px',
          left: '0',
          right: '0',
          background: '#fff',
          padding: '1rem 1.5rem',
          boxShadow: '0 8px 24px rgba(0,0,0,.1)',
          zIndex: '999',
          gap: '0',
        });
      }
    });

    // Dışarı tıklandığında menüyü kapat
    document.addEventListener('click', (e) => {
      if (!header.contains(e.target) && hamburger.getAttribute('aria-expanded') === 'true') {
        hamburger.click();
      }
    });
  }

  // ── Keyboard: Escape ile menü kapat ──────────────
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && hamburger?.getAttribute('aria-expanded') === 'true') {
      hamburger.click();
      hamburger.focus();
    }
  });

  // ── Smooth anchor scroll ─────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', (e) => {
      const target = document.querySelector(a.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ── Form submit loading state ────────────────────
  const contactForm = document.getElementById('contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', function () {
      const btn = this.querySelector('.btn-submit');
      if (btn) {
        btn.textContent = '⏳ Gönderiliyor…';
        btn.disabled = true;
      }
    });
  }

  // ── Lazy loading fallback ────────────────────────
  if ('loading' in HTMLImageElement.prototype) {
    // Native lazy loading destekleniyor
  } else {
    // Polyfill gerekiyorsa buraya ekleyin
  }

  // ── WhatsApp float butonu (opsiyonel) ────────────
  // Tüm sayfalarda sağ altta görünür WhatsApp butonu
  const wpBtn = document.createElement('a');
  wpBtn.href = 'https://wa.me/905001234567?text=Merhaba%2C+bilgi+almak+istiyorum.';
  wpBtn.target = '_blank';
  wpBtn.rel = 'noopener noreferrer';
  wpBtn.setAttribute('aria-label', 'WhatsApp ile iletişim');
  wpBtn.style.cssText = `
    position: fixed; bottom: 1.5rem; right: 1.5rem; z-index: 900;
    width: 54px; height: 54px; border-radius: 50%; background: #25D366;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.6rem; box-shadow: 0 4px 16px rgba(37,211,102,.4);
    transition: transform .2s, box-shadow .2s; text-decoration: none;
  `;
  wpBtn.textContent = '💬';
  wpBtn.addEventListener('mouseenter', () => {
    wpBtn.style.transform = 'scale(1.1)';
    wpBtn.style.boxShadow = '0 6px 24px rgba(37,211,102,.5)';
  });
  wpBtn.addEventListener('mouseleave', () => {
    wpBtn.style.transform = '';
    wpBtn.style.boxShadow = '0 4px 16px rgba(37,211,102,.4)';
  });
  document.body.appendChild(wpBtn);

});
