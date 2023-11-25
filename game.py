import chess
class Game:

    @staticmethod
    def get_player_color():
        player_color = input("Escolha a cor das SUAS peças (branco ou preto): ")
        while player_color != "branco" and player_color != "preto":
            player_color = input("Escolha a cor das SUAS peças (branco ou preto): ")

        return "white" if player_color == "branco" else "black"

    @staticmethod
    def is_player_turn(board, player_color):
        if player_color == "white":
            return board.turn == chess.WHITE
        else:
            return board.turn == chess.BLACK
        
    @staticmethod
    def get_player_move(board):
        player_move = input("Digite sua jogada, como por exemplo: e2e4\nJogada: ")
        try:
           move = chess.Move.from_uci(player_move)
           if move in board.legal_moves:
               return move
           else:
               print("Movimento inválido. Tente novamente.")
        except ValueError:
           print("Formato de movimento inválido. Tente novamente.")