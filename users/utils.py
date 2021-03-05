import random
from string import ascii_uppercase, digits

def get_random_code():
    letters = ascii_uppercase + digits
    return ''.join(random.choice(letters) for _ in range(8))

def get_code_parrain(id_parent):
    numbers = ''.join(random.choice(digits) for _ in range(4))
    return f"SBF{id_parent}_{numbers}"