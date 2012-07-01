from django.http import *
from django.shortcuts import render_to_response

def index (request):
    """ Serves / of the home page """
    return render_to_response ( "index.html", locals() )

def about (request):
    """ Serves /about of the home page """
    return render_to_response ( "about.html", locals() )


