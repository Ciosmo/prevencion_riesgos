from django.shortcuts import render

# Create your views here.
def mostrar(request):
    return render(request, 'home.html')