from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)
game_board = np.full((3, 3), None)
current_player = 'X'  # AI is 'X', player is 'O'

def check_winner(board):
    for i in range(3):
        if board[i, :].tolist().count(board[i, 0]) == 3 and board[i, 0] is not None:
            return board[i, 0]  # Return 'X' or 'O'
        if board[:, i].tolist().count(board[0, i]) == 3 and board[0, i] is not None:
            return board[0, i]

    if board.diagonal().tolist().count(board[0, 0]) == 3 and board[0, 0] is not None:
        return board[0, 0]

    if np.fliplr(board).diagonal().tolist().count(board[0, 2]) == 3 and board[0, 2] is not None:
        return board[0, 2]

    if np.all(board != None):
        return 'Draw'  # If all cells are filled and no winner

    return None  # Continue game

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    global current_player
    data = request.json
    row, col = data['row'], data['col']
    
    
    if game_board[row, col] is None:
        game_board[row, col] = 'O'  # Player's move
        winner = check_winner(game_board)
        if winner:
            return jsonify({'board': game_board.tolist(), 'status': 'win', 'player': winner, 'game_over': True})

        ai_row, ai_col = best_move(game_board)
        game_board[ai_row, ai_col] = 'X'  # AI's move
        winner = check_winner(game_board)
        if winner:
            return jsonify({'board': game_board.tolist(), 'status': 'win', 'player': winner, 'game_over': True})

    return jsonify({'board': game_board.tolist(), 'status': 'continue', 'game_over': False})

@app.route('/reset', methods=['POST'])
def reset():
    global game_board
    game_board = np.full((3, 3), None)
    return jsonify({'board': game_board.tolist()})

def minimax(board, depth, is_maximizing, alpha, beta):
    score = check_winner(board)
    if score == 'X':
        return 10 - depth  # AI wins
    if score == 'O':
        return depth - 10  # Opponent wins
    if score == 'Draw':
        return 0  # Draw

    if is_maximizing:
        max_eval = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i, j] is None:
                    board[i, j] = 'X'
                    eval = minimax(board, depth + 1, False, alpha, beta)
                    board[i, j] = None
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i, j] is None:
                    board[i, j] = 'O'
                    eval = minimax(board, depth + 1, True, alpha, beta)
                    board[i, j] = None
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

def best_move(board):
    best_val = -float('inf')
    move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i, j] is None:
                board[i, j] = 'X'  # AI's move
                move_val = minimax(board, 0, False, -float('inf'), float('inf'))
                board[i, j] = None
                if move_val > best_val:
                    move = (i, j)
                    best_val = move_val
    return move

if __name__ == '__main__':
    app.run(debug=True)
