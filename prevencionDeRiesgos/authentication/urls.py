from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import CustomLoginView
from django.urls import reverse_lazy
urlpatterns = [
    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/',CustomLoginView.as_view() ,name='login'),
    path('logout/', LogoutView.as_view(), name='logout' ),
]
