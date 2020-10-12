import time, random, re
import numpy as np

f = open("words_lower_alpha.txt", "r")

wordlist = set([word[:-1] for word in f])

def generate_random_word():
    res = random.sample(wordlist, k=1)[0]
    return res if 3 <= len(res) <= 20 else generate_random_word()

def generate_random_word_reversed():
    res = random.sample(wordlist, k=1)[0]
    return res[::-1] if 3 <= len(res) <= 20 else generate_random_word_reversed()

def generate_random_word_scrambled():
    res = list(random.sample(wordlist, k=1)[0])
    original_word = "".join(res)
    random.shuffle(res)
    return ("".join(res), original_word) if 5 <= len(res) <= 12 else generate_random_word_scrambled()

def benchmark():
    start = time.time()
    print(generate_random_word_scrambled())
    stop = time.time()
    print(stop-start)    

benchmark()

# i can't keep bot online since i run it locally 
# leaderboards and storage are an issue
# still run locally just with nohup on linux? -> still free but computer boom
# aws (free for 1 y) 
# no hang up = nohup. 
# E5-2630L V2 aliexpress 
# 6C/12T CPU with low TDP, 2.4 GHz base clock $80-100 ()
# low power xeon 