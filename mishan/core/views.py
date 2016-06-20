from django.http import *
from django.shortcuts import render_to_response
from django.conf import settings
from mishan.core.models import *
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout, get_backends
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json, re
from mishan.core.forms import *
import textile, shutil

def index ( request ):
    """ Index page for mishanenergy """
    pagename = ""
    string = file ( os.path.join (settings.MARK_DOWN, "static", "homepage.txt") ).read()
    hometext = textile.textile(string)
    return render_to_response ( "index.html", locals() )


def webinar_reg ( request ):
    """ Register for webinar """
    name = request.POST.get ( "name", "Unknown" )
    city = request.POST.get ( "city", "Unknown Place" )
    email = request.POST.get ( "email", "foo@bar.com" )
    mobile = request.POST.get ( "cell", "xxxxxxxxxx" )

    form = WebinarRegistration ( name = name, city = city, email = email, mobile = mobile )
    form.save()

    textual = """%s registered for webinar.\nEmail: %s\nCity: %s\nCell Num: %s\n\nThanks,\nFullEdge Admin """ % (name, email, city, mobile)
    to = settings.LINE_MANAGERS
    from_email = '"Fulledge Support" <support@mishanenergy.com>' 
    send_mail ( "New Webinar Registration", textual, from_email, to, fail_silently=False )

    response = {
        "status": "ok",
        "text": "Thanks for your interest, we'll get back to you shortly!",
    }

    return HttpResponse ( json.dumps (response) )


def make_logout ( request ):
    """ Logs out a user """
    logout ( request )
    return HttpResponseRedirect ( "/" )


@login_required
def adminhome (request):
    """ Admin's front page """
    return render_to_response ( "admin.html", locals() )


def register (request):
    """ Handle login page """
    if request.method == "POST":
        regform = RegisterForm(request.POST)
        if regform.is_valid ():
            email = regform.cleaned_data["email"]
            password = regform.cleaned_data["password"]
            name = regform.cleaned_data["name"]
            user = User.objects.create_user ( email, email, password )
            user.first_name = name
            user.save()
            return HttpResponseRedirect ("/auth/login?msg=success")
    else:
        regform = RegisterForm()
    return render_to_response ( "login.html", locals() )


def dologin (request):
    """ Logs in a user """
    username = request.POST['email']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    nexturl = request.POST.get ( "next", "/" )
    if nexturl == "":
        nexturl = "/"
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect (nexturl)
        else:
            return HttpResponseRedirect ( "/auth/login?error=disabled" )
    else:
            return HttpResponseRedirect ( "/auth/login?error=invalid" )


@login_required
def registrations (request):
    regs = WebinarRegistration.objects.order_by ("-id")
    return render_to_response ( "registrations.html", locals() )


def blogview (request, fixed_view = None):
    pagename = "blog"
    PAGE_LENGTH = 5
    pagenum = int(request.GET.get ("page", "1"))
    if fixed_view:
        blogs = [Blog.objects.get (seoid=fixed_view)]
    else:
        blogs = Blog.objects.order_by ("-id")
    pages = Paginator(blogs, PAGE_LENGTH, orphans = 2)
    this_page = pages.page(pagenum)
    return render_to_response ( "blog.html", locals() )


def getseoid (string):
    string = string.lower().strip()
    allwords = re.findall ( "[a-z0-9]+", string )
    return "-".join (allwords)

@login_required
def blogpost (request):
    if request.method == "POST":
        try: bid = int(request.POST.get ("bid", "0"))
        except ValueError: bid = 0
        blogform = BlogPostForm (request.POST)
        if blogform.is_valid():
            if bid == 0:
                b = Blog ( title = blogform.cleaned_data['title'], tags = blogform.cleaned_data['tags'], catagory = blogform.cleaned_data['catagory'],
                       post = blogform.cleaned_data['post'], author = request.user, seoid = getseoid(blogform.cleaned_data['title']) )
            else:
                b = Blog.objects.get (id = bid)
                b.title = blogform.cleaned_data['title']
                b.tags = blogform.cleaned_data['tags']
                b.catagory = blogform.cleaned_data['catagory']
                b.post = blogform.cleaned_data['post']
                b.seoid = getseoid(blogform.cleaned_data['title'])
            b.save()
            saved = True
    else:
        editing = request.GET.get ("edit", None)
        if editing:
            b = Blog.objects.get (id = int(editing))
            blogform = BlogPostForm ({"title": b.title, "tags": b.tags, "catagory": b.catagory, "post": b.post} )
        else:
            blogform = BlogPostForm ()
    return render_to_response ( "blogpost.html", locals() )


def services_page (request, page):
    page_titles = { 
        "aboutus": "About Us", 
        "contactus": "Contact Us", 
        "newsnevents": "News & Events",
        "termsofservice": "Terms Of Service",
        "privacy": "Privacy",
    }
    pagename = page
    title = page_titles[page] if page_titles.has_key (page) else ""
    services = False
    for i in settings.SERVICES:
        if i[0] == page:
            services = True
            title = i[1]
            pagename = "services"
            break
    string = file ( os.path.join (settings.MARK_DOWN, "static", page+".txt") ).read()
    service_contents = textile.textile(string)
    return render_to_response ( "services.html", locals() )


def autocomplete_post (request):
    markdown = request.POST.get ( "text", "your post goes here..." )
    reply = textile.textile(markdown)
    return HttpResponse (reply)


@login_required
def uploadmedia (request):
    host = request.META.get ( "HTTP_HOST", "mishanenergy.com" )
    links = []
    if request.method == "POST":
        for i in request.FILES:
            this_file = request.FILES[i]
            ofilename = os.path.join ( settings.PATH_ROOT, "static", "uploads", this_file.name )
            shutil.copyfileobj ( this_file.file, file(ofilename, "w") )
            links.append (this_file.name)
    return render_to_response ( "upload.html", locals() ) 


def contactus (request):
    pagename = "contactus"
    if request.method == "POST":
        contactusform = ContactUsForm (request.POST)
        if contactusform.is_valid():
            name = contactusform.cleaned_data['name']
            enquiry = contactusform.cleaned_data['enquiry']
            cellnum = contactusform.cleaned_data['cellnum']
            company = contactusform.cleaned_data['company']
            email = contactusform.cleaned_data['email']
            textual = """Name: %s\nEmail: %s\nCell Number: %s\nCompany: %s\nEnquiry: %s\n\nThanks,\nFullEdge Admin """ % (name, email, cellnum, company, enquiry)
            to = settings.LINE_MANAGERS
            from_email = '"Fulledge Enquiry" <support@mishanenergy.com>' 
            send_mail ( "New Enquiry at FullEdge's Website", textual, from_email, to, fail_silently=False )
            success = True
            contactusform = ContactUsForm ()
    else:
        contactusform = ContactUsForm ()
    return render_to_response ( "contactus.html", locals() )


@login_required
def texteditor (request):
    files_dir = os.path.join ( settings.PATH_ROOT, "markdown", "static" )
    editing = request.GET.get ( "file", None )

    if request.method == "POST":
        ofile = os.path.join (files_dir, editing)
        file ( ofile, "w" ).write (request.POST.get("fcontents"))
        filecontents = request.POST.get("fcontents")

    if editing == None:
        list_files = os.listdir (files_dir)
    else:
        filecontents = file ( os.path.join (files_dir, editing) ).read ()

    return render_to_response ( "texteditor.html", locals() )

