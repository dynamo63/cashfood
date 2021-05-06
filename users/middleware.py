from .models import Assignement, SBFMember, Matrice

class AssignementMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        try:
            member = request.user.sbfmember
            num = member.get_num_all_aff()
            matrices = Matrice.objects.all().order_by('prerequisite')
            for matrice in matrices:
                if num >= matrice.prerequisite and Assignement.objects.filter(member=member, matrice=matrice).exists() is False:
                    Assignement.objects.create(member=member, matrice=matrice)
        except Exception:
            pass
        finally:
            response = self.get_response(request)

            # Code to be executed for each request/response after
            # the view is called.

            return response