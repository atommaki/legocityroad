#!/usr/bin/env python3

from copy import deepcopy
import time
import sys
import argparse

road_types =  set([ '─', '│', '╭', '╮', '╰', '╯', '┼', '┤', '┴', '├', '┬' ])

left_open =   set([ '─', '╮', '╯', '┼', '┤', '┴', '┬' ])
right_open =  set([ '─', '╭', '╰', '┼', '┴', '├', '┬' ])
top_open =    set([ '│', '╰', '╯', '┼', '┤', '┴', '├' ])
bottom_open = set([ '│', '╭', '╮', '┼', '┤', '├', '┬' ])

straights   = set([ '─', '│' ])
turns       = set([ '╭', '╮', '╰', '╯' ])
t_crosses   = set([ '┤', '┴', '├', '┬' ])
xcross      = set([ '┼' ])

updown_mirrored_plate = {
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
                '┼': '┼',
                '*': '*',
                ' ': ' '
             }

rightleft_mirrored_plate = {
                '╯': '╰',
                '╮': '╭',
                '╰': '╯',
                '╭': '╮',
                '├': '┤',
                '┤': '├',
                '┬': '┬',
                '┴': '┴',
                '─': '─',
                '│': '│',
                '┼': '┼',
                '*': '*',
                ' ': ' '
             }

right_rotated_plate = {
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
                '┼': '┼',
                '*': '*',
                ' ': ' '
             }

left_rotated_plate = {
                '╰': '╯',
                '╭': '╰',
                '╮': '╭',
                '╯': '╮',
                '┬': '├',
                '┤': '┬',
                '┴': '┤',
                '├': '┴',
                '│': '─',
                '─': '│',
                '┼': '┼',
                '*': '*',
                ' ': ' '
             }

