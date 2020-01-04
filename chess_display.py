# from PIL import Image
import math
import pygame
import string
# import chess_data
import chess_game
# import chess_eval
import chess_alpha_beta_pruning as chess_AI
# import chess_AI
from importlib import reload
from _datetime import datetime
import os

my_link = os.path.realpath(__file__)
start_link = my_link[0:my_link.rfind("\\")] + r"\\"

"""
chess_data.create_new_data()
reload(chess_game)
reload(chess_AI)
"""
pygame.init()

height = 650
weight = 500
screen = pygame.display.set_mode((height, weight))

pygame.display.set_caption("Chess")
my_board = pygame.image.load(start_link + 'big_chess_board.png')

icon = pygame.image.load(start_link + r'chess_icon.png')
pygame.display.set_icon(icon)

font = pygame.font.Font("freesansbold.ttf", 32)
my_clock_x = weight + 20
my_clock_y = height / 2.4
enemy_clock_x = weight + 20
enemy_clock_y = height / 3

moves_without_captures_or_pawn_moves = 0


def show_piece(piece, square):
    x, y = square_place(square)
    my_img = img_bank(piece)
    # my_img = pygame.image.load(img)
    screen.blit(my_img, (x, y))


def show_pieces(board_to_show):
    for letter in "abcdefgh":
        for number in range(1, 9):
            if not board_to_show[string.ascii_lowercase.index(letter) + 1][number] == " ":
                show_piece(board_to_show[string.ascii_lowercase.index(letter) + 1][number], letter + str(number))


def show_board():
    screen.blit(my_board, (0, 0))


def img_bank(piece):
    link = start_link + piece + ".png"
    img = pygame.image.load(link)
    return img
    # return pieces_bank[piece]


def square_place(square):
    my_weight = 500
    my_height = 500
    x = my_weight / 8 * string.ascii_lowercase.index(square[0]) - 3
    y = my_height - my_height / 8 * int(square[1]) - 7
    # change the height
    return x, y


def cordinates_to_square(x, y):
    my_height = 500
    my_weight = 500
    my_x_square = math.ceil((x + 3) * 8 / my_weight)
    my_y_square = math.ceil(8 - (y + 7) / my_height * 8)
    return my_x_square, my_y_square


def print_pgn(move_list, my_result="", event="", site="", date="", round="", white_player="", black_player=""):
    my_event = '[Event "' + str(event) + '"] \n'
    my_site = '[Site "' + str(site) + '"] \n'
    my_date = '[Date "' + str(date) + '"] \n'
    my_round = '[Round "' + str(round) + '"] \n'
    white = '[White "' + white_player + '"] \n'
    black = '[Black "' + black_player + '"] \n'
    result = '[Result "' + str(my_result) + '"] \n'
    pgn = my_event + my_site + my_date + my_round + white + black + result
    print(pgn)
    print_move_list(move_list)
    if my_result == 0.5:
        print("0.5 - 0.5")
    elif my_result == 1:
        print("1 - 0")
    else:
        print("0 - 1")


'''
def pgn_to_game(pgn):
    event = pgn[pgn.find('Event "'):pgn.find('"', pgn.find('Event "'))]
'''


def print_move_list(move_list):
    for i in range(0, int(len(move_list) / 2)):
        print(str(i + 1) + "." + move_list[2 * i] + " " + move_list[2 * i + 1])


"""
def getKeysByValue(dictOfElements, valueToFind):
    # https://thispointer.com/python-how-to-find-keys-by-value-in-dictionary/
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item in listOfItems:
        if item[1] == valueToFind:
            listOfKeys.append(item[0])
    return listOfKeys
"""


def show_clocks():
    my_clock = my_time - my_wasted_time
    comp_clock = comp_time - comp_wasted_time

    my_minutes = str(int(my_clock / 60))
    my_seconds = str(int(my_clock % 60))
    if len(my_minutes) == 1:
        my_minutes = "0" + my_minutes
    if len(my_seconds) == 1:
        my_seconds = "0" + my_seconds

    enemy_minutes = str(int(comp_clock / 60))
    enemy_seconds = str(int(comp_clock % 60))

    if len(enemy_minutes) == 1:
        enemy_minutes = "0" + enemy_minutes
    if len(enemy_seconds) == 1:
        enemy_seconds = "0" + enemy_seconds

    my_current_time = font.render(my_minutes + ":" + my_seconds, True, (255, 255, 255))
    enemy_current_time = font.render(enemy_minutes + ":" + enemy_seconds, True, (255, 255, 255))
    if my_wasted_time >= my_time:
        screen.blit(font.render("00:00", True, (255, 255, 255)), (my_clock_x, my_clock_y))
    else:
        screen.blit(my_current_time, (my_clock_x, my_clock_y))
    if comp_wasted_time >= comp_time:
        screen.blit(font.render("00:00", True, (255, 255, 255)), (enemy_clock_x, enemy_clock_y))
    else:
        screen.blit(enemy_current_time, (enemy_clock_x, enemy_clock_y))
    # enemy_current_time = font.render(my_clock, True, (255,255,255))


board = chess_game.new_board()
turn = True
castles = [True, True, True, True]  # [White king side, White queen side, Black king side, Black queen side]
previous_move = " "
position = [board, turn, castles, previous_move]  # Maybe add moves list?

selected = False
running = True
my_comp_eval = 0
current_depth = 2
bonus_time_for_move = 0
my_time = 5 * 60
comp_time = 5 * 60
my_wasted_time = 0
comp_wasted_time = 0
done = False
move_list = []
move_list_printed = False
my_current_time = datetime.now()
result = ""

