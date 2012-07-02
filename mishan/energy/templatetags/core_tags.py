from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.conf import settings
import textile, os

register = template.Library()

@register.filter
def totextile (text):
    """ Textile a text """
    reply = textile.textile(text)
    return mark_safe(reply)

@register.filter
def snippet (name):
    """ Load a textile snippet """
    try:
        f = file ( os.path.join (settings.MARK_DOWN, "static", "%s.txt" % (name)), "r" )
    except IOError:
        return name
    contents = f.read ()
    #reply = textile.textile(contents)
    return mark_safe (contents)


@register.filter
def fileslug (name):
    return name.split (".")[0]
