from django.urls import path
from .views import mostrar

urlpatterns = [
    path('', mostrar)
]