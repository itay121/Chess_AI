import chess_eval
import chess_game
import math

# mini_max(position, 3, -infintiy, infinity, turn)

def mini_max(position, depth, alpha, beta, maximazing_player):
    if depth == 0 or chess_game.game_over(position):
        # print(chess_eval.comp_eval(position), position[3], 2 - depth)
        return position[3], chess_eval.comp_eval(position)
    elif maximazing_player:
        max_eval = ["", -math.inf]
        for option in my_options(position):
            move, eval = mini_max(option, depth - 1, alpha, beta, False)
            # move_with_eval = [move, eval]
            if eval > max_eval[1] or max_eval[0] == "":
                max_eval = [option[3], eval]
            # else:
                # print(option[3], eval, 2 - depth)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        # print(best_move)
        return max_eval
    else:
        min_eval = ["", math.inf]
        for option in my_options(position):
            move, eval = mini_max(option, depth - 1, alpha, beta, True)
            if eval < min_eval[1] or min_eval[0] == "":
                # print(option[3], eval, 2 - depth, "min")
                min_eval = [option[3], eval]
            # else:
                # print(option[3], eval, 2 - depth)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        # print(min_eval)
        return min_eval

def my_options(position):
    my_moves_list = chess_game.legal_moves(position)
    the_options = []
    for move in my_moves_list:
        new_board, legal = chess_game.move(position, [move[0], move[1]], [move[2], move[3]])
        new_pos = [new_board, not position[1], chess_game.legal_castles([new_board, not position[1], position[2], move]), move]
        # print(move)
        the_options.append(new_pos)
    return  the_options
