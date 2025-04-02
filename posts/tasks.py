from celery import shared_task
# import time
from .models import Post, Category
from datetime import datetime, timezone, timedelta
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

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

@shared_task
def new_post_notification(post_id):
    post = Post.objects.get(pk = post_id)
    categories = post.category.all()
    for cat in categories:
        subscribers = cat.subscribers.all()
        for sub in subscribers:
            send_notifications(post.preview(), post_id, post.title, [sub.email], sub.username)

@shared_task
def weekly_notification():
    today = datetime.now(timezone.utc)
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(date__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

# @shared_task
# def printer(N):
#     for i in range(N):
#         time.sleep(1)
#         print(i+1)
#
# @shared_task
# def complete_order(oid):
#     order = Order.objects.get(pk = oid)
#     order.complete = True
#     order.save()
#
# @shared_task
# def clear_old():
#     old_orders = Order.objects.all().exclude(time_in__gt = datetime.now(timezone.utc) - timedelta(minutes = 5))
#     old_orders.delete()