from engine.engine import Engine
import chess
class Ai:
    def __init__(self, color):
        self.engine = Engine()
        self.color = color

    def get_best_move(self, board):
        return self.engine.get_best_move(board)
    
    def get_eval(self, board):
        score = self.engine.get_eval(board)
        return score
    
    def __del__(self):
        self.engine.quit()