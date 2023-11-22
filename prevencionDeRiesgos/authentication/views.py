from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

from .forms import CustomUserCreationForm

class Signup(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"



class CustomLoginView(LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)

        # Personaliza la redirección después del inicio de sesión
        if self.request.user.is_authenticated:
            return redirect("home")  # Cambia "home" al nombre de tu URL de inicio

        return response