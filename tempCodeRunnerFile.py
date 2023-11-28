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
                                    