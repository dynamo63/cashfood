from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from .utils import get_random_code

def listing_affilies(sbfmember):
    affilies = SBFMember.objects.filter(parent=sbfmember)
    return affilies

def get_num_affilies(sbfmember):
    return SBFMember.objects.filter(parent=sbfmember).count()

def get_total_aff(sbfmember):
    """
        Retourne le nombre total des affiflies (avec descendance)
        d'un membre SBF
    """
    num_aff = 0
    aff = listing_affilies(sbfmember)
    num_aff += aff.count() if aff.count() == 4 else 0
    # On verifie si il est demarreur
    if num_aff == 4:
        # On verifie si il est rugby 1
        total_affs = sum([get_num_affilies(m) for m in aff])
        num_aff += total_affs if total_affs == 16 else 0
    if num_aff == 20:
        pass
    return num_aff



class SBFMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, unique=False)
    phone_number = PhoneNumberField(null=True, 
                            blank=True, 
                            verbose_name="Numero de Telephone"
                        )
    rugby_level = models.PositiveSmallIntegerField(
                        default=0,
                        verbose_name="Niveau"
                    )
    code = models.CharField(
                        default= get_random_code,
                        unique=True,
                        max_length=8
                    )
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        verbose_name = "Membre SBF"
        verbose_name_plural = "Membres SBF"

    def __str__(self):
        if self.user is not None:
            return f"{self.user.username}"
        return f"{self.code}"

class Codes(models.Model):
    code_parrain = models.CharField(verbose_name="Code Parrain", max_length=20, unique=True)
    sbfmember = models.OneToOneField(SBFMember, on_delete=models.CASCADE, verbose_name="Utilisateur")

    objects = models.Manager()

    class Meta:
        verbose_name = "Code Parrain"
        verbose_name_plural = "Codes Parrains"

    def __str__(self):
        return f"Code Parrain: {self.code_parrain}"