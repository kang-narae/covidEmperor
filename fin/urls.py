
from . import views
from django.urls import include, path


app_name = 'fin'


urlpatterns = [
    path('plot/', views.plot, name= 'plot'),    
]
