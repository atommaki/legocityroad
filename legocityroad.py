#!/usr/bin/env python3

from copy import deepcopy
import time

road_types =  set([ '─', '│', '╭', '╮', '╰', '╯', '┼', '┤', '┴', '├', '┬' ])

left_open =   set([ '─', '╮', '╯', '┼', '┤', '┴', '┬' ])
right_open =  set([ '─', '╭', '╰', '┼', '┴', '├', '┬' ])
top_open =    set([ '│', '╰', '╯', '┼', '┤', '┴', '├' ])
bottom_open = set([ '│', '╭', '╮', '┼', '┤', '├', '┬' ])

straights   = set([ '─', '│' ])
turns       = set([ '╭', '╮', '╰', '╯' ])
t_crosses   = set([ '┤', '┴', '├', '┬' ])
xcross      = '┼'

mirrored_road = {
                '╯': '╮',
                '╮': '╯',
                '╰': '╭',
                '╭': '╰',
                '├': '├',
                '┤': '┤',
                '┬': '┴',
                '┴': '┬',
                '─': '─',
                '│': '│',
                '┼': '┼'
             }

rotated_road = {
                '╯': '╰',
                '╰': '╭',
                '╭': '╮',
                '╮': '╯',
                '├': '┬',
                '┬': '┤',
                '┤': '┴',
                '┴': '├',
                '─': '│',
                '│': '─',
                '┼': '┼'
             }


n_straight = 4
n_turn     = 6
n_tcross   = 6
n_xcross   = 4

n_straight = 4
n_turn     = 6
n_tcross   = 2
n_xcross   = 2

n_straight = 6
n_turn     = 4
n_tcross   = 4
n_xcross   = 1

#n_straight = 2
#n_turn     = 8
#n_tcross   = 0
#n_xcross   = 0


min_used_items = n_straight + n_turn + n_tcross + n_xcross

rotated_board_time = 0.0
mirrored_board_time = 0.0
normal_board_time = 0.0
board_normal_str_time = 0.0
extend_left_time = 0.0
extend_right_time = 0.0
n_missing_time = 0.0
first_missing_time = 0.0

def get_rotated_board(board):
    start = time.time()
    board_size = len(board)
    new_board = []
    for i in range(board_size):
        new_board.append([])
        #for j in range(len(board[i])):
        for j in range(board_size):
            new_board[i].append(' ')

    for i in range(board_size):
        #for j in range(len(board[i])):
        for j in range(board_size):
            if board[i][j] in road_types:
                new_board[j][board_size-1-i] = rotated_road[board[i][j]]
            else:
                new_board[j][board_size-1-i] = board[i][j]

    global rotated_board_time
    rotated_board_time = rotated_board_time + time.time() - start

    return new_board


def get_mirrored_board(board):
    start = time.time()
    new_board = []
    board_size = len(board)
    for i in range(board_size):
        new_board.append([])
        #for j in range(len(board[i])):
        for j in range(board_size):
            new_board[i].append(' ')

    for i in range(board_size):
        #for j in range(len(board[i])):
        for j in range(board_size):
            if board[i][j] not in road_types or \
               board[i][j] in straights or \
               board[i][j] == xcross:
                    new_board[board_size-1-i][j] = board[i][j]
            else:
                new_board[board_size-1-i][j] = mirrored_road[board[i][j]]

    global mirrored_board_time
    mirrored_board_time = mirrored_board_time + time.time() - start

    return new_board

def get_normal_board(board):
    start = time.time()
    board_size = len(board)
    for i in range(board_size):
        if set(board[i]) != set([' ']):
            first_line = i
            break
    for i in reversed(range(board_size)):
        if set(board[i]) != set([' ']):
            last_line = i
            break
    for j in range(board_size):
        row = [ board[i][j] for i in range(board_size) ]
        if set(row) != set([' ']):
            first_row = j
            break
    for j in reversed(range(board_size)):
        row = [ board[i][j] for i in range(board_size) ]
        if set(row) != set([' ']):
            last_row = j
            break

    normal_board = []
    x = 0
    for i in range(first_line, last_line+1):
        normal_board.append([])
        for j in range(first_row, last_row+1):
            normal_board[x].append(board[i][j])
        x += 1

    global normal_board_time
    normal_board_time = normal_board_time + time.time() - start

    return normal_board

