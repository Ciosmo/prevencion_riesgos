from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.mostrar, name='home'),
    path('grafico/', views.grafico, name='grafico')
]