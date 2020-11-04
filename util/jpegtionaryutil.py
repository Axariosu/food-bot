import aiohttp
import asyncio
import io
import os, sys
import math
import time
import random
import requests
from bs4 import BeautifulSoup
import urllib
# import cookielib
import json
import re

from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont, ImageOps
from google_images_search import GoogleImagesSearch
from pexels_api import API

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PROJECT_CX_KEY = os.getenv("PROJECT_CX_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

gis = GoogleImagesSearch(GOOGLE_API_KEY, PROJECT_CX_KEY)
api = API(PEXELS_API_KEY)

# https://stackoverflow.com/questions/64215836/python-requests-scrape-image-returns-src-in-format-dataimage

# ====== POSSIBLE SEARCH PARAMETERS ======
# _search_params = {
#     'q': '...',
#     'num': 10,
#     'safe': 'high|medium|off',
#     'fileType': 'jpg|gif|png',
#     'imgType': 'clipart|face|lineart|news|photo',
#     'imgSize': 'huge|icon|large|medium|small|xlarge|xxlarge',
#     'imgDominantColor': 'black|blue|brown|gray|green|pink|purple|teal|white|yellow',
#     'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived'
# }

f = open("wordlist_10000.txt")
wordlist = set([x.strip() for x in f])

frequency = [1,
0.963685034393,
0.915514439871,
0.855651813287,
0.786739117086,
0.711649593506,
0.633291209438,
0.554424618597,
0.477510961618,
0.404600092133,
0.33726432237,
0.276577354646,
0.223133423003,
0.177098315259,
0.138282118453,
0.106223207516,
0.0802739420852,
0.0596803776859,
0.0436506110419,
0.0314087667764,
0]

def binary_search(l, start, end, target): 
    """
    Given a list l, int start, int end, and int target:
    Returns a position p in the array which p < target < q. 
    In this case, target is not in l, so we don't check l[p] or l[q] == target.
    """
    p, q = start, end
    if p + 1 == q: 
        return p
    if target <= l[int((p + q) / 2)]:
        return binary_search(l, p, int((p + q) / 2), target)
    else: 
        return binary_search(l, int((p + q) / 2), q, target)

def generate_unpixellating_pictures(query, n):
    """
    Given string query, integers n, duration:
    Returns a list of unpixellating pictures, from idx 0 to ... (8)
    """
    mosaic = generate_google_images_scrape_mosaic(query, n)
    pictures = []
    pixellation_count = round(math.log2(mosaic.width))
    for i in range(pixellation_count + 1):
        pictures.append(construct_pixel_average(mosaic, i))
    return pictures

def generate_unpixellating_gif(query, n, duration):
    """
    Given string query, integers n, duration:
    Returns a gif which unpixellates after duration seconds. 
    """
    mosaic = generate_google_images_scrape_mosaic(query, n)
    frames = []
    pixellation_count = round(math.log2(mosaic.width))
    for i in range(pixellation_count):
        fobj = io.BytesIO()
        construct_pixel_average(mosaic, i).save(fobj, 'GIF')
        frame = Image.open(fobj)
        for i in range(duration * 300):
            frames.append(frame)
    animated_gif = io.BytesIO()
    frames[0].save(animated_gif, 
        format="GIF", 
        save_all=True, 
        append_images=frames[1:], 
        delay=1000,
        loop=0)
    ani = Image.open(animated_gif)
    # animated_gif.seek(0)
    # open(f'{query}.gif', 'wb+').write(animated_gif.read())
    return ani

def get_center_square_of_image(image):
    """
    Given a PIL Image image:
    Returns the center square of the image. 
    Thanks to PIL's ImageOps. 
    """
    w, h = image.size
    if w == h:
        return image
    if w > h:
        return ImageOps.fit(image, (h, h), method=3, bleed=0.0, centering=(0.5, 0.5))
    else:
        return ImageOps.fit(image, (w, w), method=3, bleed=0.0, centering=(0.5, 0.5))

def get_soup(url,header):
    return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url, headers=header)), 'html.parser')

# def generate_google_images_scrape_mosaic_normalized_gaussian(query, n):
#     """
#     Given a query and integer n: 
#     Returns a mosaic with n pictures of query n. 
#     1 <= n <= 20
#     """
#     res = Image.new(mode='RGB', size=(256, 256))
#     max_pictures_per_side = math.ceil(math.sqrt(n)) # max number of pictures on a side
#     new_size = round(res.width // max_pictures_per_side)
#     picture_id = 0
#     q = "+".join(query.split())
#     headers = {"content-type": "image/png"}
#     search_url="https://www.google.com/search?q="+q+"&safe=off&source=lnms&tbm=isch"
#     html = requests.get(search_url, headers=headers).text
#     soup = BeautifulSoup(html, "html.parser")
#     my_bytes_io = io.BytesIO()
#     link_list = []
#     for img in soup.find_all("img")[1:21]:
#         link_list.append(img["src"])
#     for i in range(n):
#         link = link_list[binary_search(frequency, 0, len(frequency), random.random()) - 1]
#         response = requests.get(link)
#         img = Image.open(io.BytesIO(response.content))
#         temp_img = img
#         temp_img = get_center_square_of_image(temp_img)
#         temp_img = temp_img.resize((new_size, new_size))
#         row, col = round(picture_id // max_pictures_per_side), round(picture_id % max_pictures_per_side)
#         res.paste(temp_img, (col * new_size, row * new_size))
#         picture_id += 1
#     return res

