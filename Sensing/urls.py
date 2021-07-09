from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('home', views.home, name='home'),
    path('register', views.register, name='register'),
    path('', views.data, name='data'),
    path('visualize', views.visualize, name='visualize')
]
