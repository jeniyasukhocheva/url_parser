from django.urls import path
from url_parser import views


app_name = 'url_parser'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]
