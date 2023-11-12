from django.urls import path
from . import views

urlpatterns = [
    path('', views.mostrar, name='home'),
    path('home/', views.mostrar, name='home'),
    path('grafico/', views.grafico, name='grafico')
]