# def generate_google_images_scrape_mosaic_first(query, n):
#     """
#     Given a query and integer n: 
#     Returns a mosaic with n pictures of query n. 
#     1 <= n <= 20
#     """
#     res = Image.new(mode='RGB', size=(256, 256))
#     max_pictures_per_side = math.ceil(math.sqrt(n)) # max number of pictures on a side
#     new_size = round(res.width // max_pictures_per_side)
#     picture_id = 0
#     q = "+".join(query.split())
#     headers = {"content-type": "image/png"}
#     search_url="https://www.google.com/search?q="+q+"&safe=off&source=lnms&tbm=isch"
#     html = requests.get(search_url, headers=headers).text
#     soup = BeautifulSoup(html, "html.parser")
#     my_bytes_io = io.BytesIO()
#     link_list = []
#     for img in soup.find_all("img")[1:21]:
#         link_list.append(img["src"])
#     for link in random.sample(link_list, k=n):
#         response = requests.get(link)
#         img = Image.open(io.BytesIO(response.content))
#         temp_img = img
#         temp_img = get_center_square_of_image(temp_img)
#         temp_img = temp_img.resize((new_size, new_size))
#         row, col = round(picture_id // max_pictures_per_side), round(picture_id % max_pictures_per_side)
#         res.paste(temp_img, (col * new_size, row * new_size))
#         picture_id += 1
#     return res

