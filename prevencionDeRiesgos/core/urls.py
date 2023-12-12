from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('info/', views.info, name='info'),
    path('grafico/', login_required(views.grafico), name='grafico'),
    path('registrar_accidente/', login_required(views.registrar_accidente), name='registrar_accidente'),
    path('datosform/', login_required(views.datosform), name='datosform'),
    path('accidente/<int:accidente_id>/', login_required(views.accidente_detail), name='accidente_detail'),
]