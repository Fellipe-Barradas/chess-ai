from stockfish import Stockfish
import chess

class Engine:
    def __init__(self):
       
       self.engine = Stockfish(depth=20, parameters={
            "Debug Log File": "",
            "Contempt": 0,
            "Min Split Depth": 0,
            "Threads": 4, 
            "Ponder": "false",
            "Hash": 2048,
            "MultiPV": 1,
            "Skill Level": 20,
            "Move Overhead": 10,
            "Minimum Thinking Time": 20,
            "Slow Mover": 100,
            "UCI_Chess960": "false",
            "UCI_LimitStrength": "false",
            "UCI_Elo": 2000,
        })

    def get_best_move(self, board):
       self.engine.set_fen_position(board.fen())
       return self.engine.get_best_move()

    def get_eval(self, board):
       self.engine.set_fen_position(board.fen())
       if board.turn == chess.WHITE:
           return self.engine.get_evaluation()["value"]
       
       return -self.engine.get_evaluation()["value"]

    def quit(self):
       self.engine.__del__()
