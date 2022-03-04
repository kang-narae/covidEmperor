from django.shortcuts import render
from board1.models import Board

# Create your views here.
def bList(req):

    bList = Board.objects.all().order_by('-b_no')
    context = {'bList':bList}

    return render(req, 'bList.html', context)