from django.db import models
from datetime import datetime


class Fboard(models.Model):
    b_no = models.IntegerField(default=0,primary_key=True)
    b_title = models.CharField(max_length=1000)
    b_content = models.TextField()
    b_date = models.DateTimeField(default=datetime.now(),blank=True)
    b_hit = models.IntegerField(default=1)
    
    def __str__(self):
        return self.b_title
    
    