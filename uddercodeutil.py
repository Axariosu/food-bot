import random
import math
import time
import random
import queue

import string
digs = string.digits + string.ascii_letters

# https://stackoverflow.com/questions/4308610/how-to-ignore-certain-files-in-git
# http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.99.4112&rep=rep1&type=pdf
# https://pdfs.semanticscholar.org/5b57/f5d00776aa434894eafc06b11903ff02e28f.pdf
# https://stackoverflow.com/questions/3228865/how-do-i-format-a-number-with-a-variable-number-of-digits-in-python

"""
This is a helper file for an implementation of the 1970 game "Mastermind," also called "Bulls and Cows."
"""

code_length = 4
numeric = "0123456789"
smallNumeric = "012345"
target = "9999"
stack = queue.deque()

# solutionRank = {}
# count = 0
# for i in range(code_length+1):
#     for j in range(code_length+1): 
#         if (i + j) > code_length or (i == code_length-1 and j == 1): 
#             break
#         if (i, j) not in solutionRank: 
#             solutionRank.setdefault((i,j), count)
#         count += 1

class TPOANode: 
    def __init__(self, code):
        self.code = code
        self.parent = None
        self.child = []
        self.depth = 0
        self.rank = 0

def TPOA(k, d, b, c, t, solutionList, path):
    """
    Given branching factor k, exploration depth d, selected b elements,
    code c, target t, solutionList, and a stack path:
    Performs a guided DFS to find a solution node. 
    Modifies the stack and appends/pops the path taken from the root until it
    reaches a solution. 
    """
    same, good = calculateDistance(c.code, t)
    # tuples are immutable, so they take less space than lists.
    path.append((c, same, good))
    l = c.depth
    # c.rank = solutionRank[(same, good)]

    # Check if the code is a complete solution
    if (same, good) == (len(c.code), 0):
        return True
    # TPOA+ (exploration)
    if l < d: 
        b = k
    else:
    # TPOA* (exploitation)
        if math.floor(k * l / d) < k:
            b = math.floor((k * l) / d)
        else:
            b = 1

    # possibleSet is a dictionary containing the n hashing-collision groups.
    # We rearrange them based on the value length, for a higher possibility
    # to get a solution through a guided dfs. (optional)
    possibleSet = hashw(calculatePartition(len(c.code), same, good, c.code, solutionList))
    
    sortedPossibleSet = {}
    for x in sorted(possibleSet, key = lambda x: len(possibleSet[x]), reverse=True):
        sortedPossibleSet[x] = possibleSet[x]

    # If we've reached a leaf node (where there are no more continuations of the node),
    # pop everything from the stack until we reach the parent node. 
    if len(possibleSet) == 0:
        # a = stack.pop()
        # path.append(a)
        # if a[0].parent != None:
            # a = path.pop()
        for i in range(c.depth):
            path.pop()
    nextChoices = {}

    for key, value in sortedPossibleSet.items():
        # choose first b items, it will be representative of the HCG. 
        # describes commented code, but implementation does not work. 
        nextChoices.setdefault(value[0], value)
        # j = 0
        # for i in range(b):
        #     nextChoices.setdefault(value[j], value)
        #     if j % 5 == 0:
        #         j += 1
    # Keep an integer held for the next depth level
    nextDepth = c.depth + 1
    # For our new choices, initialize our node and recursively apply TPOA on the next node. 
    for choice, value in nextChoices.items(): 
        newChoice = TPOANode(choice)
        c.child.append(newChoice)
        newChoice.parent = c
        newChoice.depth = nextDepth
        if TPOA(k, d, b, newChoice, t, value, path):
            return True
    return False


"""
This file is an interpretation of the 1970 "Mastermind." 
"""

def generateRandomCode(n):
    """
    Given an integer n: 
    Returns a numeric string of length n.
    """
    return "".join(random.choices(numeric, k=n))

def calculateDistance(n, c):
    """
    Given string n and c:
    Returns a tuple (# of correct numbers, # correct numbers and correct places)
    based on how far away n is away from c.
    """
    code = {}
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

def calculatePartition(n, s, g, h, v):
    """
    Given integers n, s, g, string h, and list v:
    Returns a list of still valid combinations given same s and good g 
    with string length n with guess h with valid possibilities v. 
    """
    h = h.zfill(n)
    res = []

    for k in v:
        same, good = calculateDistance(str(k).zfill(n), h)
        if (s, g) == (same, good):
            res.append(str(k).zfill(n))
    return res
    
def hashe(d):
    """
    Given a dictionary d whose d.values() are lists:
    Returns the count of non-empty lists. (unused method)
    """
    s = [len(x) for x in d.values()]
    return sum([1 for x in s if x != 0])
    
def hashw(l):
    """
    Given a list of numbers l:
    Returns a dictionary of which hashing-collision group (HCG) it belongs to.
    """
    res = {}
    for num in l:
        sortedv = prehash(num)
        if sortedv not in res:
            res[sortedv] = [num]
        else: 
            res[sortedv].append(num)
    return res

def prehash(s):
    """
    Given a string s:
    Returns a tuple of unique elements separated by count. 
    For example, a string of format AABC or ABBC will return (2, 1, 1), 
    AAAB and ABBB will return (3, 1), ABCD will return (1, 1, 1, 1).
    """
    res = {}
    for c in s: 
        if c not in res:
            res[c] = 1
        else: 
            res[c] += 1
    return tuple(sorted(res.values()))[::-1]

def int2base(x, base):
    """
    Given an integer x and a base: 
    Returns x in the given base. 
    """
    if x < 0:
        sign = -1
    elif x == 0:
        return digs[0]
    else:
        sign = 1
    x *= sign
    digits = []
    while x:
        digits.append(digs[int(x % base)])
        x = int(x / base)
    if sign < 0:
        digits.append('-')
    digits.reverse()
    return ''.join(digits)

def reverseStack(s):
    """
    Given a stack, reverses the order. 
    """
    items = []
    while s:
        items.append(s.pop())
    for item in items:
        s.append(item)

# start = time.time()
# a = TPOANode("0123")
# TPOA(10, 2, 1, a, target, [str(x).zfill(len(a.code)) for x in range(len(numeric)**len(a.code))], stack)
# while stack:
#     print(stack.pop()[0].code)
# stop = time.time()
# print(stop - start)