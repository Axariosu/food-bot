import json
import os
import random
f = open("wordlist_10000_.txt", "w+")
for line in open("wordlist_10000.txt", "r"):
    if line.strip().isalpha():
        f.write(line)

f.close()

# a = {"a": 1, "b": 2, "c": 3}
# b = a.copy()
# for k, v in list(a.items()):
#     if v == 1:
#         del a[k]
# print(a)
# print(b)

    

# print(random.sample([x for x in range(20)], k=25))

# print(os.path.abspath(os.path.join(os.path.dirname(__file__), '../food-bot/storage/tracking.json')))
# with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../food-bot/storage/tracking.json'))) as json_file:
#     data = json.load(json_file)

# print(data)

# print(", ".join([x for x in list({"Axarious": "Word"}.keys())]))


# ll = input().strip("[]").split(", ")
# print(ll)

# import random

# def myfunction():
#     return 0.1



# mylist = [("apple", "banana")]

# print("a" if "apple" in mylist else "b")

# print(mylist)