from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.conf import settings
import textile, os

register = template.Library()

@register.filter
def totextile (name):
    """ Textile a text """
    try:
        f = file ( os.path.join (settings.MARK_DOWN, "%s.txt" % (name)), "r" )
    except IOError:
        return name
    contents = f.read ()
    reply = textile.textile(contents)
    print reply
    #contents = contents.replace ("\n","<br/>")
    return mark_safe (reply)

@register.filter
def snippet (name):
    """ Load a snippet """
    try:
        f = file ( os.path.join (settings.MARK_DOWN, "%s.txt" % (name)), "r" )
    except IOError:
        return name
    contents = f.read ()
    #reply = textile.textile(contents)
    contents = contents.replace ("\n","<br/>")
    return mark_safe (contents)


@register.filter
def nobrsnippet (name):
    """ Load a textile snippet """
    try:
        f = file ( os.path.join (settings.MARK_DOWN, "%s.txt" % (name)), "r" )
    except IOError:
        return name
    contents = f.read ()
    #reply = textile.textile(contents)
    #contents = contents.replace ("\n","<br/>")
    return mark_safe (contents)



@register.filter
def fileslug (name):
    return name.split (".")[0]
