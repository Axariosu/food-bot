import json, requests

l = requests.get("http://jservice.io/api/random?count=50").json()
# print(l[0]["question"], l[0]["answer"])
print(len(l), type(l))
