from django.contrib.auth.backends import ModelBackend
from .models import CashFoodMember, User

class CashFoodBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        code_user = kwargs['code']
        password = kwargs['password']

        try:
            cashmember = CashFoodMember.objects.get(code=code_user)
            if cashmember.user.check_password(password) is True:
                return cashmember
        except CashFoodMember.DoesNotExist:
            pass

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None