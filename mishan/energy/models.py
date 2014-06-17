from django.db import models
import datetime

class News (models.Model):
    news = models.CharField (max_length = 100)
    date = models.DateTimeField ()


class UploadFile (models.Model):
    filename = models.CharField (max_length = 1024)
    description = models.CharField (max_length = 2048)
    filetype = models.CharField (max_length = 32)
    date = models.DateTimeField (default = datetime.datetime.now)
