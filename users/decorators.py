from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout
from django.contrib import messages
from .models import SBFMember


# def sbfmember_only(view_func):
#     def wrapper(request, *args,**kwargs):
#         if SBFMember.objects.filter(user=request.user).exists():
#             return view_func(request, *args, **kwargs)
#         else:
#             logout(request)
#             return view_func(request, *args, **kwargs)
#         return wrapper

def sbfmember_only(user):
    try:
        user.sbfmember
    except AttributeError:
        raise PermissionDenied('Error')
    else:
        return True