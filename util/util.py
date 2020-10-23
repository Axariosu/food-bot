import random

def generate_random_color():
    """
    Returns a value between 0 and 16777215, the max value for int(rgb).
    """
    return random.randint(0, 256**3-1)

def italics(s):
    """
    Given a string s:
    Returns a italicized string.
    """
    return "*" + str(s) + "*"

def bold(s):
    """
    Given a string s:
    Returns a bolded string.
    """
    return "**" + str(s) + "**"

def underline(s):
    """
    Given a string s:
    Returns an underlined string.
    """
    return "__" + str(s) + "__"

def strikethrough(s):
    """
    Given a string s:
    Returns an strikethrough string.
    """
    return "~~" + str(s) + "~~"

def codeblock(s):
    """
    Given a string s:
    Returns an codeblocked string.
    """
    return "```" + str(s) + "```"

def insert_zero_width_space(word):
    """
    Given a word: 
    Returns a zero-width-space inserted word.
    """
    return '\u200b'.join([(x if x != "_" else ("\\" + x)) for x in word])