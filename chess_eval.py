import math
import chess_game
# import chess_data


def comp_eval(position):
    board = position[0]
    turn = position[1]
    pieces_value = {"pawn": 1, "knight": 3, "bishop": 3, "rook": 5, "queen": 9, "king": 999}
    my_eval = 0
    for row in board:
        for piece in row:
            if not piece == " ":
                piece_value = pieces_value[piece[6:]]
                if piece[:5] == "White":
                    my_eval += piece_value
                else:
                    my_eval -= piece_value
    enemy_legal_moves = 0  # len(chess_game.legal_moves([board, not turn, position[2], position[3]]))
    my_multi = 1
    if not turn:
        my_multi = -1
    my_legal_moves = len(chess_game.legal_moves(position))
    my_eval += ((my_legal_moves - enemy_legal_moves) / 50 * my_multi)
    if my_legal_moves == 0:
        if chess_game.king_is_in_danger(position):
            return math.inf * -1 * my_multi
        else:
            return 0
    return my_eval
