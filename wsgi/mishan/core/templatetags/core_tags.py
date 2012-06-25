from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.conf import settings
import textile

register = template.Library()

@register.filter
def totextile (text):
    """ Textile a text """
    reply = textile.textile(text)
    return mark_safe(reply)


