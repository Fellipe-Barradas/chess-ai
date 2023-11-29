import chess

colluns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
rows = ['8', '7', '6', '5', '4', '3', '2', '1']
class Game:

    @staticmethod
    def check_if_is_possible_move(board, destination):
        return destination in [move.uci() for move in board.legal_moves]
    
    @staticmethod
    def get_button_color(i,j):
        return "#7c7c7c" if (i + j) % 2 == 0 else "#cccccc"
    
    @staticmethod
    def get_uci_move(i,j):

        origin_col = colluns[j]
        origin_row = rows[i]

        return f"{origin_col}{origin_row}"
    
    @staticmethod
    def convert_from_uci(pos):

        return {
            "col" : colluns.index(pos[0]),
            'row': rows.index(pos[1])
        }
    
    @staticmethod
    def get_turn_color(board):
        return "white" if board.turn == chess.WHITE else "black"