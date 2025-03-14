from datetime import datetime, timezone
from django import template

register = template.Library()

@register.simple_tag()
def current_time(format_string='%b %d %Y'):
    return datetime.now(timezone.utc).strftime(format_string)

@register.simple_tag(takes_context=True)
def object_title(context):
    if '/articles/' in f'{context['request']}':
       title = 'Статья'
    else:
       title = 'Новость'
    return title