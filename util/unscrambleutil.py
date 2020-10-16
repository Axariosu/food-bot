import random

f = open("wordlist_10000.txt", "r")
f_2 = open("words_lower_alpha.txt", "r")

wordlist = set([word[:-1] for word in f])
hard_wordlist = set([word[:-1] for word in f_2])

def generate_random_word_scrambled(mode, minL, maxL):
    """
    Given three integers mode, minL, maxL:
    Mode determines the difficulty of the wordlist. 
    Returns a tuple of (scrambled_word, target) at random 
    with at least minL characters and at most maxL characters.
    """
    if mode == 0: 
        wl = wordlist
    elif mode == 1:
        wl = hard_wordlist
    res = list(random.sample(wl, k=1)[0])
    original_word = "".join(res)
    random.shuffle(res)
    return (insert_zero_width_space("".join(res)), original_word) if minL <= len(res) <= maxL else generate_random_word_scrambled(mode, minL, maxL)

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