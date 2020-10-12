class Player(object):
    def __init__(self, name): 
        self.name = name
        self.lives = 3
        self.guessed = False
        self.score = 0

    def toggle_guessed(self):
        self.guessed = not self.guessed

    def reset_score(self):
        self.score = 0