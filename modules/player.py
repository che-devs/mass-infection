class Player:
    ATTEMPTS = 3

    def __init__(self, id) -> None:
        self.level = 0
        self.id = id
        self.score = 0
        self.attempts = self.ATTEMPTS
        self.game_over = False

    
    def get_level(self) -> int:
        return self.level
    
    def level_up(self):
        self.level += 1
        self.reset_attempts()
    
    def get_id(self) -> int:
        return self.id
    
    def get_score(self) -> int:
        return self.score
    
    def add_score(self, score) -> int:
        if score < 0:
            self.minus_one_attempt()
        self.score += score
        if self.score < 0:
            self.score = 0
        return self.score
    
    def reset_attempts(self):
        self.attempts = self.ATTEMPTS
    
    def minus_one_attempt(self):
        if self.attempts <= 1:
            self.game_over = True
        else:
            self.attempts -= 1
    
    def get_attempts(self):
        return self.attempts

    def get_gameover(self):
        return self.game_over