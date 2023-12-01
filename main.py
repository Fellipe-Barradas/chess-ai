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

def exit_game():
    choice = sg.popup_yes_no('Deseja sair do jogo?', title='Confirmação')
    if choice == 'Yes':
        return True
    elif choice == 'No':
        return False

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
row_exit_button = sg.Button('Sair', key='-EXIT-', size=(6, 1), pad=(5, 5))
input_layout = [sg.Text('Escolha o movimento:'), sg.InputText(key='-INPUT-'), sg.Button('Enviar', key='-SEND-')]

layout = [
    [
        sg.Column(tabuleiro_layout, element_justification='center', key='-TABULEIRO-'),
        sg.Column([[turn_label], [sg.Text('Movimentos')], [movements_layout], [reset_button],[row_exit_button]], element_justification='center'),
        [input_layout]
    ],
]

window_choiche = sg.Window('Escolha de jogador', 
                           [[sg.Text('Deseja jogar com as peças brancas?')],
                            [sg.Button('Sim'), sg.Button('Não')]])
while True:
    event, values = window_choiche.read()
    if event == 'Sim':
        escolher_jogador = 'Yes'
        break
    elif event == 'Não':
        escolher_jogador = 'No'
        break
    elif event == sg.WIN_CLOSED:
        break

window_choiche.close()

player_color = "white"

if escolher_jogador == 'No':
    player_color = "black"
    
ai = Ai("white" if player_color == "black" else "white")
movements = []
window = sg.Window('Tabuleiro', layout)

selected_piece = None
while True:
    event, values = window.read(timeout=10)
    
    if Game.get_turn_color(tabuleiro) != player_color:
        print("Vez do computador")
        move = ai.get_best_move(tabuleiro)
        tabuleiro.push(chess.Move.from_uci(move))
        print(move)
        movements.append(move)
        window['-MOVEMENTS-'].update(values=movements)
        update_board(window, tabuleiro)   
     

    else:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            if exit_game():
                break

        if event:

            if event =='-EXIT-':
                if exit_game():
                    break

            if tabuleiro.is_game_over():

                if tabuleiro.is_checkmate():
                    sg.popup_ok('Xeque-mate')
                elif tabuleiro.is_stalemate():
                    sg.popup_ok('Empate')
                elif tabuleiro.is_insufficient_material():
                    sg.popup_ok('Empate por falta de material')
                elif tabuleiro.is_seventyfive_moves():
                    sg.popup_ok('Empate por 75 movimentos')
                elif tabuleiro.is_fivefold_repetition():
                    sg.popup_ok('Empate por repetição de movimentos')
                break

            if event == '-RESET-':
                print("Resetando")
                tabuleiro.reset()
                movements = []
                selected_piece = None
                window['-MOVEMENTS-'].update(values=movements)
                update_board(window, tabuleiro)

            elif event == '-SEND-':
                move = values['-INPUT-']
                if Game.check_if_is_possible_move(tabuleiro, move):
                    tabuleiro.push_uci(move)    
                    movements.append(move)
                    window['-MOVEMENTS-'].update(values=movements)

                # Update the board
                update_board(window, tabuleiro)
            
            elif selected_piece is None:
                selected_piece = event
                print(selected_piece)
                selected_piece = Game.get_uci_move(event[0], event[1])

                if tabuleiro.piece_at(chess.parse_square(selected_piece)) is not None:
                    highlight_move(window, tabuleiro, selected_piece)
                    update_element(window, event[0], event[1], "#0B00EF")
                else:
                    selected_piece = None

            elif selected_piece is not None:
                origin = selected_piece
                destination = Game.get_uci_move(event[0], event[1])

                # Movimento do jogador 
                move = origin + destination
            
                if Game.check_if_is_possible_move(tabuleiro, move):
                    tabuleiro.push_uci(move)    
                    movements.append(move)
                    window['-MOVEMENTS-'].update(values=movements)

                # Update the board
                update_board(window, tabuleiro)

                selected_piece = None

window.close()