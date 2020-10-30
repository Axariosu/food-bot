import random
import requests

trivia = open("trivia-questions.txt", "r")
trivialist = set([x[:-1] for x in trivia])

# https://github.com/luozhouyang/python-string-similarity#levenshtein

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
    if s1 == s2:
        return 0.0
    if len(s1) == 0:
        return len(s2)
    if len(s2) == 0:
        return len(s1)

    v0 = [0] * (len(s2) + 1)
    v1 = [0] * (len(s2) + 1)

    for i in range(len(v0)):
        v0[i] = i

    for i in range(len(s1)):
        v1[0] = i + 1
        for j in range(len(s2)):
            cost = 1
            if s1[i] == s2[j]:
                cost = 0
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
        v0, v1 = v1, v0

    return v0[len(s2)]

def valid_guess(s1, s2, similarity):
    """
    Given strings s1, s2 and integer similarity:
    Returns True if the similarity between s1 and s2 >= similarity, else False.
    """
    # Add a possible error for: 
    # Every 8 characters
    # Every non-alphanumeric character
    max_errors = 0
    for k in s2: 
        if not k.isalnum(): 
            max_errors += 1
    sim = (len(s2) - lehvenstein_distance(s1, s2) + max_errors) / len(s2) * 100
    return sim >= similarity

