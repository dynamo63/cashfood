from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('connexion/', views.login, name='login'),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('inscription/', views.signin_with_code, name='signin-code'),
    path('deconnexion/', views.logout, name='logout'),
    path('example/', TemplateView.as_view(template_name='tree.html'), name='example')
]