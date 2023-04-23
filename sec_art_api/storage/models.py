from django.db import models

class Storage(models.Model):
    name = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    class Mete:
        ordering = ['created']