def get_board_normal_str(board):
    normal_board = get_normal_board(board)
    start = time.time()
    normal_board_str = ""

    for i in range(len(normal_board)):
        normal_board_str += ''.join(normal_board[i]) + '\n'

    global board_normal_str_time
    board_normal_str_time = board_normal_str_time + time.time() - start

    return normal_board_str

def show_board(board):
    normal_board = get_normal_board(board)
    if normal_board == []:
        print('Empty board!')
        return

    print('-------------------------------------------')
    for i in range(len(normal_board)):
        for j in range(len(normal_board[i])):
            print(normal_board[i][j], end='')
        print()
    print('-------------------------------------------')

def extend_board_left_top(board, n):
    start = time.time()
    for x in range(n):
        board_size = len(board)
        board.insert(0, [])
        for i in range(board_size):
            board[0].append(' ')
        for i in range(board_size + 1):
            board[i].insert(0,' ')

    global extend_left_time
    extend_left_time = extend_left_time + time.time() - start


def extend_board_rigth_bottom(board, n):
    start = time.time()
    for x in range(n):
        board_size = len(board)
        board.append([])
        for i in range(board_size):
            board[board_size].append(' ')
        for i in range(board_size + 1):
            board[i].append(' ')

    global extend_right_time
    extend_right_time = extend_right_time + time.time() - start


def put_new_item(board, x, y, item, missing):
    current_board_size = len(board)
    if x < 2 or y < 2:
        extend_board_left_top(board, 2)
        current_board_size += 2
        for i in range(len(missing)):
            missing[i] = ( missing[i][0]+2, missing[i][1]+2 )
        x += 2
        y += 2
    if x > current_board_size - 3 or y > current_board_size - 3:
        extend_board_rigth_bottom(board, 2)
        current_board_size += 2

    board[x][y] = item

    if board[x+1][y] != '*' and board[x+1][y] not in road_types and item in bottom_open:
        board[x+1][y] = '*'
        missing.append((x+1,y))

    if board[x-1][y] != '*' and board[x-1][y] not in road_types and item in top_open:
        board[x-1][y] = '*'
        missing.append((x-1,y))

    if board[x][y+1] != '*' and board[x][y+1] not in road_types and item in right_open:
        board[x][y+1] = '*'
        missing.append((x,y+1))

    if board[x][y-1] != '*' and board[x][y-1] not in road_types and item in left_open:
        board[x][y-1] = '*'
        missing.append((x,y-1))


#def get_n_of_missing(board):
#    start = time.time()
#
#    missing = 0
#    board_size = len(board)
#    for i in range(board_size):
#        for j in range(board_size):
#            if  board[i][j] == '*':
#                missing += 1
#
#    global n_missing_time
#    n_missing_time = n_missing_time + time.time() - start
#
#    return missing
#
#
#def find_first_missing(board):
#    start = time.time()
#    global first_missing_time
#
#    board_size = len(board)
#    for i in range(board_size):
#        for j in range(board_size):
#            if  board[i][j] == '*':
#                first_missing_time = first_missing_time + time.time() - start
#                return i,j
#
#    first_missing_time = first_missing_time + time.time() - start
#
#    return None, None
#


