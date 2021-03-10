from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse_lazy
from .models import SBFMember, Codes

class SBFTest(TestCase):

    def setUp(self):
        """
            Creation des data de Test
        """
        self.sbf_member = SBFMember.objects.create()
        self.client = Client()
        user = User(username='dynamo63', email='dynamo63@yopmail.com')
        user.set_password('test2000')
        user.save()
        self.user_dynamo63 = User.objects.get(username='dynamo63')
        SBFMember.objects.create(user=self.user_dynamo63)

    def test_create_code(self):
        """
            Teste la creation du code parrain lors de l'ajout d'un membre
        """
        codes = Codes.objects.first()
        self.assertEqual(self.sbf_member, codes.sbfmember)

    def test_signin_success(self):
        """
            Teste l'inscription d'un membre SBF
        """
        code = self.sbf_member.code
        data = {
            'username': 'demo',
            'password': 'test2000',
            'confirm_password': 'test2000',
            'email': 'demo@yopmail.com',
            'phone_number': '+24166192844',
            'code': code
        }
        url = reverse_lazy('signin-code')
        response = self.client.post(url, data=data, secure=True)

        # Verification de l'inscription (redirection vers la page de connexion)
        self.assertRedirects(response, '/connexion/', 302, msg_prefix="Inscription Reussi")

        # Verification de la creation du compte
        sbf_user_demo_is_created = User.objects.filter(username=data.get('username')).exists()
        self.assertTrue(sbf_user_demo_is_created)

    def test_signin_failure(self):
        """
            Test un cas echeant de l'inscription
        """

        data_user = {
            'username': 'Steve',
            'password': 'demo2000',
            'confirm_password': 'demo200',
            'email': 'steve@yopmail',
            'phone_number': '+24166192855',
            'code': '1234'
        }
        url = reverse_lazy('signin-code')
        response = self.client.post(url, data=data_user, secure=True)

        self.assertFormError(response, 'form', 'code', 'Ce code n\'existe pas')
        self.assertFormError(response, 'form', 'email', 'Saisissez une adresse de courriel valide.')
        self.assertFormError(response, 'form', 'confirm_password', 'Les mots de passe ne sont pas identiques')

    def test_login_success(self):
        """
            Teste la connexion a son dashboard
        """
        data_login = {
            'code': self.user_dynamo63.sbfmember.code,
            'password': 'test2000'
        }

        is_login = self.client.login(**data_login, backend='users.backends.SBFBackend')
        self.assertTrue(is_login)

        user = User.objects.get(username='dynamo63')
        self.assertIsNotNone(user.last_login)
