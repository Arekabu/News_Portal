from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from .models import PostCategory, Post
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime, timezone
from django.core.exceptions import PermissionDenied

def send_notifications(preview, pk, title, subscribers, username):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'username': username,
            'title': title,
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')

    msg.send()

@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        # subscribers_emails = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            # subscribers_emails += [s.email for s in subscribers]
            for sub in subscribers:
                send_notifications(instance.preview(), instance.pk, instance.title, [sub.email], sub.username)

        # send_notifications(instance.preview(), instance.pk, instance.title, subscribers_emails)

@receiver(pre_save, sender=Post)
def day_post_counter(sender, instance, **kwargs):
    posts_today = Post.objects.filter(author=instance.author, date__gte=datetime.now(timezone.utc).date()).count()
    if posts_today >=3:
        raise PermissionDenied( "Вы можете публиковать максимум 3 поста в сутки!")