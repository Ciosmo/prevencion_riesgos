from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('grafico/', views.grafico, name='grafico'),
    path('registrar_accidente/', views.registrar_accidente, name='registrar_accidente'),
    path('datosform/', views.datosform, name='datosform'),
    path('accidente/<int:accidente_id>/', views.accidente_detail, name='accidente_detail'),
]