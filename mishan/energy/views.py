from django.http import *
from django.shortcuts import render_to_response
from mishan.energy.models import *
from django.core.mail import send_mail, EmailMessage

def slug (string):
    return "_".join (re.findall ("\w+", string)).lower ()

def get_board (dictionary = False):
    f = file ( os.path.join (settings.MARK_DOWN, "directors.txt" ), "r" )
    contents = f.read ()
    board = contents.split (",")
    board = map ( lambda x: x.strip(), board )
    if dictionary:
        board = map (lambda x: (slug(x), x), board)
        return board
    boardmembers = {}
    for i in board:
        boardmembers[slug(i)] = i

    return boardmembers

def index (request):
    """ Serves / of the home page """
    news = News.objects.order_by ("-date")
    return render_to_response ( "index.html", locals() )

def about (request, pagename = "about"):
    """ Serves /about of the home page """
    if pagename == "board":
        board = get_board (True)
    return render_to_response ( "%s.html" %(pagename), locals() )

def board (request, member = ""):
    """ Serves a member's page """
    board = get_board (True)
    dictboard = get_board ()
    membername = dictboard[member]
    return render_to_response ( "board.html", locals() )

def services (request):
    """ Serves /services of the site """
    return render_to_response ( "services.html", locals() )

def manufacturing (request):
    """ Serves /services of the site """
    return render_to_response ( "manufacturing.html", locals() )

def contact (request):
    """ Serves /contact of the site """
    if request.method == "POST":
        message = request.POST.get ("message", "Blank Message")
        subject = request.POST.get ("subject", "Empty Subject")
        email = request.POST.get ("email", "no_email_provided")
        name = request.POST.get ("name", "Unknown")

        textual = """%s filled contact form on mishanenergy.com\nEmail: %s\nMessage: %s\n\nThanks,\nMishanEnergy Admin """ % (name, email, message)
        to = settings.LINE_MANAGERS
        from_email = '"MishanEnergy Admin" <support@mishanenergy.com>' 
        send_mail ( "[Contact Us Filled] %s" %(subject), textual, from_email, to, fail_silently=False )

    return render_to_response ( "contact.html", locals() )

def genericpage (request, page):
    """ Serves a generic page """
    title = page.capitalize ()
    titlename = page+"_h2"
    titledesc = page+"_minidesc"
    pagetext = page+"_text"
    image = page+"_head"
    return render_to_response ( "genericpage.html", locals() )

def labourlicense (request, page):
    """ Serves a generic page """
    title = page.capitalize ()
    titlename = page+"_h2"
    titledesc = page+"_minidesc"
    pagetext = page+"_text"
    image = "portfolio_head"
    return render_to_response ( "labourlicense.html", locals() )


def documents (request, page):
    """ Serves a generic page """
    title = page.capitalize ()
    titlename = page+"_h2"
    titledesc = page+"_minidesc"
    pagetext = page+"_text"
    image = "portfolio_head"
    docs = UploadFile.objects.all ()
    return render_to_response ( "documents.html", locals() )



def careers (request):
    """ Serves a generic page """
    page = "careers"
    if request.method == "POST":
        fileobj = request.FILES['resume']
        fname = fileobj.name
        outfname = "/tmp/%s" % (fname)
        file (outfname, "wb+").write (fileobj.read ())
        if fileobj._size > 10 * 1024 * 1024:
            return HttpResponseRedirect ("/careers?error=filesize")
        email = EmailMessage ('A new resume uploaded', 'Please find attached\n\nMishan Energy Admin', '"Resume Support" <noreply@mishanenergy.com>', settings.LINE_MANAGERS)
        email.attach_file (outfname)
        email.send ()
        return HttpResponseRedirect ("/careers?msg=sent")
    title = page.capitalize ()
    titlename = page+"_h2"
    titledesc = page+"_minidesc"
    pagetext = page+"_text"
    image = page+"_head"

    return render_to_response ( "careers.html", locals() )


