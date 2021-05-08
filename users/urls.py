from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('connexion/', views.login, name='login'),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/mes-organigrammes/', views.organigramme, name='organigramme'),
    path('dashboard/liste-des-membres/', views.listing_members, name='listing-members'),
    path('dashboard/liste-des-membres/<code_sbfmember>', views.listing_members, name='listing-members'),
    path('inscription/', views.signin_with_code, name='signin-code'),
    path('deconnexion/', views.logout, name='logout'),
    path('mes-gains/', views.gains, name='gifts'),
    path('example/', TemplateView.as_view(template_name='dashboard_layout.html'), name='example'),
]