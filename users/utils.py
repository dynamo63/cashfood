import random
from string import ascii_uppercase, digits

def get_random_code():
    letters = ascii_uppercase + digits
    return ''.join(random.choice(letters) for _ in range(8))