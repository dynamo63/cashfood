from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from .utils import get_random_code
from itertools import chain

def listing_affilies(sbfmember):
    affilies = SBFMember.objects.filter(parent=sbfmember)
    return affilies

def listing_all_affs(sbfmember):
    liste = list(SBFMember.objects.filter(parent=sbfmember))
    while len(liste) > 1:
        for aff in liste:
            liste += list(listing_all_affs(aff))
        break
    return liste

def get_num_affilies(sbfmember):
    return SBFMember.objects.filter(parent=sbfmember).count()


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

    def profile(self):
        code = Codes.objects.get(sbfmember=self)
        return f"{code.code_parrain} {self.user.username} {self.phone_number}"

    def is_active(self):
        return Assignement.objects.filter(member=self).exists()
    
    def get_num_all_aff(self):
        return len(listing_all_affs(self))

    def get_level(self):
        is_active = Assignement.objects.filter(member=self).exists()
        if is_active:
            ass = Assignement.objects.filter(member=self).last()
            return ass.matrice.name
        else:
            return None

    def __str__(self):
        if self.user is not None:
            return f"{self.user.username}"
        return f"{self.code}"

class Matrice(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nom du Niveau")
    prerequisite = models.IntegerField(verbose_name='Nombre D\'affilie a avoir', unique=True)

    def __str__(self):
        return self.name

class Gain(models.Model):
    image = models.ImageField(upload_to='pics/', default='food.png')
    title = models.CharField(max_length=255, verbose_name="designation")
    description = models.TextField()
    matrice = models.ForeignKey(Matrice, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Assignement(models.Model):
    member = models.ForeignKey(SBFMember, on_delete=models.CASCADE)
    matrice = models.ForeignKey(Matrice, on_delete=models.CASCADE)
    received = models.BooleanField(default=False, verbose_name='A recu son gain')
    date_of_receipt = models.DateField(verbose_name='Date de Reception',null=True, blank=False)

    # for pylint
    objects = models.Manager()

    def status(self):
        return self.date_of_receipt == None

    def __str__(self):
        return f"{self.member} has unlocked {self.matrice}"

class Codes(models.Model):
    code_parrain = models.CharField(verbose_name="Code Parrain", max_length=20, unique=True)
    sbfmember = models.OneToOneField(SBFMember, on_delete=models.CASCADE, verbose_name="Utilisateur")

    objects = models.Manager()

    class Meta:
        verbose_name = "Code Parrain"
        verbose_name_plural = "Codes Parrains"

    def __str__(self):
        return f"Code Parrain: {self.code_parrain}"