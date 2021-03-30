import random
from django.conf import settings
from string import ascii_uppercase, digits

def get_random_code():
    letters = ascii_uppercase + digits
    return ''.join(random.choice(letters) for _ in range(8))

def get_code_parrain(id_parent):
    numbers = ''.join(random.choice(digits) for _ in range(4))
    return f"SBF{id_parent}_{numbers}"

def get_level(num_aff):
    if num_aff == settings.DEMARREUR:
        return "Demarreur"
    elif num_aff == settings.RUGBY_1:
        return "Rugby 1"
    else:
        return "Pas encore defini"