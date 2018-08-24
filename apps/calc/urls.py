from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('initializedb', views.initializedb),
    path('champ_id_names', views.champion_id_names)
]