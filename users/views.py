from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import (SBFMember, 
                    User, Codes, 
                    listing_affilies, 
                    listing_all_affs,
                    Assignement,
                    Matrice,
                    Gain)
from .forms import SBFSignInForm, SBFLoginForm
from .utils import get_code_parrain, get_level, convert_queryset_in_dict


def login(request):
    """
        Connexion Utilisateur : login
            - code : le code de l'utilisateur
            - password: mot de passe utilisateur
    """
    form = SBFLoginForm()
    if request.method == 'POST':
        form = SBFLoginForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            password = form.cleaned_data['password']
            user = authenticate(code=code, password=password)
            if user is not None:
                auth_login(request, user, backend='users.backends.SBFBackend')
                return redirect('dashboard')
    return render(request, 'users/connexion.html', { 'form': form })

@login_required
def dashboard(request):
    """
        Page d'accueil : home
    """
    matrices = Matrice.objects.all()

    # Get Matrice
    matrices = convert_queryset_in_dict(matrices)
    for m in matrices:
        m['gains'] = []

    # Get Gain Matrice
    for matrice in matrices:
        gains = convert_queryset_in_dict(Gain.objects.filter(matrice__pk=matrice['id']))
        matrice['gains'] += gains

        # Verification
        matrice['status'] = Assignement.objects.filter(member=request.user.sbfmember, matrice__pk=matrice['id']).exists()


    context = {
        'matrices': matrices
    }

    return render(request, 'users/dashboard.html', context=context)

@login_required
def organigramme(request):
    sbfmember = SBFMember.objects.get(user=request.user)
    affilies = listing_affilies(sbfmember=sbfmember)
    for aff in affilies:
        aff.team = listing_affilies(sbfmember=aff)
    num_aff = len(listing_all_affs(sbfmember))
    data = {
        'affilies': affilies,
        'num_aff': num_aff
    }
    return render(request, 'users/organigramme.html', data)

@login_required
def listing_members(request, code_sbfmember=None):
    """
       Listing of members of users 
    """
    if code_sbfmember is None:
        sbfmember = request.user.sbfmember
    else:
        sbfmember = SBFMember.objects.filter(codes__code_parrain=code_sbfmember)[0]
    data = {
        'members': listing_all_affs(sbfmember)
    }
    return render(request, 'users/liste_membres.html', context=data)

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
            if keys_parent.count() != 0:
                parent = keys_parent.first()
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
    messages.info(request, "Voulez-vous vous reconnecter ?")
    return redirect('login')