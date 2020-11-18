import re
import random
regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
osu_mplink = re.compile(
        r'^(?:http)s?://osu.ppy.sh/community/matches/([0-9]{8}$|[0-9]{9}$)'
)


# helpful links
# https://www.w3schools.com/python/python_regex.asp

# checks if the mplink provided is a valid osu!mp link
def valid_mplink(mplink):
    if re.match(osu_mplink, mplink) is not None:
        return True
    return False

def generate_random_color(self):
    """
    Returns a value between 0 and 16777215, the max value for int(rgb).
    """
    return random.randint(0, 256**3-1)

# if __name__ == "__main__":
#     print(valid_mplink('https://osu.ppy.sh/community/matches/56872668'))
#     pass