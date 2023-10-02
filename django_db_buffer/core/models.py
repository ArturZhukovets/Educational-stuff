from django.db import models

# Create your models here.


class TextLog(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    message = models.CharField()
