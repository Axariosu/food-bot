import json
import os
import random
import aiohttp
import asyncio
from PIL import Image

import queue    # For Python 2.x use 'import Queue as queue'
import threading, time, random

def func(id, result_queue):
    print("Thread", id)
    time.sleep(random.random() * 5)
    result_queue.put((id, 'done'))

def main():
    q = queue.Queue()
    threads = [ threading.Thread(target=func, args=(i, q)) for i in range(5) ]
    for th in threads:
        th.daemon = True
        th.start()

    result1 = q.get()
    result2 = q.get()

    print("Second result: {}".format(result2))

if __name__=='__main__':
    main()


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