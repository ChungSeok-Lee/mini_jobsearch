from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('/?select_=1', views.makewordcloud, name='wordcloud'),
]