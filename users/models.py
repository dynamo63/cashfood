from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from .utils import get_random_code

class CashFoodMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, unique=False)
    phone_number = PhoneNumberField(null=False, blank=True, unique=True, verbose_name="Numero de Telephone")
    rugby_level = models.PositiveSmallIntegerField(
                        default=0,
                        verbose_name="Niveau"
                    )
    code = models.CharField(
                        default= get_random_code,
                        unique=True,
                        max_length=8
                    )
    is_member = models.BooleanField(default=False)

    objects = models.Manager()

    class Meta:
        verbose_name = "Membre SBF"
        verbose_name_plural = "Membres SBF"

    def __str__(self):
        if self.user is not None:
            return f"{self.user.username}"
        return f"{self.code} - Number Phone: {self.phone_number}"

class Affilie(models.Model):
    parent = models.ForeignKey(CashFoodMember, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    code = models.CharField(max_length=8)

    objects = models.Manager()

    class Meta:
        verbose_name = "Affilie"
        verbose_name_plural = "Affilies"

    def clean(self):
        """
            Verifier la validite du modele
        """
        # ETAPE 1: Si le parent a entre 0 et 4 affilies 
        if (0 < self.parent.affilie_set.count() < 4) is False:
            raise ValidationError('Ce membre a deja atteint son quota d\'affilie', code='invalid')
        

    def __str__(self):
        return f"{self.username} - Code: {self.code} - Parent Code: {self.parent.code}"