def solve_board(already_tried, missing, board, a,b, new_item, n_straight, n_turn, n_tcross, n_xcross, used_items, min_used_items):
    put_new_item(board, a, b, new_item, missing)

    #show_board(board)
    #print(missing)

    if len(missing) > n_straight + n_turn + n_tcross + n_xcross:
        # already too many open ends
        #print('x', end='')
        return False

    normal_board_str = get_board_normal_str(board)
    if normal_board_str in already_tried:
        return False

    r1_board  = get_rotated_board(board)
    r2_board  = get_rotated_board(r1_board)
    r3_board  = get_rotated_board(r2_board)
    m_board   = get_mirrored_board(board)
    mr1_board = get_rotated_board(m_board)
    mr2_board = get_rotated_board(mr1_board)
    mr3_board = get_rotated_board(mr2_board)

    normal_r1_board_srt   = get_board_normal_str(r1_board)
    normal_r2_board_srt   = get_board_normal_str(r2_board)
    normal_r3_board_srt   = get_board_normal_str(r3_board)
    normal_m_board_srt    = get_board_normal_str(m_board)
    normal_mr1_board_srt  = get_board_normal_str(mr1_board)
    normal_mr2_board_srt  = get_board_normal_str(mr2_board)
    normal_mr3_board_srt  = get_board_normal_str(mr3_board)

    already_tried.add(normal_board_str)
    already_tried.add(normal_r1_board_srt)
    already_tried.add(normal_r2_board_srt)
    already_tried.add(normal_r3_board_srt)
    already_tried.add(normal_m_board_srt)
    already_tried.add(normal_mr1_board_srt)
    already_tried.add(normal_mr2_board_srt)
    already_tried.add(normal_mr3_board_srt)

    if len(missing) == 0:
        # there are no open ends
        if used_items != min_used_items:
            print('o', end='')
            return False

        print('\nFound a new solution!')
        global n_solutions
        n_solutions += 1
        show_board(board)
        #print('xxxxxxxxxxxxxx')
        #print(normal_m_board_str)
        #print('xxxxxxxxxxxxxx')
        return True

    x, y = missing.pop(0)

    #print(f' new item: {new_item} ({a},{b})')
    #print(x,y)
    #print(board[x][y])
    #show_board(board)
    possible_new_items = set(road_types)
    if board[x-1][y] in road_types:
        if board[x-1][y] in bottom_open:
            possible_new_items = possible_new_items & top_open
        else:
            possible_new_items = possible_new_items - top_open
    if board[x+1][y] in road_types:
        if board[x+1][y] in top_open:
            possible_new_items = possible_new_items & bottom_open
        else:
            possible_new_items = possible_new_items - bottom_open
    if board[x][y+1] in road_types:
        if board[x][y+1] in left_open:
            possible_new_items = possible_new_items & right_open
        else:
            possible_new_items = possible_new_items - right_open
    if board[x][y-1] in road_types:
        if board[x][y-1] in right_open:
            possible_new_items = possible_new_items & left_open
        else:
            possible_new_items = possible_new_items - left_open

    if n_straight == 0:
        possible_new_items = possible_new_items - straights
    if n_turn == 0:
        possible_new_items = possible_new_items - turns
    if n_tcross == 0:
        possible_new_items = possible_new_items - t_crosses
    if n_xcross == 0:
        possible_new_items = possible_new_items - set([xcross])

    if len(possible_new_items) == 0:
        #print('0', end='')
        return False


    for new in possible_new_items:
        nn_straight = n_straight
        nn_turn     = n_turn
        nn_tcross   = n_tcross
        nn_xcross   = n_xcross

        if new in straights:
            nn_straight -= 1
        elif new in turns:
            nn_turn -= 1
        elif new in t_crosses:
            nn_tcross -= 1
        elif new == xcross:
            nn_xcross -= 1

        solve_board(already_tried, deepcopy(missing), deepcopy(board), x, y, new, nn_straight, nn_turn, nn_tcross, nn_xcross, used_items+1, min_used_items)

n_solutions = 0
already_tried = set([])
missing = []

board = [ [ ' ' ] ]

print(f'n_straight = { n_straight }')
print(f'n_turn     = { n_turn }')
print(f'n_tcross   = { n_tcross }')
print(f'n_xcross   = { n_xcross }')
print(f'total      = { n_straight + n_turn + n_tcross + n_xcross}')

solve_board(already_tried, missing, board, 0, 0, '╭', n_straight, n_turn-1, n_tcross, n_xcross, 1, min_used_items)

print(f'\nNumber of solutions: { n_solutions }')
print(f' rotated_board_time    = { rotated_board_time }')
print(f' mirrored_board_time   = { mirrored_board_time }')
print(f' normal_board_time     = { normal_board_time }')
print(f' board_normal_str_time = { board_normal_str_time }')
print(f' extend_left_time      = { extend_left_time }')
print(f' extend_right_time     = { extend_right_time }')
print(f' n_missing_time        = { n_missing_time }')
print(f' first_missing_time    = { first_missing_time }')


