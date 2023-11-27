import PySimpleGUI as sg      
import chess
from game import Game

pieces = {
    'r': "images/torre_p.png",
    'n': "images/cavalo_p.png",
    'b': "images/bispo_p.png",
    'q': "images/rainha_p.png",
    'k': "images/rei_p.png",
    'p': "images/peao_p.png",
    'R': "images/torre_b.png",
    'N': "images/cavalo_b.png",
    'B': "images/bispo_b.png",
    'Q': "images/rainha_b.png",
    'K': "images/rei_b.png",
    'P': "images/peao_b.png",
    '': "images/vazio.png"
}

def update_element(window, i, j, color):
    window[(i,j)].update(button_color = color)

# Função para desenhar o tabuleiro
def draw_board_by_fen(fen):

    board = fen.split()[0]
    board = board.split('/')
    board = [list(row) for row in board]
    
    layout = []
    for i in range(len(board)):
        row = []
        for j in range(len(board[i])):
            element = board[i][j]
         
            if element.isdigit():
                for k in range(int(element)):
                    row.append(sg.Button("", 
                                         size=(1, 1), 
                                         pad=(0, 0), 
                                         key=(i, k),
                                         image_filename=pieces[""],
                                         image_size=(60,60),
                                         button_color=(Game.get_button_color(i,k))
                                        )
                              )
            else:
                piece = sg.Button("", 
                                  size=(1, 1), 
                                  pad=(0, 0), 
                                  key=(i, j), 
                                  image_filename=pieces[element],
                                  image_size=(60,60),
                                  button_color=(Game.get_button_color(i,j))
                                  )
                
                row.append(piece)  

        layout.append(row)

    return layout

def highlight_move(window, board, from_square):
    moves = board.legal_moves
    for move in moves:
       if move.uci()[:2] == from_square:
           pos = Game.convert_from_uci(move.uci()[2:])
           update_element(window, pos["row"], pos["col"], "red")
    


## Main

tabuleiro = chess.Board()

tabuleiro_layout = draw_board_by_fen(tabuleiro.fen())      

window = sg.Window('Tabuleiro', 
        [
            [sg.Column(tabuleiro_layout, element_justification='center', key='-TABULEIRO-')],
        ])

selected_piece = None

while True:                            
    event, values = window.read()    

    if event == sg.WIN_CLOSED:
        break
    
    if event:
        if selected_piece is None:
            selected_piece = event
            selected_piece = Game.get_uci_move(event[0], event[1])
            
            if tabuleiro.piece_at(chess.parse_square(selected_piece)) is not None:
                highlight_move(window, tabuleiro, selected_piece)
                update_element(window, event[0], event[1], "#0B00EF")
            else:
                selected_piece = None
            
        else:
            origin = selected_piece
            destination = Game.get_uci_move(event[0], event[1])

            move = origin + destination
            # Verifica se o movimento é um roque
            
            if move in ['e1g1', 'e8g8', 'e1c1', 'e8c8']:
                print("Roque")
                tabuleiro.push_uci(move)
            else:
                if Game.check_if_is_possible_move(tabuleiro, move):
                    tabuleiro.push_uci(move)    

                # Update the board
                board = str(tabuleiro).split('\n')
                for i in range(len(board)):
                    board[i] = board[i].split(' ')
        
                for i in range(len(board)):
                    for j in range(len(board[i])):
                        element = board[i][j]
                        
                        if element == ".":
                            window[(i,j)].update(image_filename=pieces[""], 
                                                 image_size=(60,60),
                                                 button_color = Game.get_button_color(i,j)
                                                )
                        else:
                            window[(i,j)].update(image_filename=pieces[element],
                                                 button_color = Game.get_button_color(i,j))

            selected_piece = None

window.close()