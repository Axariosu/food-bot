from dotenv import load_dotenv
import os
import aiohttp
import asyncio
import json
import random

load_dotenv()

TENOR_API_KEY = os.getenv("TENOR_API_KEY")

async def get_random_gif(q, limit, contentfilter, media_filter):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.tenor.com/v1/random?key=%s&q=%s&limit=%s&contentfilter=%s&media_filter=%s' % (TENOR_API_KEY, q, limit, contentfilter, media_filter)) as resp:
            k = json.loads(await resp.text())['results']
            try:
                gif = random.choice(k)
            except IndexError:
                return "No results found! :zany_face:"
            return gif['url']

# async def get_top_gif(q, limit, contentfilter, media_filter):
#     async with aiohttp.ClientSession() as session:
#         async with session.get('https://api.tenor.com/v1/random?key=%s&q=%s&limit=%s&contentfilter=%s&media_filter=%s' % (TENOR_API_KEY, q, limit, contentfilter, media_filter)) as resp:
#             k = json.loads(await resp.text())
#             return k['results'][0]['url']
