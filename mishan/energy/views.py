from django.http import *
from django.shortcuts import render_to_response
from mishan.energy.models import *

def slug (string):
    return "_".join (re.findall ("\w+", string)).lower ()

def get_board (dictionary = False):
    f = file ( os.path.join (settings.MARK_DOWN, "static", "directors.txt" ), "r" )
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
        print board
    return render_to_response ( "%s.html" %(pagename), locals() )

def board (request, member = ""):
    """ Serves a member's page """
    board = get_board (True)
    dictboard = get_board ()
    membername = dictboard[member]
    return render_to_response ( "board.html", locals() )


