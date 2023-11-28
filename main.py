import PySimpleGUI as sg      
import chess
from game import Game
from engine.ai import Ai

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

def update_board(window, board):
    board = str(board).split('\n')
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

def update_element(window, i, j, color):
    window[(i,j)].update(button_color = color)


def draw_board_by_fen(fen):
    pos_letra = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    pos_numero = ['8', '7', '6', '5', '4', '3', '2', '1']

    board = fen.split()[0]
    board = board.split('/')
    board = [list(row) for row in board]

    layout = []

    for i in range(len(board)):
        row = []
        row.append(sg.Text(pos_numero[i], size=(1, 1), pad=(0, 0), font=("Helvetica", 20))) 
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
    row = []
    for i in range(len(pos_letra)):
        row.append(sg.Text(pos_letra[i], size=(4, 3), pad=(0, 0), font=("Helvetica", 20), justification='center')) 
    layout.append(row)
    return layout

def highlight_move(window, board, from_square):
    moves = board.legal_moves
    for move in moves:
       if move.uci()[:2] == from_square:
           pos = Game.convert_from_uci(move.uci()[2:])
           update_element(window, pos["row"], pos["col"], "red")

 
tabuleiro = chess.Board()
tabuleiro_layout = draw_board_by_fen(tabuleiro.fen())      
movements_layout = sg.Listbox(values=[], size=(10, 20), key='-MOVEMENTS-')
turn_label = sg.Text('Turno do Jogador Branco', key='-TURN-')
reset_button = sg.Button('Reiniciar Partida', key='-RESET-')

layout = [
    [
        sg.Column(tabuleiro_layout, element_justification='center', key='-TABULEIRO-'),
        sg.Column([[turn_label], [sg.Text('Movimentos')], [movements_layout], [reset_button]], element_justification='center')
    ],
]

window = sg.Window('Tabuleiro', layout)

selected_piece = None

player_color = "white"
ai = Ai("black")
movements = []
white_turn = True

while True:
    if event == '-RESET-':
        print("Resetando")
        tabuleiro.reset()
        movements = []
        window['-MOVEMENTS-'].update(values=movements)
        white_turn = True
        turn_label.update('Turno do Jogador Branco')

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
                     
    if not tabuleiro.turn:
        print("Vez do computador")
        move = ai.get_best_move(tabuleiro)
        tabuleiro.push(chess.Move.from_uci(move))
        print(move)
        update_board(window, tabuleiro)    
                                
    event, values = window.read()    

    if event == sg.WIN_CLOSED:
        break

    if tabuleiro.is_game_over():
        # Mostra popup de fim de jogo
        break

    if tabuleiro.turn:
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

                # Movimento do jogador 
                move = origin + destination
               
                if Game.check_if_is_possible_move(tabuleiro, move):
                    tabuleiro.push_uci(move)    
                    movements.append(move)
                    window['-MOVEMENTS-'].update(values=movements)

                    # Alterna o turno
                    white_turn = not white_turn

                    # Atualiza a label de turno
                    turn_label.update('Turno do Jogador Branco' if white_turn else 'Turno do Jogador Preto')

                # Update the board
                update_board(window, tabuleiro)

                selected_piece = None

window.close()
