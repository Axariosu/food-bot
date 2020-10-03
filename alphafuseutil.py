import time, random, re
import numpy as np

f = open("words_lower.txt", "r")

# word[:-1] to get rid of \n character
wordlist = [word[:-1] for word in f]

# letter frequency of alphaletters in this specific wordlist
letter_frequency = [0.08458060175046897,
0.018870222161450043,
0.04197147712997857,
0.03526743096890421,
0.10983719731598748,
0.012519759590782241,
0.0243180797464511,
0.027399735687058266,
0.08641504682335299,
0.0017957718676833115,
0.008946861865065964,
0.05737814544946437,
0.029181925893391324,
0.07148741981352609,
0.07085483667131436,
0.031015450175675335,
0.0018636801744345713,
0.0704308126000065,
0.0704545229579569,
0.06473779451775089,
0.03625106552737246,
0.009874097999283165,
0.008463676997707002,
0.0028482355235028346,
0.01916717712995555,
0.0040689736614754795]

"""
[0].append previous total + current, created with 
cumulative_letter_frequency = np.zeros(26)
for i in range(len(letter_frequency)):
    cumulative_letter_frequency[i] += cumulative_letter_frequency[i-1] + letter_frequency[i]
for i in range(len(cumulative_letter_frequency)):
    print(cumulative_letter_frequency[i], ",")
print(cumulative_letter_frequency)
"""
cumulative_letter_frequency = [0,
0.08458060175046897,
0.10345082391191901,
0.14542230104189757,
0.1806897320108018,
0.29052692932678925,
0.30304668891757147,
0.3273647686640226,
0.35476450435108087,
0.44117955117443386,
0.4429753230421172,
0.45192218490718317,
0.5093003303566476,
0.5384822562500389,
0.609969676063565,
0.6808245127348793,
0.7118399629105546,
0.7137036430849892,
0.7841344556849957,
0.8545889786429526,
0.9193267731607034,
0.9555778386880759,
0.9654519366873591,
0.9739156136850661,
0.976763849208569,
0.9959310263385245,
1.0]

def check_valid(first, second):
    """
    Given two strings first and second:
    Returns true if second is in the wordlist, len(second) >= 3 
    and all characters in first are found in second. 
    """
    if second not in wordlist or len(second) < 3: 
        return False

    # initial check passed
    fst = {}
    snd = {}
    for x in first: 
        if x not in fst:
            fst.setdefault(x, 1)
        else: 
            fst[x] += 1
    for x in second: 
        if x not in snd:
            snd.setdefault(x, 1)
        else: 
            snd[x] += 1
    
    # return True if fst and snd == fst else False
    for key in fst: 
        # print(snd[key], fst[key])
        if key not in snd: 
            return False
        if fst[key] > snd[key]:
            return False
    return True

    # n^2 solution
    # print(fst, snd)
    # for c in fst: 
    #     for i in range(len(snd) - count):
    #         print(c, snd[i], i, count)
    #         if c == snd[i]: 
    #             print(fst, snd)
    #             count += 1
    #             snd[i], snd[len(snd) - count] = snd[len(snd) - count], snd[i]
    #             break

    # return True if count >= len(fst) else False

def check_valid_combinations(first, second):
    """
    Given two lists first and second:
    Returns true if all characters in first are found in second. 
    """
    fst = {}
    snd = {}
    for x in first: 
        if x not in fst:
            fst.setdefault(x, 1)
        else: 
            fst[x] += 1
    for x in second: 
        if x not in snd:
            snd.setdefault(x, 1)
        else: 
            snd[x] += 1
    
    # return True if fst and snd == fst else False
    for key in fst: 
        # print(snd[key], fst[key])
        if key not in snd: 
            return False
        if fst[key] > snd[key]:
            return False
    return True

