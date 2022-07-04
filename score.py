import time

class Score:

    def __init__(self):
        self.score=0
        self.wickets=0
        self.game_over=False
        self.batsman_state="Bat"
   
    def add_score(self,runs):
        self.score=self.score+runs
        return self.score
   
    def sub_score(self,runs):
        self.score=self.score-runs
        if self.score<0:
            self.score=0
        return self.score    

    def reset_score(self):
        self.score=0
        return self.score

    def add_wickets(self):
        self.wickets=self.wickets+1
        return self.wickets

    def reset_wickets(self):
        self.wickets=0
        return self.wickets

    def set_game_over(self):
        self.game_over=True
        return self.game_over

    def reset_game_over(self):
        self.game_over=False
        self.reset_wickets()
        return self.game_over
    
    def is_game_over(self):
        if self.wickets>=5:
            self.set_game_over()
        return self.game_over

    def set_batsman_state(self):
        self.batsman_state="Out"
        return self.batsman_state
    
    def reset_batsman_state(self):
        time.sleep(3)
        self.batsman_state="Bat"
        return self.batsman_state

    