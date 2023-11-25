import chess
from engine.ai import Ai
from game import Game


def main():
    board = chess.Board()
    player_color = Game.get_player_color()

    ai = Ai("white" if player_color == "black" else "black")
    print(board)
    print("-------------------")
    print("")

    while board.is_game_over() == False:
       
        if Game.is_player_turn(board, player_color):
            player_move = Game.get_player_move(board)
            board.push_san(player_move.uci())
            print("")
        else:
            result = ai.get_best_move(board)
            print(f"IA movimento: {result}")
            board.push(chess.Move.from_uci(result))
            print(board)
            print(f"Pontos avaliados: {ai.get_eval(board)} \n")

        

    print("Fim de jogo! ")

main()