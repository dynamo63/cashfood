from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.urls import reverse
from .models import SBFMember, User, Codes, listing_affilies
from .forms import SBFSignInForm
from .utils import get_code_parrain


def login(request):
    """
        Connexion Utilisateur : login
            - code : le code de l'utilisateur
            - password: mot de passe utilisateur
    """
    if request.method == 'POST':
        code = request.POST['code']
        password = request.POST['password']
        sbfmember = authenticate(code=code, password=password)
        if sbfmember is not None:
            auth_login(request, sbfmember.user, backend='users.backends.SBFBackend')
            return redirect('dashboard')
    return render(request, 'users/connexion.html')

@login_required
def dashboard(request):
    """
        Page d'accueil : home
    """
    sbfmember = SBFMember.objects.get(user=request.user)
    affilies = listing_affilies(sbfmember=sbfmember)
    code = Codes.objects.get(sbfmember=sbfmember)
    for aff in affilies:
        aff.team = listing_affilies(sbfmember=aff)
    data = {
        'affilies': affilies,
        'code': code
    }

    return render(request, 'users/dashboard.html', data)

def home(request):
    return render(request, 'index.html')

@transaction.atomic
def signin_with_code(request):
    """
        Page d'inscription avec un code : signin-code
    """
    form = SBFSignInForm()
    if request.method == 'POST':
        form = SBFSignInForm(request.POST)
        if form.is_valid():
            # Recuperation des donnees
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            code = form.cleaned_data['code']
            code_parrain = form.cleaned_data['code_parrain']

            #  ================== INSCRIPTION DU CANDIDAT ===================
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()

            # Creation du membre SBF
            sbfmember = SBFMember.objects.get(code=code)
            sbfmember.user = user
            sbfmember.phone_number = phone_number

            keys_parent = Codes.objects.filter(code_parrain=code_parrain)
            if keys_parent is not None:
                parent = keys_parent.first()
                print(parent)
                sbfmember.parent = parent.sbfmember
            sbfmember.save()
            messages.success(request, "Inscription Reussi, rentrez vos informations pour vous connecter")
            return redirect('login')
    return render(request, 'users/inscription.html', { 'form': form })

@login_required
def logout(request):
    """
        Page de deconnexion utilisateur : logout
    """
    auth_logout(request)
    return redirect('login')