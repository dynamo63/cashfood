from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('', views.home, name='home'),
    path('signin/', views.signin_with_code, name='signin-code'),
    path('logout/', views.logout, name='logout')
]