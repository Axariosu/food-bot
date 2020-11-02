import json
import os
import random
import aiohttp

async def fetch():
    async with aiohttp.request('GET',
            'http://python.org/') as resp:
        assert resp.status == 200
        print(await resp.text())

# f = open("retrivia.txt", "w+")
# for line in open("trivia-questions.txt", "r"):
#     a = line.split("\"")
#     if len(a) > 6: 
#         print(line)
#     # print(k)
    

# f.close()
# sampleAnswer="<i> (test) The best answer </i>"




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