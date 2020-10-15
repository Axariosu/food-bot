import random

def sample_from_list(l, n):
    """
    Given a list l and integer n:
    Returns a sample of size n from the list. 
    """
    return random.choices(l, k=n)