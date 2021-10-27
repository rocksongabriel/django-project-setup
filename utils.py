import random

def secret_key():
    characters = 'abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()[].,:;+*=_-~|'
    """function to generate a 50 character secret_key"""
    secret_key = ''
    for _ in range(50):
        secret_key = secret_key + random.choice(characters)
    return secret_key