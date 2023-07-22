from django.urls import path
from .views import LoginView,SignUpView

urlpatterns = [
    path('login/',LoginView,name='login'),
    path('signUp/',SignUpView,name='signUp'),
]