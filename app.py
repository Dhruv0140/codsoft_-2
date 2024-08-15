from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Initialize the board
board = ['' for _ in range(9)]
game_status = {'winner': None, 'turn': 'X'}

def is_winner(board, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]  # diagonals
    ]
    return any(all(board[i] == player for i in condition) for condition in win_conditions)

def minimax(board, depth, is_maximizing):
    if is_winner(board, 'O'):
        return 1
    if is_winner(board, 'X'):
        return -1
    if all(cell != '' for cell in board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == '':
                board[i] = 'O'
                score = minimax(board, depth + 1, False)
                board[i] = ''
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == '':
                board[i] = 'X'
                score = minimax(board, depth + 1, True)
                board[i] = ''
                best_score = min(score, best_score)
        return best_score

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
    global board, game_status
    data = request.get_json()
    player_move = int(data['move'])

    if game_status['winner']:
        return jsonify({'board': board, 'status': game_status})

    if board[player_move] == '' and game_status['turn'] == 'X':
        board[player_move] = 'X'
        if is_winner(board, 'X'):
            game_status = {'winner': 'X', 'turn': None}
        elif all(cell != '' for cell in board):
            game_status = {'winner': 'Draw', 'turn': None}
        else:
            # AI Move
            best_score = -float('inf')
            best_move = None
            for i in range(9):
                if board[i] == '':
                    board[i] = 'O'
                    score = minimax(board, 0, False)
                    board[i] = ''
                    if score > best_score:
                        best_score = score
                        best_move = i

            if best_move is not None:
                board[best_move] = 'O'
                if is_winner(board, 'O'):
                    game_status = {'winner': 'O', 'turn': None}
                elif all(cell != '' for cell in board):
                    game_status = {'winner': 'Draw', 'turn': None}
                else:
                    game_status['turn'] = 'X'

    return jsonify({'board': board, 'status': game_status})

@app.route('/restart', methods=['POST'])
def restart():
    global board, game_status
    board = ['' for _ in range(9)]
    game_status = {'winner': None, 'turn': 'X'}
    return jsonify({'board': board, 'status': game_status})

if __name__ == '__main__':
    app.run(debug=True)
