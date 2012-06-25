from django.db import models
import datetime
from django.contrib.auth.models import User

class WebinarRegistration (models.Model):
    name = models.CharField ( max_length = 512 )
    city = models.CharField ( max_length = 64 )
    email = models.CharField ( max_length = 512 )
    mobile = models.CharField ( max_length = 20 )
    timestamp = models.DateTimeField ( default = datetime.datetime.now )


class Blog (models.Model):
    title = models.CharField ( max_length = 500 )
    tags = models.CharField ( max_length = 200 )
    catagory = models.CharField ( max_length = 50 )
    post = models.TextField ()
    author = models.ForeignKey (User)
    timestamp = models.DateTimeField ( default = datetime.datetime.now )
    seoid = models.CharField ( max_length = 100 )

