import chess
import time

# standart board = rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR

initial_board = "2k1Q3/R7/2N5/8/8/8/8/4K3 b - - 0 1"

piece_values_with_position = {
    chess.PAWN: [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5, 5, 10, 25, 25, 10, 5, 5],
        [0, 0, 0, 20, 20, 0, 0, 0],
        [5, -5, -10, 0, 0, -10, -5, 5],
        [5, 10, 10, -20, -20, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ],
    chess.KNIGHT: [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-30, 5, 15, 20, 20, 15, 5, -30],
        [-30, 0, 15, 20, 20, 15, 0, -30],
        [-30, 5, 10, 15, 15, 10, 5, -30],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ],
    chess.BISHOP: [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 10, 10, 5, 0, -10],
        [-10, 5, 5, 10, 10, 5, 5, -10],
        [-10, 0, 10, 10, 10, 10, 0, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10, 5, 0, 0, 0, 0, 5, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
    ],
    chess.ROOK: [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 10, 10, 10, 10, 10, 10, 5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [0, 0, 0, 5, 5, 0, 0, 0]
    ],
    chess.QUEEN: [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-5, 0, 5, 5, 5, 5, 0, -5],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-10, 5, 5, 5, 5, 5, 0, -10],
        [-10, 0, 5, 0, 0, 0, 0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ],
    chess.KING: [
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [20, 20, 0, 0, 0, 0, 20, 20],
        [20, 30, 10, 0, 0, 10, 30, 20]
    ]
}

def get_piece_value(piece, x, y):
    if piece.piece_type == chess.PAWN:
        return 100 + piece_values_with_position[piece.piece_type][x][y]
    elif piece.piece_type == chess.KNIGHT:
        return 320 + piece_values_with_position[piece.piece_type][x][y]
    elif piece.piece_type == chess.BISHOP:
        return 330 + piece_values_with_position[piece.piece_type][x][y]
    elif piece.piece_type == chess.ROOK:
        return 500 + piece_values_with_position[piece.piece_type][x][y]
    elif piece.piece_type == chess.QUEEN:
        return 900 + piece_values_with_position[piece.piece_type][x][y]
    elif piece.piece_type == chess.KING:
        return 20000 + piece_values_with_position[piece.piece_type][x][y]
    else:
        return 0
    
def evaluate_board(board):
    score = 0
    for i in range(8):
        for j in range(8):
            piece = board.piece_at(chess.square(i, j))
            if piece is not None:
                if piece.color == chess.WHITE:
                    score += get_piece_value(piece, i, j)
                else:
                    score -= get_piece_value(piece, i, j)

    return score

def best_move_using_minimax(board, depth):
    white_to_play = board.turn
    best_score = -99999 if white_to_play else 99999
    best_move = None

    score, move = minimax(board, depth - 1, -9999, 9999, white_to_play)

    if score > best_score and white_to_play:
            best_score = score
            best_move = move
    elif score < best_score and not white_to_play:
        best_score = score
        best_move = move
       
    return best_move

def minimax(board, depth, alpha, beta, white_to_play):
    if depth == 0:
        return evaluate_board(board), None
    if white_to_play:
        best_score = -9999
        best_move = None
        for move in board.legal_moves:
            board.push(move)
            score, _ = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
        return best_score, best_move
    else:
        best_score = 9999
        best_move = None
        for move in board.legal_moves:
            board.push(move)
            score, _ = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, best_score)
            if alpha >= beta:
                break
        return best_score, best_move

def main():
    board = chess.Board()

    while board.is_game_over() == False:
        start_time = time.time()
        if board.turn == chess.WHITE:
            move = best_move_using_minimax(board, 5)
            print(f"White move: {move}")
            board.push(move)
        else:
            move = best_move_using_minimax(board, 5)
            print(f"Black move: {move}")
            board.push(move)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(board)

        print(f"Pontos avalido: {evaluate_board(board)}")
        print(f"Tempo decorrido: {elapsed_time:.2f} segundos")
        print("")

    print("Fim de jogo!")

start_time = time.time()
main()
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Tempo decorrido: {elapsed_time:.2f} segundos")