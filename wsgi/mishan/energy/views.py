from django.http import *

def index (request):
    """ Serves / of the home page """
    return HttpResponse ("OK")

