from django.contrib.auth.backends import ModelBackend
from .models import SBFMember, User

class SBFBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        code_user = kwargs['code']
        password = kwargs['password']

        try:
            sbfmember = SBFMember.objects.get(code=code_user)
            if sbfmember.user.check_password(password) is True:
                return sbfmember.user
        except SBFMember.DoesNotExist:
            pass

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None