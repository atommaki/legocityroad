#!/usr/bin/env python3

from copy import deepcopy
import time
import sys

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


#n_straight = 4
#n_turn     = 6
#n_tcross   = 6
#n_xcross   = 4

#n_straight = 4 # ~7h runtime, ~10GB RAM, 781 solution
#n_turn     = 6
#n_tcross   = 6
#n_xcross   = 2

#n_straight = 6
#n_turn     = 4
#n_tcross   = 4
#n_xcross   = 1

#n_straight = 4
#n_turn     = 6
#n_tcross   = 2
#n_xcross   = 2

n_straight = 3
n_turn     = 6
n_tcross   = 2
n_xcross   = 2

#n_straight = 2
#n_turn     = 12
#n_tcross   = 0
#n_xcross   = 0

#n_straight = 3
#n_turn     = 4
#n_tcross   = 2
#n_xcross   = 0


min_used_items = n_straight + n_turn + n_tcross + n_xcross

rotated_board_time = 0.0
rotated_board_calls = 0
mirrored_board_time = 0.0
mirrored_board_calls = 0
board_hash_time = 0.0
board_hash_calls = 0
extend_time = 0.0
extend_calls = 0


def get_board_dimensions(board):
    board_size_x = len(board)
    if board_size_x == 0:
        return 0, 0
    board_size_y = len(board[0])
    return board_size_x, board_size_y

def get_rotated_board(board):
    start = time.time()
    #show_board(board)
    board_size_x, board_size_y = get_board_dimensions(board)
    #print(f'board_size_x, board_size_y = {board_size_x}, {board_size_y}')
    new_board = []

    for i in range(board_size_y):
        new_board.append([])
        for j in range(board_size_x):
            #print(f' j, board_size_x-1-j,  i = {j}, {board_size_x-1-j}, {i}')
            #print(f'board[board_size_x-1-j][i] = {board[board_size_x-1-j][i]}')
            if board[board_size_x-1-j][i] in road_types:
                new_board[i].append(rotated_road[board[board_size_x-1-j][i]])
                #new_board[i][j] = rotated_road[board[board_size_x-1-j][i]]
            else:
                new_board[i].append(board[board_size_x-1-j][i])
                #new_board[i][j] = board[board_size_x-1-j][i]

    global rotated_board_calls
    rotated_board_calls += 1
    global rotated_board_time
    rotated_board_time = rotated_board_time + time.time() - start

    return new_board


def get_mirrored_board(board):
    start = time.time()
    new_board = []
    board_size_x = len(board)
    board_size_y = len(board[0])
    for i in range(board_size_x):
        new_board.append([])
        #for j in range(len(board[i])):
        for j in range(board_size_y):
            new_board[i].append(' ')

    for i in range(board_size_x):
        #for j in range(len(board[i])):
        for j in range(board_size_y):
            if board[i][j] not in road_types or \
               board[i][j] in straights or \
               board[i][j] == xcross:
                    new_board[board_size_x-1-i][j] = board[i][j]
            else:
                new_board[board_size_x-1-i][j] = mirrored_road[board[i][j]]

    global mirrored_board_calls
    mirrored_board_calls += 1
    global mirrored_board_time
    mirrored_board_time = mirrored_board_time + time.time() - start

    return new_board

def get_board_hash(board):
    start = time.time()
    h = hash(tuple(tuple(x) for x in board))

    global board_hash_calls
    board_hash_calls += 1
    global board_hash_time
    board_hash_time = board_hash_time + time.time() - start

    return h

def get_transformed_board_hashes(board):
    start = time.time()
    hash_set = set()

    #board_size_x, board_size_y = get_board_dimensions(board)

    r1_board   = get_rotated_board(board)
    r2_board   = get_rotated_board(r1_board)
    r3_board   = get_rotated_board(r2_board)
    m_board    = get_mirrored_board(board)
    mr1_board  = get_rotated_board(m_board)
    mr2_board  = get_rotated_board(mr1_board)
    mr3_board  = get_rotated_board(mr2_board)

    hash_set.add(get_board_hash(r1_board))
    hash_set.add(get_board_hash(r2_board))
    hash_set.add(get_board_hash(r3_board))
    hash_set.add(get_board_hash(m_board))
    hash_set.add(get_board_hash(mr1_board))
    hash_set.add(get_board_hash(mr2_board))
    hash_set.add(get_board_hash(mr3_board))

    global board_hash_calls
    board_hash_calls += 1
    global board_hash_time
    board_hash_time = board_hash_time + time.time() - start

    return hash_set

def show_board(board):
    board_size_x, board_size_y = get_board_dimensions(board)

    #print('-------------------------------------------')
    #print(board)
    print('-------------------------------------------')
    for i in range(board_size_x):
        for j in range(board_size_y):
            print(board[i][j], end='')
        print()
    print('-------------------------------------------')

def extend_board_left(board):
    start = time.time()
    board_size_x, board_size_y = get_board_dimensions(board)
    for i in range(board_size_x):
        board[i].insert(0,' ')

    global extend_calls
    extend_calls += 1
    global extend_time
    extend_time = extend_time + time.time() - start

def extend_board_right(board):
    start = time.time()
    board_size_x, board_size_y = get_board_dimensions(board)
    for i in range(board_size_x):
        board[i].append(' ')

    global extend_calls
    extend_calls += 1
    global extend_time
    extend_time = extend_time + time.time() - start

