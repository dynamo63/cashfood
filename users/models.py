from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from .utils import get_random_code

class SBFMember(models.Model):
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
    is_eligible = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        verbose_name = "Membre SBF"
        verbose_name_plural = "Membres SBF"

    def __str__(self):
        if self.user is not None:
            return f"{self.user.username}"
        return f"{self.code} - Number Phone: {self.phone_number}"

class Codes(models.Model):
    code_parrain = models.CharField(verbose_name="Code Parrain", max_length=20, unique=True)
    sbfmember = models.OneToOneField(SBFMember, on_delete=models.CASCADE)

    objects = models.Manager()

    class Meta:
        verbose_name = "Code Parrain"
        verbose_name_plural = "Codes Parrains"

    def __str__(self):
        return f"{self.sbfmember} - {self.code}"