from . import views
from django.urls import include, path


app_name = 'fin'


urlpatterns = [
    path('chart/', views.chart, name= 'chart' ),
    path('plot/', views.plot, name= 'plot' ),
    path('chart_data/', views.chart_data, name= 'chart_data' ),
    path('code_data/', views.code_data, name= 'code_data' ),
]