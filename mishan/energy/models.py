from django.db import models

class News (models.Model):
    news = models.CharField (max_length = 100)
    date = models.DateTimeField ()
