import PySimpleGUI as sg      
import chess

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

def check_if_is_possible_move(board, destination):
    return destination in [move.uci() for move in board.legal_moves]

def update_element(window, i, j, color):
    window[(i,j)].update(button_color = color)
    

def get_button_color(i,j):
    return "#7c7c7c" if (i + j) % 2 == 0 else "#cccccc"

# Função para converter a posição do tabuleiro para a notação do chess
def make_move(origin, destination):
    colluns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    rows = ['8', '7', '6', '5', '4', '3', '2', '1']

    origin_col = colluns[origin['col']]
    origin_row = rows[origin['row']]

    destination_col = colluns[destination['col']]
    destination_row = rows[destination['row']]

    return f"{origin_col}{origin_row}{destination_col}{destination_row}"

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
                                         button_color=(get_button_color(i,k))
                                        )
                              )
            else:
                piece = sg.Button("", 
                                  size=(1, 1), 
                                  pad=(0, 0), 
                                  key=(i, j), 
                                  image_filename=pieces[element],
                                  image_size=(60,60),
                                  button_color=(get_button_color(i,j))
                                  )
                
                row.append(piece)  

        layout.append(row)

    return layout


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

            update_element(window, selected_piece[0], selected_piece[1], "#0B00EF")
        else:
            
            origin = {'row': selected_piece[0], 'col': selected_piece[1]}
            update_element(window,selected_piece[0], selected_piece[1], get_button_color(origin["row"], origin["col"]))
            
            destination = {'row': event[0], 'col': event[1]}

            move = make_move(origin, destination)

            # Verifica se o movimento é um roque
        
            if move in ['e1g1', 'e8g8', 'e1c1', 'e8c8']:
                print("Roque")
                tabuleiro.push_uci(move)
            else:
                if check_if_is_possible_move(tabuleiro, move):
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
                                                 button_color = get_button_color(i,j)
                                                )
                        else:
                            window[(i,j)].update(image_filename=pieces[element],
                                                 button_color = get_button_color(i,j))

            selected_piece = None

window.close()