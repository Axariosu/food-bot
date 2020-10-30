import random
import math

async def generate_random_time(minT, maxT):
    """
    Given 2 integers low and high: 
    Returns a float (2 decimal points) value between low and high.
    """
    return round(minT + random.random() * maxT, 2)