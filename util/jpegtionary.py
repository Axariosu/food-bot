import aiohttp
import asyncio
import io
import os, sys
import math
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont, ImageOps
from google_images_search import GoogleImagesSearch

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PROJECT_CX_KEY = os.getenv("PROJECT_CX_KEY")
gis = GoogleImagesSearch(GOOGLE_API_KEY, PROJECT_CX_KEY)

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

def get_mosaic(query, n):
    """
    Given a string query, integer n: 
    Returns a mosaic size 1024 x 1024 with n pictures of the top google searches.
    """
    res = Image.new(mode='RGB', size=(1024, 1024))
    _search_params = {'q': query, 'num': n, 'filetype': 'jpg'}
    gis.search(search_params=_search_params)

    max_pictures_per_side = math.ceil(math.sqrt(n)) # max number of pictures on a side

    new_size = round(res.width // max_pictures_per_side)
    picture_id = 0
    my_bytes_io = io.BytesIO()
    for image in gis.results():
        my_bytes_io.seek(0)
        raw_image_data = image.get_raw_data()
        image.copy_to(my_bytes_io, raw_image_data)
        image.copy_to(my_bytes_io)
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
    """
    averages_of_x_y = {}
    max_blur = round(math.log2(image.width)) # gets the total size of blur, generally will be 10
    pixel_count = round(2 ** blur) # the amount of divisions needed, up to 10. 
    pixel_range = image.width // pixel_count # 1024 / (2 ** 10) = 1 pixel, for example. 
    # 1m operations on 1024x1024 picture
    px = image.load()
    r_sum, g_sum, b_sum, count = 0, 0, 0, 0
    # print(pixel_count, pixel_range)
    res = Image.new(mode=image.mode, size=image.size)
    # ImageStat.Stat could also work for median here. 
    for row in range(pixel_range): 
        for col in range(pixel_range):
            for i in range(pixel_count):
                for j in range(pixel_count):
                    x, y = row * pixel_count + i, col * pixel_count + j
                    r_sum += px[x, y][0]
                    g_sum += px[x, y][1]
                    b_sum += px[x, y][2]
                    count += 1
            avg_r, avg_g, avg_b = r_sum // count, g_sum // count, b_sum // count
            # print(avg_r, avg_g, avg_b, row * pixel_range, col * pixel_range)
            to_paste = Image.new(mode=image.mode, size=(pixel_range, pixel_range), color=(avg_r, avg_g, avg_b))
            res.paste(to_paste, (row * pixel_range, col * pixel_range))
            r_sum, g_sum, b_sum, count = 0, 0, 0, 0
    return res



k = get_mosaic('ahri', 4)
k.show()
construct_pixel_average(k, 5).show()


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
