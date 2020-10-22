import random

trivia = open("trivia-questions.txt", "r")
trivialist = set([x[:-1] for x in trivia])

def fetch_question():
    """
    Returns a tuple (question, answer) from the trivia list. 
    """
    k = random.sample(trivialist, k=1)[0]
    filtered = tuple(k.strip("\"[]").split("\", \""))
    return filtered[0], filtered[1].lower()

def lehvenstein_distance(s1, s2):
    """
    Given strings s1, s2: 
    Returns the lehvenstein distance.
    """
    m = len(s1)
    n = len(s2) 

    # check for 
    # 1) insertion
    # 2) deletion
    # 3) changing one char

    count = 0    # Count of isEditDistanceOne 
  
    i = 0
    j = 0
    while i < m and j < n: 
        # If current characters dont match 
        if s1[i] != s2[j]: 
            # If length of one string is 
            # more, then only possible edit 
            # is to remove a character 
            if m > n: 
                i += 1
            elif m < n: 
                j += 1
            else:    # If lengths of both strings is same 
                i += 1
                j += 1
            # Increment count of edits 
            count += 1
        else:    # if current characters match 
            i += 1
            j += 1
    # if last character is extra in any string 
    while i < m:
        i += 1
        count += 1
    while j < n: 
        j += 1
        count += 1
    # if i < m or j < n: 
    #     count += 1
    return count

def valid_guess(s1, s2):
    """
    Given strings s1, s2:
    Returns True if the errors of s1 is an acceptable response for s2, else False.
    """
    # Add a possible error for: 
    # Every 8 characters
    # Every non-alphanumeric character
    max_errors = len(s2) // 8
    for k in s2: 
        if not k.isalnum(): 
            max_errors += 1
    return lehvenstein_distance(s1, s2) <= max_errors

print(valid_guess("test", "test"))

