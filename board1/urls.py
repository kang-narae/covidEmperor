from django.urls import path
from . import views

app_name = 'board1'
urlpatterns = [
    path('bList/', views.bList, name='bList'),
]