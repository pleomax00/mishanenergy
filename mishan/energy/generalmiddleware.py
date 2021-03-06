from django.conf import settings 
from django.http import HttpResponseRedirect
import os

class GeneralMiddleware(object):

    def process_request ( self, request ):
        """ Automatic page loads for correct browser """

        host = request.META.get ( "HTTP_HOST", "digisalts.com" )
        if host in settings.REDIRECTION_RULES[0]:
            return HttpResponseRedirect ( "http://" + settings.REDIRECTION_RULES[1] )

        request.MENU = settings.MENU
        request.SERVICES = settings.SERVICES
        if request.user.is_authenticated():
            if request.user.email in settings.LINE_MANAGERS:
                request.is_admin = True