def generate_google_images_scrape_mosaic(query, n):
    """
    Given a query and integer n: 
    Returns a mosaic with n pictures of query n. 
    1 <= n <= 20
    """
    res = Image.new(mode='RGB', size=(256, 256))
    max_pictures_per_side = math.ceil(math.sqrt(n)) # max number of pictures on a side
    new_size = round(res.width // max_pictures_per_side)
    picture_id = 0
    q = "+".join(query.split())
    headers = {"content-type": "image/png"}
    search_url="https://www.google.com/search?q="+q+"&safe=off&source=lnms&tbm=isch"
    html = requests.get(search_url, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")
    my_bytes_io = io.BytesIO()
    link_list = []
    for img in soup.find_all("img")[1:21]:
        link_list.append(img["src"])
    for link in random.sample(link_list, k=n):
        response = requests.get(link)
        img = Image.open(io.BytesIO(response.content))
        temp_img = img
        temp_img = get_center_square_of_image(temp_img)
        temp_img = temp_img.resize((new_size, new_size))
        row, col = round(picture_id // max_pictures_per_side), round(picture_id % max_pictures_per_side)
        res.paste(temp_img, (col * new_size, row * new_size))
        picture_id += 1
    return res

def generate_pexels_mosaic(query, n):
    res = Image.new(mode='RGB', size=(1024, 1024))
    api.search(query, page=1, results_per_page=n)
    max_pictures_per_side = math.ceil(math.sqrt(n)) # max number of pictures on a side
    new_size = round(res.width // max_pictures_per_side)
    picture_id = 0
    photos = api.get_entries()
    my_bytes_io = io.BytesIO()
    for photo in photos:
        response = requests.get(photo.original)
        img = Image.open(io.BytesIO(response.content))
        temp_img = img
        temp_img = get_center_square_of_image(temp_img)
        temp_img = temp_img.resize((new_size, new_size))
        row, col = round(picture_id // max_pictures_per_side), round(picture_id % max_pictures_per_side)
        res.paste(temp_img, (col * new_size, row * new_size))
        picture_id += 1
    return res

def generate_mosaic(query, n):
    """
    Given a string query, integer n: 
    Returns a mosaic size 1024 x 1024 with n pictures of the top google searches.
    """
    res = Image.new(mode='RGB', size=(512, 512))
    _search_params = {'q': query, 'num': n, 'filetype': 'png', 'rights': 'cc_publicdomain'}
    gis.search(search_params=_search_params)
    max_pictures_per_side = math.ceil(math.sqrt(n)) # max number of pictures on a side
    new_size = round(res.width // max_pictures_per_side)
    picture_id = 0
    my_bytes_io = io.BytesIO()
    for image in gis.results():
        my_bytes_io.seek(0)
        raw_image_data = image.get_raw_data()
        image.copy_to(my_bytes_io, raw_image_data)
        my_bytes_io.seek(0)
        temp_img = Image.open(my_bytes_io)
        temp_img = get_center_square_of_image(temp_img)
        temp_img = temp_img.resize((new_size, new_size))
        row, col = round(picture_id // max_pictures_per_side), round(picture_id % max_pictures_per_side)
        res.paste(temp_img, (col * new_size, row * new_size))
        picture_id += 1
    return res

def construct_pixel_average(image, blur):
    """
    Given a PIL.Image image and integer blur:
    Returns an image with image.size // 2 ** blur pixels taken
    by getting the average pixels of that square region. 
    NOTE: Takes about 2 seconds to run for size 1024x1024. 
    """
    averages_of_x_y = {}
    max_blur = round(math.log2(image.width)) # gets the total size of blur, generally will be 10
    pixel_count = round(2 ** blur) # the amount of pixels per side, up to blur=10.
    pixel_range = image.width // pixel_count # For example: 1024 / (2 ** 3) = 1028 / 8 = 128 pixels per side. Ends up being a 8 x 8 grid of 128 pixels.
    # 1m operations on 1024x1024 picture
    px = image.load()
    r_sum, g_sum, b_sum, count = 0, 0, 0, 0
    # print(pixel_count, pixel_range)
    res = Image.new(mode=image.mode, size=image.size)
    # ImageStat.Stat could also work for median here. 
    for row in range(pixel_count): 
        for col in range(pixel_count):
            for i in range(pixel_range):
                for j in range(pixel_range):
                    x, y = row * pixel_range + i, col * pixel_range + j
                    r_sum += px[x, y][0]
                    g_sum += px[x, y][1]
                    b_sum += px[x, y][2]
                    count += 1
            avg_r, avg_g, avg_b = r_sum // count, g_sum // count, b_sum // count
            # print(row, col, row * pixel_range, col * pixel_range, avg_r, avg_g, avg_b)
            to_paste = Image.new(mode=image.mode, size=(pixel_range, pixel_range), color=(avg_r, avg_g, avg_b))
            res.paste(to_paste, (row * pixel_range, col * pixel_range))
            r_sum, g_sum, b_sum, count = 0, 0, 0, 0
    return res

def generate_list_of_words(n):
    """
    Given an integer n: 
    Returns a wordlist of size n. 
    """
    return random.sample(wordlist, k=n)

def generate_hangman(word):
    """
    Given a string word: 
    Returns a space separated broken-underscore of len(word). 
    """
    "/".join(word.split(" "))
    return "\xa0".join(["\_\xa0" for c in word])

def benchmark(query, n, duration):
    """
    Gif making runs in ~1.5s average!
    """
    start = time.time()
    gif = generate_unpixellating_gif(query, n, duration)
    stop = time.time()
    print(stop-start)


# pic.show()
# stop = time.time()
# print(stop-start)
# start = time.time()
# for i in range(11):
    # construct_pixel_average(pic, i).show()
# stop = time.time()

# k = generate_pexels_mosaic('managers', 4)
# k.show()
# start = time.time()
# construct_pixel_average(k, 6).show()
# stop = time.time()
# print(stop-start)

# print(generate_hangman("test"))

# my_bytes_io = io.BytesIO()

# gis.search(search_params=_search_params)

# for image in gis.results():
#     # here we tell the BytesIO object to go back to address 0
#     my_bytes_io.seek(0)
#     # take raw image data
#     raw_image_data = image.get_raw_data()
#     # this function writes the raw image data to the object
#     image.copy_to(my_bytes_io, raw_image_data)
#     # or without the raw data which will be automatically taken
#     # inside the copy_to() method
#     image.copy_to(my_bytes_io)
#     # we go back to address 0 again so PIL can read it from start to finish
#     my_bytes_io.seek(0)
#     # create a temporary image object
#     temp_img = Image.open(my_bytes_io)
#     # show it in the default system photo viewer
#     print(temp_img, type(temp_img))
#     # temp_img.show()

# for image in gis.results():
#     # image.download('C://Users/jeffrey/Downloads/1 School/ASU/0 Projects/_tempdirectory')
#     my_bytes_io.seek(0)
#     raw_image_data = image.get_raw_data()
#     image.copy_to(my_bytes_io, raw_image_data)

# async def main():
#     async with aiohttp.ClientSession() as session:
#         async with session.get('https://pbs.twimg.com/media/Elyir1oVgAYKtRG?format=jpg&name=4096x4096') as resp:
#             q = await resp.read()
#             image_file = io.BytesIO(q)
#             print(type(image_file))
#             picture = Image.open(image_file)
#             dim = picture.size
#             print(dim)
#             # picture.save("Compressed_","JPEG",optimize=True,quality=0) 

#             # im.show()
#             # print(resp.status)
#             # print(await resp.json())


# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
