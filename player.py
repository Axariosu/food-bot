class Player(object):
    def __init__(self, name): 
        self.name = name
        self.lives = 3
        self.guessed = False

    def toggle_guessed(self):
        self.guessed = not self.guessed