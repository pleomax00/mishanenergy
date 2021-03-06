from django.conf.urls.defaults import patterns, include, url
#from mishan.core.views import *

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()
from mishan.energy.admin import *

urlpatterns = patterns('',
    url(r'^$', 'mishan.energy.views.index'),
    url(r'^about$', 'mishan.energy.views.about'),
    url(r'^about/(\w+)$', 'mishan.energy.views.about'),
    url(r'^about/board/(\w+)$', 'mishan.energy.views.board'),
    url(r'^services$', 'mishan.energy.views.services'),
	url(r'^manufacturing$', 'mishan.energy.views.manufacturing'),
    url(r'^contactus$', 'mishan.energy.views.contact'),
    url(r'^partners/(alliances)$', 'mishan.energy.views.genericpage'),
    url(r'^partners/(clients)$', 'mishan.energy.views.genericpage'),
    url(r'^careers$', 'mishan.energy.views.careers'),
    url(r'^(portfolio)$', 'mishan.energy.views.genericpage'),
    url(r'^portfolio/(labourlicense)$', 'mishan.energy.views.labourlicense'),
    url(r'^portfolio/(documents)$', 'mishan.energy.views.documents'),
    url(r'^(termsnconditions)$', 'mishan.energy.views.genericpage'),
    url(r'^(privacypolicy)$', 'mishan.energy.views.genericpage'),
    url(r'^(securitypolicy)$', 'mishan.energy.views.genericpage'),

    url(r'^admin$', 'mishan.energy.admin.index'),
    url(r'^admin/createmail$', createmail),
    url(r'^admin/block$', blockuser),
    url(r'^admin/files$', uploader),
    url(r'^admin/removefile$', removefile),
    url(r'^admin/changepassword$', changepassword),
    url(r'^admin/mail/delete/(\d+)$', deletemail),
    url(r'^admin/textstrings$', textstrings),
    url(r'^admin/settextval$', settextstring),
    url(r'^admin/news$', editnews),
    url(r'^admin/removenews/(\d+)$', removenews),
    url(r'^admin/(staff)/(\d+)$', staff),
    url(r'^admin/(unstaff)/(\d+)$', staff),

    url(r'^auth/login$', 'mishan.energy.admin.loginpage'),
    url(r'^auth/logout$', 'mishan.energy.admin.logout'),

)

