from django.http import *
from django.shortcuts import render_to_response
from django import forms
from django.db.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.models import check_password
from django.conf import settings
from django.forms.extras.widgets import SelectDateWidget
import xmlrpclib, os
from mishan.energy.models import *
import hashlib
from django.contrib.auth import authenticate, login as djangologin, logout as djangologout, get_backends

class NewsForm (forms.Form):
    news_text = forms.CharField (label = "News Text", max_length = 100, widget=forms.Textarea)
    date = forms.DateField(initial=datetime.date.today, widget=SelectDateWidget())

class EmailRegForm (forms.Form):
    full_name = forms.CharField (label = "Full Name", max_length = 30)
    email = forms.EmailField (max_length = 512)
    password = forms.CharField (label = "Set Password", widget=forms.PasswordInput, max_length = 32, min_length = 4)
    retype_password = forms.CharField (label = "Retype Password", widget=forms.PasswordInput, max_length = 32)
    alternate_email = forms.EmailField (label = "Alternate Email", max_length = 512)
    master_password = forms.CharField (label = "Mater Password", widget=forms.PasswordInput)

    def clean_master_password (self):
        passwd = self.cleaned_data.get ('master_password')
        if settings.MASTER_PASSWORD != hashlib.md5 (passwd).hexdigest():
            raise forms.ValidationError ("To create a new user, you need to provide valid master password.")

    def clean_retype_password (self):
        data1 = self.cleaned_data.get ('password')
        data2 = self.cleaned_data.get ('retype_password')
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


#@login_required
def index (request):
    """ serves /admin """
#    if request.email not in settings.LINE_MANAGERS:
#        raise Http404
    return render_to_response ("admin/index.html", locals())


@login_required
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

            #server = xmlrpclib.ServerProxy ('https://api.webfaction.com/')
            #session_id, account = server.login (settings.WEBFACTION_USER, settings.WEBFACTION_PASSWORD)

            emailname = email.split ("@")[0]
            if settings.MODE == "PRODUCTION":
                os.system ("sudo useradd %s" %(emailname))
                os.system ("echo '%s:%s' | sudo chpasswd" % (emailname, password))
                os.system ("sudo mkdir /home/%s" %(emailname))
                os.system ("sudo chown -R %s:%s /home/%s" %(emailname, emailname, emailname))
            #response = server.create_mailbox (session_id, emailname, False)
            #resp = server.create_email (session_id, email, emailname)

            return HttpResponseRedirect ("/admin/createmail?msg=success&email=" + eform.cleaned_data.get ('email'))
    else:
        eform = EmailRegForm ()

    users = User.objects.all ()
    return render_to_response ("admin/createmail.html", locals())

@login_required
def deletemail (request, iid):
    u = User.objects.get (id = iid)
    
    #server = xmlrpclib.ServerProxy ('https://api.webfaction.com/')
    #session_id, account = server.login (settings.WEBFACTION_USER, settings.WEBFACTION_PASSWORD)

    #try:
    #    server.delete_email (session_id, u.email)
    ##    emailname = u.email.split ("@")[0]
    #    server.delete_mailbox (session_id, emailname)
    #except:
    #    print "Cannot remove", u.email
    #    pass

    email = u.email
    emailname = email.split ("@")[0]
    if settings.MODE == "PRODUCTION":
        os.system ("sudo userdel %s" %(emailname))
        os.system ("sudo mv /home/%s /home/ubuntu/backup/delusers" % (emailname))

    u.delete()
    return HttpResponseRedirect ('/admin/createmail?msg=deleted&email=' + email)


def changepassword (request):
    """ Changes the password """
    if request.method == "POST":
        email = request.POST.get ('email', '')
        old = request.POST.get ('old', '')
        new1 = request.POST.get ('new1', '')
        new2 = request.POST.get ('new2', '')
        if old == '' or new1 == '' or new2 == '' or email == '':
            return HttpResponseRedirect ('/admin/changepassword?error=allfieldsreq')
        if len(new1) < 4:
            return HttpResponseRedirect ('/admin/changepassword?error=minchar')
        if new1 != new2:
            return HttpResponseRedirect ('/admin/changepassword?error=match')

        try:
            u = User.objects.get (email = email)
        except User.DoesNotExist:
            return HttpResponseRedirect ('/admin/changepassword?error=nosuchuser&email='+email)
        
        if not u.check_password (old):
            return HttpResponseRedirect ('/admin/changepassword?error=nopassmatch&email='+email)

        u.set_password (new1)
        u.save ()
        emailname = u.email.split ("@")[0]
        if settings.MODE == "PRODUCTION":
            os.system ("echo '%s:%s' | sudo chpasswd" % (emailname, new1))
        return HttpResponseRedirect ('/admin/changepassword?msg=success')

    return render_to_response ("admin/changepassword.html", locals())


@login_required
def textstrings (request):
    """ Change web sites text strings """
    if not request.user.is_staff:
        return HttpResponseRedirect ("/auth/login?msg=noperm")
    textpath = os.path.join (settings.MARK_DOWN)
    files = filter (lambda x: x.endswith ('.txt'), os.listdir (textpath))
    return render_to_response ("admin/textstrings.html", locals())

@login_required
def settextstring (request):
    """ Save a file """
    if not request.user.is_staff:
        return HttpResponseRedirect ("/auth/login?msg=noperm")
    textpath = os.path.join (settings.MARK_DOWN, request.POST.get ('file'))
    if not textpath.endswith (".txt"):
        textpath += ".txt"
    file (textpath, "wb+").write (request.POST.get ('value'))
    if request.POST.has_key ("next"):
        return HttpResponseRedirect (request.POST.get ("next"))
    return HttpResponse ("{}")


@login_required
def editnews (request):
    """ News editor """
    if not request.user.is_staff:
        return HttpResponseRedirect ("/auth/login?msg=noperm")
    if request.method == "POST":
        nform = NewsForm (request.POST)
        if nform.is_valid ():
            news = nform.cleaned_data.get ("news_text")
            when = nform.cleaned_data.get ("date")
            n = News (news = news, date = when)
            n.save ()
            nform = NewsForm ()
    else:
        nform = NewsForm ()

    newss = News.objects.all ()
    return render_to_response ("admin/newsedit.html", locals ())


@login_required
def removenews (request, iid):
    """ Remove a news """
    n = News.objects.get (id = iid)
    n.delete ()
    return HttpResponseRedirect ("/admin/news?action=removed")


def loginpage (request):
    """ Serves login page """
    if request.method == "POST":
        login = request.POST.get ("login", "")
        password = request.POST.get ("password", "")
        print login, password
        if login == "" or password == "":
            return HttpResponseRedirect ("/auth/login?error=allfields&next=" + request.POST.get('next','/admin'))
        user = authenticate ( username = login, password = password )
        print user
        if user is not None:
            djangologin (request, user)
            return HttpResponseRedirect (request.GET.get ("next", "/admin"))
        print user
    return render_to_response ("admin/login.html", locals())


def logout (request):
    djangologout (request)
    return HttpResponseRedirect ("/admin")

@login_required
def staff (request, action, uid):
    if not request.user.is_staff:
        return HttpResponseRedirect ("/auth/login?msg=noperm")
    u = User.objects.get (id = uid)
    if action == "staff":
        u.is_staff = True
    else:
        u.is_staff = False
    u.save ()
    return HttpResponseRedirect ("/admin/createmail")