def extend_board_top(board):
    start = time.time()
    board_size_x, board_size_y = get_board_dimensions(board)
    board.insert(0, [])
    for j in range(board_size_y):
        board[0].append(' ')

    global extend_calls
    extend_calls += 1
    global extend_time
    extend_time = extend_time + time.time() - start

def extend_board_bottom(board):
    start = time.time()
    board_size_x, board_size_y = get_board_dimensions(board)
    board.append([])
    for j in range(board_size_y):
        board[board_size_x].append(' ')

    global extend_calls
    extend_calls += 1
    global extend_time
    extend_time = extend_time + time.time() - start


def put_new_item(board, x, y, item, missing):
    board_size_x, board_size_y = get_board_dimensions(board)

    board[x][y] = item

    if item in top_open:
        if x == 0:
            extend_board_top(board)
            board_size_x += 1
            x += 1
            for i in range(len(missing)):
                missing[i] = ( missing[i][0]+1, missing[i][1] )
        if board[x-1][y] != '*' and board[x-1][y] not in road_types:
            board[x-1][y] = '*'
            missing.append((x-1,y))

    if item in bottom_open:
        if x == board_size_x -1:
            extend_board_bottom(board)
            board_size_x += 1
        if board[x+1][y] != '*' and board[x+1][y] not in road_types:
            board[x+1][y] = '*'
            missing.append((x+1,y))

    if item in right_open:
        if y == board_size_y -1:
            extend_board_right(board)
            board_size_y += 1
        if board[x][y+1] != '*' and board[x][y+1] not in road_types:
            board[x][y+1] = '*'
            missing.append((x,y+1))

    if item in left_open:
        if y == 0:
            extend_board_left(board)
            board_size_y += 1
            y += 1
            for i in range(len(missing)):
                missing[i] = ( missing[i][0], missing[i][1]+1 )

        if board[x][y-1] != '*' and board[x][y-1] not in road_types:
            board[x][y-1] = '*'
            missing.append((x,y-1))


def solve_board(progress, already_tried, missing, board, a,b, new_item, n_straight, n_turn, n_tcross, n_xcross, used_items, min_used_items):
    put_new_item(board, a, b, new_item, missing)
    board_size_x, board_size_y = get_board_dimensions(board)

    #show_board(board)
    #print(missing)

    if len(missing) > n_straight + n_turn + n_tcross + n_xcross:
        # already too many open ends
        #print('x', end='')
        return False

    board_hash = get_board_hash(board)
    board_all_hashes = set([board_hash]) | get_transformed_board_hashes(board)

    if board_all_hashes & already_tried != set():
        return False

    already_tried.add(board_hash)

    if len(missing) == 0:
        # there are no open ends
        if used_items != min_used_items:
            print('o', end='')
            return False

        global n_solutions
        n_solutions += 1
        print(f'\nFound a new solution! ({n_solutions}, {round(progress[1])}%)')
        show_board(board)
        #print('xxxxxxxxxxxxxx')
        #print(m_board_hash)
        #print('xxxxxxxxxxxxxx')
        return True

    x, y = missing.pop(0)

    #print(f' new item: {new_item} ({a},{b})')
    #print(x,y)
    #print(board[x][y])
    #show_board(board)
    possible_new_items = set(road_types)
    if x > 0 and board[x-1][y] in road_types:
        if board[x-1][y] in bottom_open:
            possible_new_items = possible_new_items & top_open
        else:
            possible_new_items = possible_new_items - top_open
    if x < board_size_x - 1 and board[x+1][y] in road_types:
        if board[x+1][y] in top_open:
            possible_new_items = possible_new_items & bottom_open
        else:
            possible_new_items = possible_new_items - bottom_open
    if y < board_size_y - 1 and board[x][y+1] in road_types:
        if board[x][y+1] in left_open:
            possible_new_items = possible_new_items & right_open
        else:
            possible_new_items = possible_new_items - right_open
    if y > 0 and board[x][y-1] in road_types:
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
        # no fitting road piece
        #print('0', end='')
        return False


    possible_new_steps = len(possible_new_items)

    progress_step = (progress[1] - progress[0]) / possible_new_steps

    step = 0
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

        next_progress = ( progress[0] + progress_step * step,
                          progress[0] + progress_step * (step+1)
                        )

        solve_board(next_progress, already_tried, deepcopy(missing), deepcopy(board), x, y, new, nn_straight, nn_turn, nn_tcross, nn_xcross, used_items+1, min_used_items)

        step += 1

progress = (0, 100)
n_solutions = 0
already_tried = set([])
missing = []

board = [ [ ' ' ] ]

print(f'n_straight = { n_straight }')
print(f'n_turn     = { n_turn }')
print(f'n_tcross   = { n_tcross }')
print(f'n_xcross   = { n_xcross }')
print(f'total      = { n_straight + n_turn + n_tcross + n_xcross}')

solve_board(progress, already_tried, missing, board, 0, 0, '╭', n_straight, n_turn-1, n_tcross, n_xcross, 1, min_used_items)

print(f'\nNumber of solutions: { n_solutions }')
print(f' rotated_board_time    = { rotated_board_time }   calls: {rotated_board_calls}')
print(f' mirrored_board_time   = { mirrored_board_time }   calls: {mirrored_board_calls}')
print(f' board_hash_time       = { board_hash_time }   calls: {board_hash_calls}')
print(f' extend_time           = { extend_time }   calls: {extend_calls}')
print()
print(f' size of already_tried: {sys.getsizeof(already_tried) / 1024**2} MB')

