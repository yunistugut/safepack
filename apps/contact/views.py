from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .forms import ContactForm


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save()

            # Firmaya bildirim e-postası
            try:
                body = render_to_string('contact/email_notification.txt', {'msg': msg})
                send_mail(
                    subject=f'[SafePackISG] Yeni Teklif Talebi: {msg.get_subject_display()} — {msg.name}',
                    message=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass  # Prod'da loglama ekleyin

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                from django.http import JsonResponse
                return JsonResponse({'success': True})

            messages.success(request, 'Talebiniz alındı! En kısa sürede size ulaşacağız.')
            return redirect('contact:success')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                from django.http import JsonResponse
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = ContactForm()

    context = {
        'form': form,
        'meta_title': 'İletişim | SafePackISG – Teklif ve Bilgi Talebi',
        'meta_description': 'SafePackISG ile iletişime geçin. Teklif alın veya ISG danışmanlığı için bize ulaşın.',
    }
    return render(request, 'contact/contact.html', context)


def contact_success(request):
    return render(request, 'contact/success.html', {
        'meta_title': 'Talebiniz Alındı | SafePackISG',
    })
