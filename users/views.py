from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.urls import reverse

from .models import CashFoodMember, User, Affilie
from .forms import CashFoodSignInForm

def login(request):
    """
        Connexion Utilisateur : login
            - code : le code de l'utilisateur
            - password: mot de passe utilisateur
    """
    if request.method == 'POST':
        code = request.POST['code']
        password = request.POST['password']
        cashmember = authenticate(code=code, password=password)
        if cashmember is not None:
            auth_login(request, cashmember.user, backend='users.backends.CashFoodBackend')
            return redirect('dashboard')
    return render(request, 'users/connexion.html')

@login_required
def dashboard(request):
    """
        Page d'accueil : home
    """
    cashmember = CashFoodMember.objects.get(user=request.user)
    affilies = cashmember.affilie_set.all()
    data = {
        'affilies': affilies
    }

    return render(request, 'users/home.html', data)

def home(request):
    return render(request, 'index.html')

def signin_with_code(request):
    """
        Page d'inscription avec un code : signin-code

    """
    form = CashFoodSignInForm()
    if request.method == 'POST':
        form = CashFoodSignInForm(request.POST)
        if form.is_valid():
            # Recuperation des donnees
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            code = form.cleaned_data['code']

            # Inscription du candidat
            current_cashfoodmember = CashFoodMember.objects.get(code=code)
            # Creation du compte utilisateur
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()
            if current_cashfoodmember.user is None:
                current_cashfoodmember.user = user
                current_cashfoodmember.save()
            else:
                CashFoodMember.objects.create(user=user, phone_number=phone_number)
                # Affiliation
                Affilie.objects.create(parent=current_cashfoodmember, username=username, code=code)
            return redirect('login')
    return render(request, 'users/inscription.html', { 'form': form })

def signin_with_link(request, code):
    """
        Page d'affiliation : affiliation
    """
    form = CashFoodSignInForm()
    if request.method == 'POST':
        form = CashFoodSignInForm(request.POST)
        if form.is_valid():
            # Recuperation des donnees
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            code = form.cleaned_data['code']

            # Inscription du candidat
            current_cashfoodmember = CashFoodMember.objects.get(code=code)
            # Creation du compte utilisateur
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()

            if current_cashfoodmember.user is not None:
                CashFoodMember.objects.create(user=user, phone_number=phone_number)
                # Affiliation
                Affilie.objects.create(parent=current_cashfoodmember, username=username, code=code)
                return redirect('login')
    return render(request, 'users/affiliate.html', { 'form': form, 'code': code })

@login_required
def create_link_affiliation(request):
    """ Cette vue permet d'affilier un utilisateur 
        - code : str
        Retourne un objet json contenant le lien de parainnage
    """
    uri = reverse('affiliation', args=[request.user.cashfoodmember.code], current_app='users')
    data = {
        'link': request.build_absolute_uri(uri)
    }
    return JsonResponse(data)

def logout(request):
    """
        Page de deconnexion utilisateur : logout
    """
    auth_logout(request)
    return redirect('login')