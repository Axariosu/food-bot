import random
import requests

trivia = open("trivia-questions.txt", "r")
trivialist = set([x[:-1] for x in trivia])

def fetch_questions_jservice(): 
    """
    Returns a list of length 50 of a dictionary which contains: 
    http://jservice.io/ documentation
    """
    return requests.get("http://jservice.io/api/random?count=50").json()


def fetch_question():
    """
    Returns a tuple (question, answer) from the trivia list. 
    """
    k = random.sample(trivialist, k=1)[0]
    filtered = k.strip("\"[]").split("\", \"")
    return filtered[0], filtered[1].lower()

def lehvenstein_distance(s1, s2):
    """
    Given strings s1, s2: 
    Returns the lehvenstein distance.
    """
    m, n = len(s1), len(s2)
    count = 0 
    i = 0
    j = 0
    while i < m and j < n: 
        if s1[i] != s2[j]: 
            if m > n: 
                i += 1
            elif m < n: 
                j += 1
            else:
                i += 1
                j += 1
            count += 1
        else:
            i += 1
            j += 1
    while i < m:
        i += 1
        count += 1
    while j < n: 
        j += 1
        count += 1
    return count

def valid_guess(s1, s2):
    """
    Given strings s1, s2:
    Returns True if the errors of s1 is an acceptable response for s2, else False.
    """
    # Add a possible error for: 
    # Every 8 characters
    # Every non-alphanumeric character
    max_errors = len(s2) // 5
    for k in s2: 
        if not k.isalnum(): 
            max_errors += 1
    return lehvenstein_distance(s1, s2) <= max_errors

