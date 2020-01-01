# import chess_data


def legal_castles(position):
    board = position[0]
    white_can_castle_short = position[2][0]
    white_can_castle_long = position[2][1]
    black_can_castle_short = position[2][2]
    black_can_castle_long = position[2][3]
    if not board[5][1] == "White_king":
        white_can_castle_short = 0
        white_can_castle_long = 0
    if not board[1][1] == "White_rook":
        white_can_castle_long = 0
    if not board[8][1] == "White_rook":
        white_can_castle_short = 0
    if not board[5][8] == "Black_king":
        black_can_castle_short = 0
        black_can_castle_long = 0
    if not board[1][8] == "Black_rook":
        black_can_castle_long = 0
    if not board[8][8] == "Black_rook":
        black_can_castle_short = 0
    return white_can_castle_short, white_can_castle_long, black_can_castle_short, black_can_castle_long


def game_over(position):
    if len(legal_moves(position)) == 0:
        return True
    else:
        return False


def new_board():
    the_board = [[" ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " "]]

    for i in range(1, 9):
        the_board[i][2] = "White_pawn"
        the_board[i][7] = "Black_pawn"
    the_board[1][1] = "White_rook"
    the_board[8][1] = "White_rook"
    the_board[1][8] = "Black_rook"
    the_board[8][8] = "Black_rook"
    the_board[2][1] = "White_knight"
    the_board[7][1] = "White_knight"
    the_board[2][8] = "Black_knight"
    the_board[7][8] = "Black_knight"
    the_board[3][1] = "White_bishop"
    the_board[6][1] = "White_bishop"
    the_board[6][8] = "Black_bishop"
    the_board[3][8] = "Black_bishop"
    the_board[4][1] = "White_queen"
    the_board[5][1] = "White_king"
    the_board[4][8] = "Black_queen"
    the_board[5][8] = "Black_king"
    return the_board


def no_pieces(board, old_x, old_y, new_x, new_y):
    if old_y > new_y:
        big_y = old_y
        small_y = new_y
    else:
        big_y = new_y
        small_y = old_y
    if old_x > new_x:
        big_x = old_x
        small_x = new_x
    else:
        big_x = new_x
        small_x = old_x

    if new_x == old_x:
        for num in range(small_y + 1, big_y):
            if not board[old_x][num] == " ":
                return False

    elif new_y == old_y:
        for num in range(small_x + 1, big_x):
            if not board[num][old_y] == " ":
                return False
    else:
        for i in range(1, big_x - small_x):
            if (big_x == new_x and big_y == new_y) or (big_x == old_x and big_y == old_y):
                if not board[small_x + i][small_y + i] == " ":
                    return False
            else:
                if not board[small_x + i][big_y - i] == " ":
                    return False
    return True


def move_is_legal(position, old_square, new_square):
    board = position[0]
    castles = position[2]
    previous_move = position[3]

    old_x = old_square[0]
    old_y = old_square[1]
    new_x = new_square[0]
    new_y = new_square[1]

    if board[old_x][old_y][6:] == "knight":
        if abs(old_x - new_x) == 2 and abs(old_y - new_y) == 1 or abs(old_x - new_x) == 1 and abs(old_y - new_y) == 2:
            return True
    elif board[old_x][old_y] == "White_pawn":
        if old_x == new_x and (
                # old_y + 1 == new_y or old_y == 2 and new_y == 4 and no_pieces(board, old_x, old_y, new_x, new_y)) and \
                old_y + 1 == new_y or old_y == 2 and new_y == 4 and no_pieces(board, old_x, old_y, new_x, new_y)) and board[new_x][new_y] == " ":
            return True
        elif abs(old_x - new_x) == 1 and old_y + 1 == new_y:
            if board[new_x][new_y][0:5] == "Black":
                return True
            elif previous_move[0] == new_x and previous_move[1] == 7 and previous_move[3] == 5 and board[new_x][
                new_y - 1] == "Black_pawn":
                return True
    elif board[old_x][old_y] == "Black_pawn":
        if old_x == new_x and (
                # old_y - 1 == new_y or old_y == 7 and new_y == 5 and no_pieces(board, old_x, old_y, new_x, new_y)) and \
                old_y - 1 == new_y or old_y == 7 and new_y == 5 and no_pieces(board, old_x, old_y, new_x, new_y)) and board[new_x][new_y] == " ":
            return True
        elif abs(old_x - new_x) == 1 and old_y - 1 == new_y:
            if board[new_x][new_y][0:5] == "White":
                return True
            elif previous_move[0] == new_x and previous_move[1] == 2 and previous_move[3] == 4 and board[new_x][
                new_y + 1] == "White_pawn":
                return True
    elif board[old_x][old_y][6:] == "rook" or board[old_x][old_y][6:] == "queen":
        if old_x == new_x and not old_y == new_y or not old_x == new_x and old_y == new_y:
            if no_pieces(board, old_x, old_y, new_x, new_y):
                return True
    elif board[old_x][old_y][6:] == "king":
        if abs(new_x - old_x) <= 1 and abs(new_y - old_y) <= 1:
            return True
        else:
            white_can_castle_short = castles[0]
            white_can_castle_long = castles[1]
            black_can_castle_short = castles[2]
            black_can_castle_long = castles[3]
            if board[old_x][old_y] == "White_king" and not king_is_in_danger([board, True, castles, previous_move]):
                if new_y == 1 and no_pieces(board, old_x, old_y, new_x, new_y) and board[new_x][new_y] == " ":
                    # and not king_is_in_danger(board, True):
                    # squares between in check
                    if new_x == 3 and white_can_castle_long:
                        return True
                    elif new_x == 7 and white_can_castle_short:
                        return True
            elif not king_is_in_danger([board, False, castles, previous_move]):
                if new_y == 8 and no_pieces(board, old_x, old_y, new_x, new_y) and board[new_x][new_y] == " ":
                    # and not king_is_in_danger(board, False):
                    # squares between in check
                    if new_x == 3 and black_can_castle_long:
                        return True
                    elif new_x == 7 and black_can_castle_short:
                        return True

    if board[old_x][old_y][6:] == "bishop" or board[old_x][old_y][6:] == "queen":
        if abs(new_x - old_x) == abs(new_y - old_y) and no_pieces(board, old_x, old_y, new_x, new_y):
            return True
    return False


def valid_move(position, old_square, new_square):
    board = position[0]
    turn = position[1]
    if old_square == new_square or new_square[0] < 1 or new_square[1] < 1:
        return False
    # print(old_square, new_square, turn)
    if turn:
        if not "White" == board[old_square[0]][old_square[1]][0:5]:
            return False
        elif "White" == board[new_square[0]][new_square[1]][0:5]:
            return False
        elif not move_is_legal(position, old_square, new_square):
            return False
    else:
        if not "Black" == board[old_square[0]][old_square[1]][0:5]:
            return False
        elif "Black" == board[new_square[0]][new_square[1]][0:5]:
            return False
        elif not move_is_legal(position, old_square, new_square):
            return False
    return True


def legal_moves(position):
    # print(position)
    # board = [row[:] for row in position[0]]
    board = position[0]
    turn = position[1]
    # my_legal = True
    color = "White"
    if not turn:
        color = "Black"
    board_for_legal_moves = [row[:] for row in board]
    moves_list = []
    for i in range(1, 9):
        for j in range(1, 9):
            if not board_for_legal_moves[i][j] == " ":
                # print(board_for_legal_moves[i][j][:5])
                if board_for_legal_moves[i][j][:5] == color:
                    for x in range(1, 9):
                        for y in range(1, 9):
                            if not board_for_legal_moves == board:
                                print("error!")
                            board2, my_legal = move(position, [i, j], [x, y])
                            if my_legal:
                                legal_move = [i, j, x, y]
                                moves_list.insert(0, legal_move)
    return moves_list


def promote_pawns(board):
    # need to add promote to other pieces
    for i in range(1, 9):
        if board[i][8] == "White_pawn":
            return True, "White_queen", i, 8
        if board[i][1] == "Black_pawn":
            return True, "Black_queen", i, 1
    return False, " "


def numbers_to_move(position, move):
    try:
        board = position[0]
        if board[move[0]][move[1]] == " ":
            return " "
        piece = board[move[0]][move[1]][6:]
        answer = ""
        # I need to add which of the pieces if two piece can so the same move
        if piece == "pawn":
            answer = ""
        elif piece == "knight":
            answer = "N"
        elif piece == "bishop":
            answer = "B"
        elif piece == "rook":
            answer = "R"
        elif piece == "queen":
            answer = "Q"
        elif position[1] and move == [5, 1, 7, 1] or not position[1] and move == [5, 8, 7, 8]:
            return "0-0"
        elif position[1] and move == [5, 1, 3, 1] or not position[1] and move == [5, 8, 3, 8]:
            return "0-0-0"
        else:
            answer == "K"
        if not board[move[2]][move[3]] == " ":
            if piece == "pawn":
                answer = chr(96 + move[0])
            answer = answer + ":"  # x
        answer = answer + chr(96 + move[2]) + str(move[3])
        if piece == "pawn" and (position[1] and move[3] == 8 or not position[1] and move[3] == 0):
            answer += "(Q)"  # I need to add options of promoting other pieces
        return answer
    except Exception:
        return ""


def king_is_in_danger(position):
    board = position[0]
    turn = position[1]

    king_pos_x = 0
    king_pos_y = 0
    king = "White_king"
    if not turn:
        king = "Black_king"

    king_found = False
    for x in range(1, 9):
        for y in range(1, 9):
            if board[x][y] == king:
                king_pos_x = x
                king_pos_y = y
                king_found = True
                break
            if king_found:
                break

    for i in range(1, 9):
        for j in range(1, 9):
            if not board[i][j] == " ":
                if not board[i][j][:5] == king[:5]:
                    if board[i][j][6:] == "king":
                        if abs(king_pos_x - i) <= 1 and abs(king_pos_y - j) <= 1:
                            return True
                    elif move_is_legal(position, [i, j], [king_pos_x, king_pos_y]):
                        return True
    return False


def move(position, previous_position, new_position):
    board = position[0]
    turn = position[1]

    my_old_board = [row[:] for row in board]
    my_new_board = [row[:] for row in board]
    try:
        if valid_move(position, previous_position, new_position):  # position?
            my_new_board[new_position[0]][new_position[1]] = my_new_board[previous_position[0]][previous_position[1]]
            my_new_board[previous_position[0]][previous_position[1]] = " "

            pawns_to_promote = promote_pawns(my_new_board)
            if pawns_to_promote[0]:
                my_new_board[pawns_to_promote[2]][pawns_to_promote[3]] = pawns_to_promote[1]
            if turn:
                if my_old_board[new_position[0]][new_position[1]] == " " and my_new_board[new_position[0]][new_position[1]] == "White_pawn":
                    my_new_board[new_position[0]][new_position[1] - 1] = " "
            else:
                if my_old_board[new_position[0]][new_position[1]] == " " and my_new_board[new_position[0]][new_position[1]] == "Black_pawn":
                    my_new_board[new_position[0]][new_position[1] + 1] = " "
            if king_is_in_danger([my_new_board, turn, position[2], position[3]]):
                return my_old_board, False
            else:
                if my_old_board[previous_position[0]][previous_position[1]][6:] == "king" and abs(previous_position[0] - new_position[0]) > 1:
                    if new_position[0] == 7 and new_position[1] == 1:
                        my_new_board[8][1] = " "
                        my_new_board[6][1] = "White_rook"
                    elif new_position[0] == 3 and new_position[1] == 1:
                        my_new_board[1][1] = " "
                        my_new_board[4][1] = "White_rook"
                    elif new_position[0] == 7 and new_position[1] == 8:
                        my_new_board[8][8] = " "
                        my_new_board[6][8] = "Black_rook"
                    else:
                        my_new_board[1][8] = " "
                        my_new_board[4][8] = "Black_rook"

                return my_new_board, True
        else:
            return my_old_board, False
    except Exception as error:
        print(error)
        return my_old_board, False
