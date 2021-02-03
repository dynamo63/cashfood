from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import CashFoodMember, User, Affilie
from .forms import CashFoodSignInForm

def login(request):
    if request.method == 'POST':
        code = request.POST['code']
        password = request.POST['password']
        cashmember = authenticate(code=code, password=password)
        if cashmember is not None:
            auth_login(request, cashmember.user)
        return redirect('home')
    return render(request, 'users/login.html')

@login_required
def home(request):
    cashmember = CashFoodMember.objects.get(user=request.user)
    affilies = cashmember.affilie_set.all()
    print(affilies)

    data = {
        'affilies': affilies
    }

    return render(request, 'users/home.html', data)

def signin_with_code(request):
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
    return render(request, 'users/sign_in2.html', { 'form': form })

def logout(request):
    auth_logout(request)
    return redirect('login')