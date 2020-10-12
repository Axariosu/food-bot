
import time, random, re
import numpy as np

f = open("words_lower_alpha.txt", "r")

wordlist = set([word[:-1] for word in f])
# sets, checking member is O(log n)
# lists, checking member is O(n)

# https://stackabuse.com/levenshtein-distance-and-text-similarity-in-python/
# https://www.geeksforgeeks.org/check-if-two-given-strings-are-at-edit-distance-one/

def levenshtein_1(s1, s2):
    """
    Given string s1, s2: 
    Returns False is s2 is not in the wordlist. 
    Returns True if their levenshtein distance is 1, else False. 
    """
    # if s2 not in wordlist:
        # return False
    m = len(s1)
    n = len(s2) 

    if abs(m - n) > 1: 
        return False 
    if n < 3:
        return False
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
            if count == 1: 
                return False 
  
            # If length of one string is 
            # more, then only possible edit 
            # is to remove a character 
            if m > n: 
                i+=1
            elif m < n: 
                j+=1
            else:    # If lengths of both strings is same 
                i+=1
                j+=1
  
            # Increment count of edits 
            count+=1
  
        else:    # if current characters match 
            i+=1
            j+=1
  
    # if last character is extra in any string 
    if i < m or j < n: 
        count+=1
    # interesting. 
    return count == 1 and s2 in wordlist

def levenshtein_neighbors(s):
    """
    Given a string s: 
    Returns the count of neighboring words inside the wordlist with 
    levenshtein distance 1. 
    """
    count = 0
    for word in wordlist:
        count += 1 if levenshtein_1(s, word) else 0
    return count

def get_levenshtein_neighbors_possibility(s):
    """
    Given a string s: 
    Returns at most 25 neighboring words inside the wordlist with 
    levenshtein distance 1. 
    """
    res = []
    for word in wordlist:
        if levenshtein_1(s, word):
            res.append(word)
    if len(res) > 25:
        return random.sample(res, k=25) if res != [] else []
    else:
        return res

def generate_random_start():
    """
    Returns a random word in the wordlist such that it has at least 1 neighbor. 
    """
    a = random.sample(wordlist, k=1)[0]
    return a if (3 <= len(a) <= 6 and levenshtein_neighbors(a) > 0) else generate_random_start()

def benchmark():

    start = time.time()
    # print(levenshtein_neighbors("tenderloins"))
    a = generate_random_start()
    print(a, levenshtein_neighbors(a))
    stop = time.time()

    return(stop-start)

print(benchmark())
