from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signin/', views.signin_with_code, name='signin-code'),
    path('logout/', views.logout, name='logout'),
    path('create-link/', views.create_link_affiliation, name='create-link'),
    path('affiliation/<code>', views.signin_with_link, name='affiliation')
]