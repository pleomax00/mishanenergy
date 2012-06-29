from django.http import *
from django.shortcuts import render_to_response
from django import forms
from django.db.models import *
from django.contrib.auth.models import User
from django.conf import settings
import xmlrpclib

class EmailRegForm (forms.Form):
    full_name = forms.CharField (label = "Full Name", max_length = 30)
    email = forms.EmailField (max_length = 512)
    password = forms.CharField (label = "Set Password", widget=forms.PasswordInput, max_length = 32, min_length = 4)
    retype_password = forms.CharField (label = "Retype Password", widget=forms.PasswordInput, max_length = 32)
    alternate_email = forms.EmailField (label = "Alternate Email", max_length = 512)
    master_password = forms.CharField (label = "Mater Password", widget=forms.PasswordInput)

    def clean_master_password (self):
        passwd = self.cleaned_data.get ('master_password')
        if passwd != settings.MASTER_PASSWORD:
            raise forms.ValidationError ("To create a new user, you need to provide valid master password.")

    def clean_retype_password (self):
        data1 = self.cleaned_data.get ('password')
        data2 = self.cleaned_data.get ('retype_password')
        print data1, data2
        if data1 != data2:
            raise forms.ValidationError ("Both the supplied passwords must match")
        return data1

    def clean_email (self):
        email = self.cleaned_data.get ('email')
        domain = email.split ("@")[1]
        if domain.strip() != 'mishanenergy.com':
            raise forms.ValidationError ("You can only create an email address for mishanenergy.com (e.g username@mishanenergy.com)")
        try:
            user = User.objects.get (email = email)
            raise forms.ValidationError ("This email ID is already being used by " + user.first_name)
        except User.DoesNotExist:
            pass
        return email


def index (request):
    """ serves /admin """
    return render_to_response ("admin/index.html", locals())


def createmail (request):
    """ serves /admin/createmail """
    if request.method == "POST":
        eform = EmailRegForm (request.POST)
        if eform.is_valid ():
            email = eform.cleaned_data.get ('email')
            password = eform.cleaned_data.get ('password')
            name = eform.cleaned_data.get ('full_name')
            alternate_email = eform.cleaned_data.get ('alternate_email')

            u = User.objects.create_user (email, email)
            u.first_name = name
            u.last_name = alternate_email
            u.set_password (password)

            u.save ()

            server = xmlrpclib.ServerProxy ('https://api.webfaction.com/')
            session_id, account = server.login (settings.WEBFACTION_USER, settings.WEBFACTION_PASSWORD)

            emailname = email.split ("@")[0]
            response = server.create_mailbox (session_id, emailname, False)
            resp = server.create_email (session_id, email, emailname)

            return HttpResponseRedirect ("/admin/createmail?msg=success&email=" + eform.cleaned_data.get ('email'))
    else:
        eform = EmailRegForm ()

    users = User.objects.all ()
    return render_to_response ("admin/createmail.html", locals())

def deletemail (request, iid):
    u = User.objects.get (id = iid)
    
    server = xmlrpclib.ServerProxy ('https://api.webfaction.com/')
    session_id, account = server.login (settings.WEBFACTION_USER, settings.WEBFACTION_PASSWORD)

    try:
        server.delete_email (session_id, u.email)
        emailname = u.email.split ("@")[0]
        server.delete_mailbox (session_id, emailname)
    except:
        print "Cannot remove", u.email
        pass

    email = u.email
    u.delete()
    return HttpResponseRedirect ('/admin/createmail?msg=deleted&email=' + email)
