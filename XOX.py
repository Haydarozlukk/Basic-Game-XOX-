from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Oyun tahtası ve durum değişkenleri
board = [' '] * 9
current_player = 'X'
game_over = False
winner = None

def check_winner(board, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # yatayy
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # dikey
        [0, 4, 8], [2, 4, 6]              # çapraz
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False

def is_board_full(board):
    return all(spot in ['X', 'O'] for spot in board)

@app.route('/')
def index():
    global board, current_player, game_over, winner
    return render_template('index.html', board=board, current_player=current_player, game_over=game_over, winner=winner)

@app.route('/move', methods=['POST'])
def move():
    global board, current_player, game_over, winner
    move = int(request.form['move'])
    if board[move] == ' ' and not game_over:
        board[move] = current_player
        if check_winner(board, current_player):
            winner = current_player
            game_over = True
        elif is_board_full(board):
            game_over = True
        else:
            current_player = 'O' if current_player == 'X' else 'X'
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    global board, current_player, game_over, winner
    board = [' '] * 9
    current_player = 'X'
    game_over = False
    winner = None
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
