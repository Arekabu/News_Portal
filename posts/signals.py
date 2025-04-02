from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from .models import PostCategory, Post
from datetime import datetime, timezone
from django.core.exceptions import PermissionDenied
from .tasks import new_post_notification

@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        new_post_notification.apply_async([instance.pk])

@receiver(pre_save, sender=Post)
def day_post_counter(sender, instance, **kwargs):
    posts_today = Post.objects.filter(author=instance.author, date__gte=datetime.now(timezone.utc).date()).count()
    if posts_today >=3:
        raise PermissionDenied("Вы можете публиковать максимум 3 поста в сутки!")