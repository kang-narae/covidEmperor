from datetime import datetime
from django.db import models

# Create your models here.
class Board(models.Model) :
    b_no = models.IntegerField(default=0, primary_key=True)
    b_title = models.CharField(max_length=100)
    b_content = models.TextField()
    b_date = models.DateTimeField(default=datetime.now(), blank=True)
    b_hit = models.IntegerField(default=1)
    b_img = models.ImageField(blank=True)

    def __str__(self):
        return self.b_title


class Comment(models.Model) :
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True)
    c_no = models.IntegerField(default=0, primary_key=True)
    c_content = models.TextField()
    c_date = models.DateTimeField(default=datetime.now(), blank=True)
    c_pw = models.CharField(max_length=10, blank=True)
    
    def __str__(self):
        return self.c_content