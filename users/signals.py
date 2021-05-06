from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SBFMember, Assignement, Codes
from .utils import get_code_parrain

@receiver(post_save, sender=SBFMember)
def create_codes(sender, instance, created, **kwargs):
    if created:
        code_parrain = get_code_parrain(instance.pk)
        Codes.objects.create(code_parrain=code_parrain, sbfmember=instance)
