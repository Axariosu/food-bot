import time, random, re

f = open("words_lower_alpha.txt", "r")

wordlist = set([word[:-1] for word in f])

def generate_random_word(minL, maxL):
    """
    Given two integers minL, maxL:
    Returns a tuple of (word, target) at random 
    with at least minL characters and at most maxL characters.
    """
    res = random.sample(wordlist, k=1)[0]
    return (insert_zero_width_space(res), res) if minL <= len(res) <= maxL else generate_random_word(minL, maxL)

def generate_random_word_alphabetized(minL, maxL):
    """
    Given two integers minL, maxL:
    Returns a tuple of (alphabetised_word, target) at random 
    with at least minL characters and at most maxL characters.
    """
    res = random.sample(wordlist, k=1)[0]
    original_word = "".join(res)
    res = sorted(res)
    return (insert_zero_width_space(original_word), "".join(res)) if minL <= len(res) <= maxL else generate_random_word_alphabetized(minL, maxL)

def generate_random_word_alphabetized_reversed(minL, maxL):
    """
    Given two integers minL, maxL:
    Returns a tuple of (reversed_alphabetised_word, target) at random 
    with at least minL characters and at most maxL characters.
    """
    res = random.sample(wordlist, k=1)[0]
    original_word = "".join(res)
    res = sorted(res)
    return (insert_zero_width_space(original_word), "".join(res)[::-1]) if minL <= len(res) <= maxL else generate_random_word_alphabetized_reversed(minL, maxL)

def generate_random_word_scrambled(minL, maxL):
    """
    Given two integers minL, maxL:
    Returns a tuple of (scrambled_word, target) at random 
    with at least minL characters and at most maxL characters.
    """
    res = list(random.sample(wordlist, k=1)[0])
    original_word = "".join(res)
    random.shuffle(res)
    return (insert_zero_width_space("".join(res)), original_word) if minL <= len(res) <= maxL else generate_random_word_scrambled(minL, maxL)

def scramble(s):
    """
    Given a string s: 
    Returns the same string but with shuffled characters.
    """
    k = list(s)
    random.shuffle(k)
    return "".join(k)

def insert_zero_width_space(word):
    return '\u200b'.join([x for x in word])

# print(generate_random_word_alphabetized(5, 20))

# print(insert_zero_width_space("teste"))
# def benchmark():
#     start = time.time()
#     print(generate_random_word_scrambled())
#     stop = time.time()
#     print(stop-start)    

# benchmark()

# i can't keep bot online since i run it locally 
# leaderboards and storage are an issue
# still run locally just with nohup on linux? -> still free but computer boom
# aws (free for 1 y) 
# no hang up = nohup. 
# E5-2630L V2 aliexpress 
# 6C/12T CPU with low TDP, 2.4 GHz base clock $80-100 ()
# low power xeon 