from django.contrib import admin
from board1.models import Board
from board1.models import Comment

# Register your models here.
admin.site.register(Board)
admin.site.register(Comment)