def generate_random_string_of_length_biased(n):
    """
    Given an integer n: 
    Returns a list of random n letters, biased from cumulative_letter_frequency. 
    Guarantees combinations >= 1.
    """ 
    res = []
    for i in range(n):
        res.append(chr(int(ord('a') + binary_search(cumulative_letter_frequency, 0, len(cumulative_letter_frequency), random.random()))))
    if combinations(res) == 0:
        print(res)
        return generate_random_string_of_length_biased(n)
    return res

def generate_random_string_of_length_unbiased(n):
    """
    Given an integer n: 
    Returns a list of random n letters. 
    Guarantees combinations >= 1.
    """ 
    res = []
    for i in range(n):
        res.append(chr(int(ord('a') + 26 * random.random())))
    if combinations(res) == 0:
        print(res)
        return generate_random_string_of_length_unbiased(n)
    return res

def binary_search(l, start, end, target): 
    """
    Given a list l, int start, int end, and int target:
    Returns a position p in the array which p < target < q. 
    In this case, target is not in l, so we don't check l[p] or l[q] == target.
    """
    p, q = start, end
    # print(p, q, l[int((p + q) / 2)], target)
    if p + 1 == q: 
        return p
    if target <= l[int((p + q) / 2)]:
        return binary_search(l, p, int((p + q) / 2), target)
    else: 
        return binary_search(l, int((p + q) / 2), q, target)

def combinations(l): 
    """
    Given a string or list l: 
    Returns count of valid possibilities in the wordlist containing minimally those letters. 
    """
    count = 0
    for word in wordlist:
        # print(l, word, check_valid_combinations(l, word))
        count += 1 if check_valid_combinations(l, word) else 0
    return count

def get_random_possibility(l):
    """
    Given a string or list l:
    Returns a random valid possibility.
    """
    combinations = []
    for word in wordlist:
        if check_valid_combinations(l, word):
            combinations.append(word)
    return random.choice(combinations) if combinations is not [] else None

def get_first_possibility(l):
    """
    Given a string or list l:
    Returns first valid possibility (runs much faster than get_random_possibility(), takes no space)
    """
    combinations = []
    for word in wordlist:
        if check_valid_combinations(l, word):
            return word

def get_many_possibilities(l):
    """
    Given a string or list l:
    Returns up to 200 valid possibilities.
    """
    combinations = []
    for word in wordlist:
        if check_valid_combinations(l, word):
            combinations.append(word)
        # if len(combinations) > 500:
        #     break
    if len(combinations) > 25:
        return random.choices(combinations, 25) if combinations is not [] else None
    else:
        return combinations if combinations is not [] else None

def in_wordlist(l):
    """
    Given a string or list l: 
    Returns true if the word is in the wordlist, else return false. 
    """
    return True if l in wordlist else False

def benchmark_unbiased():
    """
    Returns a tuple which shows running time of the functions.
    """
    start = time.time()
    string = generate_random_string_of_length_unbiased(7)
    stop = time.time()
    return (string, combinations(string), get_first_possibility(string), stop - start)
    # print(string, combinations(string), get_first_possibility(string))
    # print(stop - start)

# def setup(bot):
#     bot.add_cog(alphafuseutil(bot))

# benchmark()



# print(generate_random(1000))

# print(binary_search(cumulative_letter_frequency, 0, len(cumulative_letter_frequency), 0))







# a = dict()
# for char in "abcdefghijklmnopqrstuvwxyz": 
#     a.setdefault(char, 0)

# for char in generate_random(100000): 
#     a[char] += 1

# print(a)

# print([100 * x for x in letter_frequency])





# total = 0
# for word in wordlist: 
#     for ch in word: 
#         if ch.isalpha():
#             a[ch] += 1
#             total += 1
# print(a, total)

# for k, v in a.items(): 
#     print(v / total, ",")
        
# 1, 2, 3

# ...

# "X" 

# print(generate_random(15))
# print(check_valid("benzo", "benzofuroquinoxaline"))




# start = time.time()
# print(len([x for x in f]))
# 
# stop = time.time()
# 
# print(stop - start)