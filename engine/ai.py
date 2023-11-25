import chess.engine

class Ai:
    def __init__(self, color):
        self.engine = chess.engine.SimpleEngine.popen_uci("/home/luis/virtual_env/chess-ai/engine/stockfish/stockfish/stockfish-ubuntu-x86-64-avx2")
        self.color = color

    def get_best_move(self, board):
        return self.engine.play(board, chess.engine.Limit(time=0.5))
    
    def get_eval(self, board):
        if self.color == chess.WHITE:
            return self.engine.analyse(board, chess.engine.Limit(time=0.5))["score"].white().score()
        
        return self.engine.analyse(board, chess.engine.Limit(time=0.1))["score"].black().score()
    
    def __del__(self):
        self.engine.quit()