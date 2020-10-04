import random

# http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.99.4112&rep=rep1&type=pdf
# https://stackoverflow.com/questions/4308610/how-to-ignore-certain-files-in-git
"""
This file is an interpretation of the 1970 "Mastermind." 
"""

def generateRandomCode(n):
    """
    Given an integer n: 
    Returns a numeric string of length n.
    """
    return "".join(random.choices("0123456789", k=n))

def calculateDistance(n, c):
    """
    Given string n and c:
    Returns a tuple (# of correct numbers, # correct numbers and correct places)
    based on how far away n is away from c.
    """
    code = dict()
    same, good = 0, 0
    checklater = []
    for i in range(len(n)):
        # Check if the two characters are the same, otherwise we add the index to check later. 
        if n[i] == c[i]:
            same += 1
        else:
            if c[i] in code: 
                code[c[i]] += 1
            else: 
                code[c[i]] = 1
            checklater.append(i)

    for num in checklater:
        if n[num] in code and code[n[num]] != 0:
            # if code[n[num]] != 0:
            good += 1
            code[n[num]] -= 1
    
    return same, good

# print(generateRandomCode(5))
# def optimalpath(same, good, guess, code, path):
#     if good == len(code):
#         return path
#     s, g = calculateDistance(guess, code)
#     print(same, good, guess, code, path)
#     pass



# print 
# print(calculateDistance("5123", "5123"))

    
