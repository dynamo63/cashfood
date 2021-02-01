from django.db import models
from django.contrib.auth.models import User

# Utilitaires
from phonenumber_field.modelfields import PhoneNumberField
from .utils import get_random_code

class CashFoodMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField()
    rugby_level = models.PositiveSmallIntegerField(
                        default=0
                    )
    code = models.CharField(
                        default= get_random_code(),
                        unique=True,
                        max_length=8
                    )
    is_member = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return f"{self.user.username} - Member"

class Affilie(models.Model):
    parent = models.ForeignKey(CashFoodMember, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    code = models.CharField(max_length=8)

    def __str__(self):
        return f"{self.username} - Code: {self.code} - Parent: {self.parent.user.username}"