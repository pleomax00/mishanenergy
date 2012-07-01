from django.conf.urls.defaults import patterns, include, url
#from mishan.core.views import *

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()
from mishan.energy.admin import *

urlpatterns = patterns('',
    url(r'^$', 'mishan.energy.views.index'),
    url(r'^about$', 'mishan.energy.views.about'),

    url(r'^admin$', 'mishan.energy.admin.index'),
    url(r'^admin/createmail$', createmail),
    url(r'^admin/changepassword$', changepassword),
    url(r'^admin/mail/delete/(\d+)$', deletemail),
    # url(r'^di/', include('di.foo.urls')),
)

"""(r'^$', index),
    (r'^blog/\w+/(.+)$', blogview),
    (r'^blog$', blogview),
    (r'^service/(\w+)$', services_page),
    (r'^(aboutus)$', services_page),
    (r'^(newsnevents)$', services_page),
    (r'^info/(termsofservice)$', services_page),
    (r'^info/(privacy)$', services_page),
    (r'^contactus$', contactus),

    (r'^admin$', adminhome),
    (r'^admin/registrations$', registrations),
    (r'^admin/blogpost$', blogpost),
    (r'^admin/upload$', uploadmedia),
    (r'^admin/textedit$', texteditor),

    (r'^auth/login$', register),
    (r'^auth/check$', dologin),
    (r'^auth/logout$', make_logout),

    (r'^form/webinar$', webinar_reg),

    (r'^ac/post$', autocomplete_post),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)"""