twice_rotated_plate = {
                '╰': '╮',
                '╭': '╯',
                '╮': '╰',
                '╯': '╭',
                '┬': '┴',
                '┤': '├',
                '┴': '┬',
                '├': '┤',
                '│': '│',
                '─': '─',
                '┼': '┼',
                '*': '*',
                ' ': ' '
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

#n_straight = 4 # ~55sec, 7 solutions
#n_turn     = 6
#n_tcross   = 2
#n_xcross   = 2

#n_straight = 3
#n_turn     = 6
#n_tcross   = 2
#n_xcross   = 2

#n_straight = 2
#n_turn     = 12
#n_tcross   = 0
#n_xcross   = 0

#n_straight = 3
#n_turn     = 4
#n_tcross   = 2
#n_xcross   = 0



rotated_board_time = 0.0
rotated_board_calls = 0
mirrored_board_time = 0.0
mirrored_board_calls = 0
board_hash_time = 0.0
board_hash_calls = 0
extend_time = 0.0
extend_calls = 0


def get_board_size(board):
    board_size_x = len(board)
    if board_size_x == 0:
        return 0, 0
    board_size_y = len(board[0])
    return board_size_x, board_size_y

def get_right_rotated_board(board):
    start = time.time()
    board_size_x, board_size_y = get_board_size(board)
    new_board = []

    for i in range(board_size_y):
        new_board.append([])
        for j in range(board_size_x):
            new_board[i].append(right_rotated_plate[board[board_size_x-1-j][i]])

    global rotated_board_calls
    rotated_board_calls += 1
    global rotated_board_time
    rotated_board_time = rotated_board_time + time.time() - start

    return new_board

def get_left_rotated_board(board):
    start = time.time()
    board_size_x, board_size_y = get_board_size(board)
    new_board = []

    for i in range(board_size_y):
        new_board.append([])
        for j in range(board_size_x):
            new_board[i].append(left_rotated_plate[board[j][board_size_y-1-i]])

    global rotated_board_calls
    rotated_board_calls += 1
    global rotated_board_time
    rotated_board_time = rotated_board_time + time.time() - start

    return new_board

def get_twice_rotated_board(board):
    start = time.time()
    board_size_x, board_size_y = get_board_size(board)
    new_board = []

    for i in range(board_size_x):
        new_board.append([])
        for j in range(board_size_y):
            new_board[i].append(twice_rotated_plate[board[board_size_x-1-i][board_size_y-1-j]])

    global rotated_board_calls
    rotated_board_calls += 1
    global rotated_board_time
    rotated_board_time = rotated_board_time + time.time() - start

    return new_board


def get_updown_mirrored_board(board):
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
            new_board[board_size_x-1-i][j] = updown_mirrored_plate[board[i][j]]

    global mirrored_board_calls
    mirrored_board_calls += 1
    global mirrored_board_time
    mirrored_board_time = mirrored_board_time + time.time() - start

    return new_board

def trim_board(board):
    def first_row(board):
        return [ board[x][0] for x in range(len(board)) ]
    def last_row(board):
        return [ board[x][-1] for x in range(len(board)) ]
    while set(board[0]) == set([' ']):
        board.pop(0)
    while set(board[len(board) -1 ]) == set([' ']):
        board.pop(len(board) -1)
    while set(first_row(board)) == set([' ']):
        for x in range(len(board)):
            board[x].pop(0)
    while set(last_row(board)) == set([' ']):
        for x in range(len(board)):
            board[x].pop(-1)

def str2board(board_str):
    # for testing
    board_size_x = 0
    board_size_y = 0
    board = []
    for line in board_str.splitlines():
        board.append([])
        if len(line) > board_size_y:
            board_size_y = len(line)
        for c in line:
            board[board_size_x].append(c)
        board_size_x += 1
    for x in range(board_size_x):
        for c in range(board_size_y - len(board[x])):
            board[x].append(' ')

    trim_board(board)

    return board


def get_board_hash(board):
    start = time.time()
    board_size_x, board_size_y = get_board_size(board)
    if board_size_x > board_size_y:
        h = hash(tuple(tuple(x) for x in get_right_rotated_board(board)))
    else:
        h = hash(tuple(tuple(x) for x in board))

    global board_hash_calls
    board_hash_calls += 1
    global board_hash_time
    board_hash_time = board_hash_time + time.time() - start

    return h

def get_transformed_board_hashes(board):
    start = time.time()
    hash_set = set()

    board_size_x, board_size_y = get_board_size(board)

    if board_size_x > board_size_y:
        r3_board   = get_left_rotated_board(board)
        m_board    = get_updown_mirrored_board(board)
        mr1_board  = get_right_rotated_board(m_board)
        mr3_board  = get_left_rotated_board(m_board)

        # r1 hash is already stored (see get_board_hash())
        hash_set.add(get_board_hash(r3_board))
        hash_set.add(get_board_hash(mr1_board))
        hash_set.add(get_board_hash(mr3_board))
    elif board_size_x < board_size_y:
        r2_board   = get_twice_rotated_board(board)
        m_board    = get_updown_mirrored_board(board)
        mr2_board  = get_twice_rotated_board(m_board)

        hash_set.add(get_board_hash(r2_board))
        hash_set.add(get_board_hash(m_board))
        hash_set.add(get_board_hash(mr2_board))
    else: # square board
        r1_board   = get_right_rotated_board(board)
        r2_board   = get_twice_rotated_board(board)
        r3_board   = get_left_rotated_board(board)
        m_board    = get_updown_mirrored_board(board)
        mr1_board  = get_right_rotated_board(m_board)
        mr2_board  = get_twice_rotated_board(m_board)
        mr3_board  = get_left_rotated_board(m_board)

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
    board_size_x, board_size_y = get_board_size(board)

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
    board_size_x, board_size_y = get_board_size(board)
    for i in range(board_size_x):
        board[i].insert(0,' ')

    global extend_calls
    extend_calls += 1
    global extend_time
    extend_time = extend_time + time.time() - start

def extend_board_right(board):
    start = time.time()
    board_size_x, board_size_y = get_board_size(board)
    for i in range(board_size_x):
        board[i].append(' ')

    global extend_calls
    extend_calls += 1
    global extend_time
    extend_time = extend_time + time.time() - start

def extend_board_top(board):
    start = time.time()
    board_size_x, board_size_y = get_board_size(board)
    board.insert(0, [])
    for j in range(board_size_y):
        board[0].append(' ')

    global extend_calls
    extend_calls += 1
    global extend_time
    extend_time = extend_time + time.time() - start

def extend_board_bottom(board):
    start = time.time()
    board_size_x, board_size_y = get_board_size(board)
    board.append([])
    for j in range(board_size_y):
        board[board_size_x].append(' ')

    global extend_calls
    extend_calls += 1
    global extend_time
    extend_time = extend_time + time.time() - start


def put_new_item(board, x, y, item, missing):
    board_size_x, board_size_y = get_board_size(board)

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


def solve_board(progress, solutions, already_tried, missing, board, a,b, new_item, roads, used_items, min_used_items):


    put_new_item(board, a, b, new_item, missing)

    if   new_item in straights:  roads['straight'] -= 1
    elif new_item in turns:      roads['turn']     -= 1
    elif new_item in t_crosses:  roads['tcross']   -= 1
    elif new_item in xcross:     roads['xcross']   -= 1

    board_size_x, board_size_y = get_board_size(board)

    #show_board(board)
    #print(missing)

    if len(missing) > roads['straight'] + roads['turn'] + roads['tcross'] + roads['xcross']:
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

        solutions.append(board)
        print(f'\nFound a new solution! Size: {board_size_x}x{board_size_y} ({len(solutions)}, {round(progress[1])}%)')
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

    if roads['straight'] < 1: possible_new_items = possible_new_items - straights
    if roads['turn'] < 1:     possible_new_items = possible_new_items - turns
    if roads['tcross'] < 1:   possible_new_items = possible_new_items - t_crosses
    if roads['xcross'] < 1:   possible_new_items = possible_new_items - xcross

    if len(possible_new_items) == 0:
        # no fitting road piece
        #print('0', end='')
        return False


    possible_new_steps = len(possible_new_items)

    progress_step = (progress[1] - progress[0]) / possible_new_steps

    step = 0
    for new in possible_new_items:

        next_progress = ( progress[0] + progress_step * step,
                          progress[0] + progress_step * (step+1)
                        )

        solve_board(next_progress, solutions, already_tried, deepcopy(missing), deepcopy(board), x, y, new, deepcopy(roads), used_items+1, min_used_items)

        step += 1



def main():
    ### Main

    ### Arguments
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--straight', type=int, action='store', default=0, help='number of straight road plates')
    parser.add_argument('--turn', type=int, action='store', default=0,     help='number of simple turn road plates')
    parser.add_argument('--tcross', type=int, action='store', default=0,   help='number of T (3 way) crossing road plates')
    parser.add_argument('--xcross', type=int, action='store', default=0,   help='number of X (4 way) crossing road plates')

    args = parser.parse_args()
    n_straight = args.straight
    n_turn = args.turn
    n_tcross = args.tcross
    n_xcross = args.xcross

    ### /Arguments

    min_used_items = n_straight + n_turn + n_tcross + n_xcross

    progress = (0, 100)
    solutions = []
    already_tried = set([])
    missing = []

    board = [ [ '*' ] ]

    print(f'n_straight = { n_straight }')
    print(f'n_turn     = { n_turn }')
    print(f'n_tcross   = { n_tcross }')
    print(f'n_xcross   = { n_xcross }')
    print(f'total      = { n_straight + n_turn + n_tcross + n_xcross}')

    roads = { 'straight': n_straight, 'turn': n_turn, 'tcross': n_tcross, 'xcross': n_xcross }


    solve_board(progress, solutions, already_tried, missing, board, 0, 0, '╭', roads, 1, min_used_items)

    print(f'\nNumber of solutions: { len(solutions) }')

    print(f' rotated_board_time    = { rotated_board_time }   calls: {rotated_board_calls}')
    print(f' mirrored_board_time   = { mirrored_board_time }   calls: {mirrored_board_calls}')
    print(f' board_hash_time       = { board_hash_time }   calls: {board_hash_calls}')
    print(f' extend_time           = { extend_time }   calls: {extend_calls}')
    print()
    print(f' size of already_tried: {sys.getsizeof(already_tried) / 1024**2} MB')

if __name__ == "__main__":
    main()

