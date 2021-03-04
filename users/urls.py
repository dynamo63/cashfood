from django.urls import path
from . import views

urlpatterns = [
    path('connexion/', views.login, name='login'),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('inscription/', views.signin_with_code, name='signin-code'),
    path('deconnexion/', views.logout, name='logout'),
    # path('create-link/', views.create_link_affiliation, name='create-link'),
    # path('affiliation/<code>', views.signin_with_link, name='affiliation')
]