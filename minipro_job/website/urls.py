from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('/?select=<int:select>', views.makewordcloud, name='wordcloud'),
    path('update', views.update, name='update_home'),
]