from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('select=1', views.show, name='show'),
]