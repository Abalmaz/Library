from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from .models import User, Book
from django.core.mail import send_mail
from celery import shared_task


@shared_task
def send_new_book():
    """
    The task which sends emails to users with new books.
    """
    context = {}
    last_week = timezone.now() - timedelta(days=7)
    new_books = Book.objects.filter(
        created_at__gte=last_week).order_by('-created_at')[:5]
    if new_books:
        books = list()
        for book in new_books:
            books.append(dict(title=book.title,
                              url=''.join([get_current_site(None).domain,
                                           book.get_absolute_url()])))
        context['books'] = books
        subject = 'New book'
        message = render_to_string('mylib/mail.html', context)
        mail_from = settings.EMAIL_HOST_USER
        users_emails = User.objects.filter(is_subscription=True).values_list(
            'email', flat=True)
        if users_emails:
            send_mail(message=message,
                      html_message=message,
                      recipient_list=users_emails,
                      from_email=mail_from,
                      subject=subject)