while running:
    screen.fill((0, 0, 0))
    show_board()
    show_pieces(position[0])
    my_diffrence = datetime.now() - my_current_time
    my_wasted_time += my_diffrence.total_seconds()
    my_current_time = datetime.now()
    show_clocks()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif not done:
            x, y = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                if not selected:
                    x_square, y_square = cordinates_to_square(x, y)
                    first_position = x_square, y_square
                    # print("mark_square(" + chr(x_square + 96) + str(y_square) + ")")
                    # mark square
                    selected = True
                else:
                    x_square1, y_square1 = cordinates_to_square(x, y)
                    second_position = x_square1, y_square1
                    # print("move mark(" + chr(x_square1 + 96) + str(y_square1) + ")")
                    move = chess_game.numbers_to_move(position, [first_position[0], first_position[1], second_position[0], second_position[1]])
                    # print(first_position, second_position)
                    board, legal = chess_game.move(position, first_position, second_position)
                    if legal:
                        white_can_castle_short, white_can_castle_long, black_can_castle_short, black_can_castle_long = chess_game.legal_castles(position)
                        previous_move = [first_position[0], first_position[1], second_position[0], second_position[1]]
                        turn = not turn
                        position = [board, turn, [white_can_castle_short, white_can_castle_long, black_can_castle_short, black_can_castle_long], previous_move]
                        screen.fill((0, 0, 0))
                        show_board()
                        show_pieces(position[0])
                        # my_diffrence = datetime.now() - my_current_time
                        # my_wasted_time += my_diffrence.total_seconds()
                        my_time += bonus_time_for_move
                        comp_current_time = datetime.now()
                        pygame.display.update()

                        if board[second_position[0]][second_position[1]][6:] == "pawn":
                            # I need to consider that the pawn can promote
                            moves_without_captures_or_pawn_moves = 0
                        else:
                            moves_without_captures_or_pawn_moves += 0.5

                        """
                        chess_data.change_data("white_can_castle_short", white_can_castle_short)
                        chess_data.change_data("white_can_castle_long", white_can_castle_long)
                        chess_data.change_data("black_can_castle_short", black_can_castle_short)
                        chess_data.change_data("black_can_castle_long", black_can_castle_long)
                        chess_data.change_data("previous_move", previous_move)
                        """
                        selected = False
                        my_legal_moves = chess_game.legal_moves(position)
                        if chess_game.king_is_in_danger(position):
                            if len(my_legal_moves) == 0:
                                move = move + "#"
                                print(move)
                                move_list.append(move)
                                # print("Checkmate!")
                                done = True
                                result = 1
                                break
                            else:
                                move = move + "+"
                                # I need to add double check
                                # print("Check!")
                            # mark king square
                        elif len(my_legal_moves) == 0:
                            print("Stalemate!")
                            result = 0.5
                            done = True
                            break
                        if moves_without_captures_or_pawn_moves == 50:
                            print("Draw due to the 50 moves rule!")
                            done = True
                            result = 0.5
                            break
                        move_list.append(move)
                        print(move)
                        legal = False
                        while not legal:
                            computer_move, computer_move_value = chess_AI.mini_max(position, current_depth, -math.inf, math.inf, turn)
                            # print(computer_move_value)
                            # print(computer_move)
                            previous_pos = [computer_move[0], computer_move[1]]
                            new_pos = [computer_move[2], computer_move[3]]
                            # board, legal, the_comp_move, my_comp_eval = comp_move(board, turn)
                            previous_move = [previous_pos[0], previous_pos[1], new_pos[0], new_pos[1]]
                            move = chess_game.numbers_to_move(position, previous_move)
                            board, legal = chess_game.move(position, previous_pos, new_pos)

                        if board[new_pos[0]][new_pos[1]][6:] == "pawn":
                            # I need to consider that the pawn can promote
                            moves_without_captures_or_pawn_moves = 0
                        else:
                            moves_without_captures_or_pawn_moves += 0.5

                        white_can_castle_short, white_can_castle_long, black_can_castle_short, black_can_castle_long = chess_game.legal_castles(position)
                        turn = not turn
                        position = [board, turn, [white_can_castle_short, white_can_castle_long, black_can_castle_short, black_can_castle_long], previous_move]

                        my_current_time = datetime.now()

                        my_legal_moves = chess_game.legal_moves(position)
                        comp_diffrence = datetime.now() - comp_current_time
                        comp_wasted_time += comp_diffrence.total_seconds()
                        comp_time += bonus_time_for_move
                        if chess_game.king_is_in_danger(position):
                            if len(my_legal_moves) == 0:
                                move = move + "#"
                                move_list.append(move)
                                # print("Checkmate!")
                                done = True
                                result = 0
                                break
                            else:
                                # print("Check!")
                                move += "+"
                            # mark king square
                        elif len(my_legal_moves) == 0:
                            print("Stalemate!")
                            result = 0.5
                            done = True
                            break
                        if moves_without_captures_or_pawn_moves == 50:
                            print("Draw by the 50 moves rule!")
                            result = 0.5
                            done = True
                            break
                        print(move, computer_move_value)
                        move_list.append(move)
                    else:
                        x_square, y_square = cordinates_to_square(x, y)
                        first_position = x_square, y_square
                        selected = True
            pygame.display.update()
    if done and not move_list_printed:
        move_list_printed = True
        print(print_pgn(move_list, result))
