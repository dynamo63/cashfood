from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import csrf_exempt

from .models import CashFoodMember

@csrf_exempt
def login(request):
    if request.method == 'POST':
        code = request.POST['code']
        password = request.POST['password']
        print(code)
        cashmember = CashFoodMember.objects.get(code=code)
        print(cashmember)
        # user = authenticate(code=code, password=password)
        # print(user)
        # if user is not None:
        #     auth_login(request, user)
    return HttpResponse('hello')
