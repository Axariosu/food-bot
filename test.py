import json
import os
import random
import aiohttp
import asyncio
from PIL import Image
import queue    # For Python 2.x use 'import Queue as queue'
import threading, time, random
import requests
import math


# f = open("wordlist_league.txt2", "w+")
# for word in open("wordlist_league.txt", "r"):
#     for k in word.split(", "):
        
#         f.write("".join([x.lower() for x in k if (x.isalpha() or x.isspace())]) + "\n")
# f.close()

# names=["Arnesh Dawar","Moses Maldonado","Sean Li","Crystal Yu","Kevin Cui","Stanley Wu","Cameron Farhan","Triniti Chan","Christopher Quinto","Karan Sharma","Hana Burton"]

# a = random.sample(names,k=len(names))

# for i in range(len(names)):
#     print(names[i] + " -> " + a[i])

# print([names[i] + " -> " + random.sample(names, k=len(names))[i] for i in range(len(names))])

# query = "koko"
# url = "https://www.google.com/search?q=" + str(query) + "&source=lnms&tbm=isch"

# HEADERS = {"content-type": "image/png"}

# html = requests.get(url, headers=HEADERS).text

# soup = BeautifulSoup(html, "html.parser")

# for img in soup.find_all("img"):
#     print(img["src"])





# def func(id, result_queue):
#     print("Thread", id)
#     time.sleep(random.random() * 5)
#     result_queue.put((id, 'done'))

# def main():
#     q = queue.Queue()
#     threads = [ threading.Thread(target=func, args=(i, q)) for i in range(5) ]
#     for th in threads:
#         th.daemon = True
#         th.start()

#     result1 = q.get()
#     result2 = q.get()

#     print("Second result: {}".format(result2))

# if __name__=='__main__':
#     main()


# async def fetch(client):
#     async with client.get('http://python.org') as resp:
#         assert resp.status == 200
#         return await resp.text()

# async def main():
#     async with aiohttp.ClientSession() as client:
#         html = await fetch(client)
#         print(html)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())

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

def mystery(s, l, r): 
    if l == r:
        pass
        # print(s)
    else: 
        for i in range(r-l): 
            s[i], s[l] = s[l], s[i]
            mystery(s, l + 1, r)
            s[i], s[l] = s[l], s[i]

def main(m):
    s = list(m)
    mystery(s, 0, len(s) - 1)
    return


if __name__ == "__main__":
    k = "abcdefghijkl"
    for i in range(len(k)):
        start = time.time()
        main(k[0:i])
        stop = time.time()
        print(k[0:i], stop-start)
