#!/usr/bin/env python3

from copy import deepcopy
import time
import os
import sys
import signal
import argparse
from random import randrange
import multiprocessing
from multiprocessing import Process, Manager, Semaphore
import logging

### Road types, mirrored and rotated plates {{{
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

weight =  { '─': 3,  '│': 3,  '╭': 1,  '╮': 1,  '╰': 1, '╯': 1,
            '┼': 24, '┤': 8,  '┴': 8,  '├': 8,  '┬': 8, ' ': 0,
            '*': 0 }
### }}}

rotated_board_time = 0.0
rotated_board_calls = 0
mirrored_board_time = 0.0
mirrored_board_calls = 0
board_hash_time = 0.0
board_hash_calls = 0
extend_time = 0.0
extend_calls = 0

def printlog(s = ''): # {{{
    logging.debug(s)
    print(s)
# }}}
def get_board_size(board): # {{{
    board_size_x = len(board)
    if board_size_x == 0:
        return 0, 0
    board_size_y = len(board[0])
    return board_size_x, board_size_y
# }}}
def get_right_rotated_board(board): # {{{
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
# }}}
def get_left_rotated_board(board): # {{{
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
# }}}
def get_twice_rotated_board(board): # {{{
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
# }}}
def get_updown_mirrored_board(board): # {{{
    start = time.time()
    new_board = []
    board_size_x = len(board)
    board_size_y = len(board[0])
    for i in range(board_size_x):
        new_board.append([])
        for j in range(board_size_y):
            new_board[i].append(' ')

    for i in range(board_size_x):
        for j in range(board_size_y):
            new_board[board_size_x-1-i][j] = updown_mirrored_plate[board[i][j]]

    global mirrored_board_calls
    mirrored_board_calls += 1
    global mirrored_board_time
    mirrored_board_time = mirrored_board_time + time.time() - start

    return new_board
# }}}
def get_rightleft_mirrored_board(board): # {{{
    start = time.time()
    new_board = []
    board_size_x = len(board)
    board_size_y = len(board[0])
    for i in range(board_size_x):
        new_board.append([])
        for j in range(board_size_y):
            new_board[i].append(' ')

    for i in range(board_size_x):
        for j in range(board_size_y):
            new_board[i][board_size_y-1-j] = rightleft_mirrored_plate[board[i][j]]

    global mirrored_board_calls
    mirrored_board_calls += 1
    global mirrored_board_time
    mirrored_board_time = mirrored_board_time + time.time() - start

    return new_board
# }}}
def trim_board(board,missing): # {{{
    if len(board) == 0:
        return

    def first_row(board):
        return [ board[x][0] for x in range(len(board)) ]
    def last_row(board):
        return [ board[x][-1] for x in range(len(board)) ]

    missing_size = len(missing)
    while len(board) > 1 and set(board[0]) == set([' ']):
        board.pop(0)
        for i in range(missing_size):
            missing[i] = ( missing[i][0]-1, missing[i][1] )

    while len(board) > 1 and set(board[len(board) -1 ]) == set([' ']):
        board.pop(len(board) -1)

    while len(board[0]) > 1 and set(first_row(board)) == set([' ']):
        for x in range(len(board)):
            board[x].pop(0)
        for i in range(missing_size):
            missing[i] = ( missing[i][0], missing[i][1]-1 )

    while len(board[0]) > 1 and set(last_row(board)) == set([' ']):
        for x in range(len(board)):
            board[x].pop(-1)
# }}}
def str2board(board_str): # {{{
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

    trim_board(board, [])

    return board
# }}}
def get_board_hash(board): # {{{
    start = time.time()
    board_size_x, board_size_y = get_board_size(board)
    if board_size_x > board_size_y:
        h = hash(tuple(tuple(x) for x in get_right_rotated_board(board)))
        #h = str(get_right_rotated_board(board))
    else:
        h = hash(tuple(tuple(x) for x in board))
        #h = str(board)

    global board_hash_calls
    board_hash_calls += 1
    global board_hash_time
    board_hash_time = board_hash_time + time.time() - start

    return h
# }}}
def have_been_there(board, been_there): # {{{
    start = time.time()
    def ret(retval):
        global board_hash_calls
        board_hash_calls += 1
        global board_hash_time
        board_hash_time = board_hash_time + time.time() - start
        return retval
    def check_hash(h):
        if h in been_there:
            return True
        return False

    board_hash = get_board_hash(board)
    if check_hash(board_hash): return True

    board_size_x, board_size_y = get_board_size(board)

    if board_size_x > board_size_y:
        r3_board   = get_left_rotated_board(board)
        if check_hash(get_board_hash(r3_board)): return True

        m_board    = get_updown_mirrored_board(board)
        if check_hash(get_board_hash(m_board)): return True

        mr1_board  = get_right_rotated_board(m_board)
        if check_hash(get_board_hash(mr1_board)): return True

        mr3_board  = get_left_rotated_board(m_board)
        if check_hash(get_board_hash(mr3_board)): return True

    elif board_size_x < board_size_y:
        r2_board   = get_twice_rotated_board(board)
        if check_hash(get_board_hash(r2_board)): return True

        m_board    = get_updown_mirrored_board(board)
        if check_hash(get_board_hash(m_board)): return True

        mr2_board  = get_twice_rotated_board(m_board)
        if check_hash(get_board_hash(mr2_board)): return True

    else: # square board
        r1_board   = get_right_rotated_board(board)
        if check_hash(get_board_hash(r1_board)): return True

        r2_board   = get_twice_rotated_board(board)
        if check_hash(get_board_hash(r2_board)): return True

        r3_board   = get_left_rotated_board(board)
        if check_hash(get_board_hash(r3_board)): return True

        m_board    = get_updown_mirrored_board(board)
        if check_hash(get_board_hash(m_board)): return True

        mr1_board  = get_right_rotated_board(m_board)
        if check_hash(get_board_hash(mr1_board)): return True

        mr2_board  = get_twice_rotated_board(m_board)
        if check_hash(get_board_hash(mr2_board)): return True

        mr3_board  = get_left_rotated_board(m_board)
        if check_hash(get_board_hash(mr3_board)): return True

    #been_there.add(board_hash)
    been_there[board_hash] = None

    ret(False)
# }}}
def show_board(board): # {{{
    board_size_x, board_size_y = get_board_size(board)

    #print('-------------------------------------------')
    #print(board)
    for i in range(board_size_x):
        for j in range(board_size_y):
            print(board[i][j], end='')
        print()
# }}}
def get_center_of_mass(board): # {{{
    # artificial center of mass to help rotating and ordering
    board_size_x, board_size_y = get_board_size(board)
    x_center = 0
    y_center = 0
    total_weight = 0
    for x in range(board_size_x):
        for y in range(board_size_y):
            x_center = x_center + (x+1) * weight[board[x][y]]
            y_center = y_center + (y+1) * weight[board[x][y]]
            total_weight = total_weight + weight[board[x][y]]
    x_center = x_center / total_weight - 0.5
    y_center = y_center / total_weight - 0.5

    return x_center, y_center, total_weight
# }}}
def rotate_and_order(board_list): # {{{
    # tries to make some kind of order, hoping the similar boards will be
    # next to eacho other (also rotates boards into "landscape mode")
    board_order = []
    for i in range(len(board_list)):
        board_size_x, board_size_y = get_board_size(board_list[i])
        if board_size_x > board_size_y:
            board_list[i] = get_right_rotated_board(board_list[i])
            board_size_x, board_size_y = get_board_size(board_list[i])
        x_cg, y_cg, w = get_center_of_mass(board_list[i])
        if x_cg < board_size_x / 2: # move CG down
            #print('updown (x)')
            board_list[i] = get_updown_mirrored_board(board_list[i])
            x_cg = board_size_x - x_cg
        if y_cg < board_size_y / 2: # move CG right
            #print('rightleft (y)')
            board_list[i] = get_rightleft_mirrored_board(board_list[i])
            y_cg = board_size_y - y_cg
        board_order.append(board_size_x * 10**9 + board_size_y * 10**7 +
                           round(x_cg,3) * 10**5 + round(y_cg,3))

    board_list[:] = [ b for _,b in sorted(zip(board_order,board_list)) ]
# }}}
def show_multiple_boards(board_list): # {{{
    print_board_list = deepcopy(board_list)
    try:
        term_y, term_x = os.get_terminal_size()
    except OSError:
        term_y = 100
    space_bw_items = 3
    rotate_and_order(print_board_list)
    while len(print_board_list) > 0:
        current_print = []
        width = 0
        max_x = 0
        while len(print_board_list) > 0:
            board_size_x, board_size_y = get_board_size(print_board_list[0])
            if board_size_y + width + space_bw_items < term_y:
                current_print.append(print_board_list.pop(0))
                width += space_bw_items + board_size_y
                if board_size_x > max_x:
                    max_x = board_size_x
            else:
                break
        for b in current_print:
            board_size_x, board_size_y = get_board_size(b)
            sizestr = f'{board_size_x}x{board_size_y}'
            print(sizestr, end='')
            missing_space = board_size_y + space_bw_items - len(sizestr)
            if missing_space > 0:
                print(' ' * missing_space, end='')
        print()
        for x in range(max_x):
            for b in current_print:
                b_x, b_y = get_board_size(b)
                if x < b_x:
                    print(''.join(b[x]), end='')
                else:
                    print(' ' * b_y, end='')
                print(' ' * space_bw_items, end='')
            print()
# }}}
def extend_board_left(board): # {{{
    start = time.time()
    board_size_x, board_size_y = get_board_size(board)
    for i in range(board_size_x):
        board[i].insert(0,' ')

    global extend_calls
    extend_calls += 1
    global extend_time
    extend_time = extend_time + time.time() - start
# }}}
def extend_board_right(board): # {{{
    start = time.time()
    board_size_x, board_size_y = get_board_size(board)
    for i in range(board_size_x):
        board[i].append(' ')

    global extend_calls
    extend_calls += 1
    global extend_time
    extend_time = extend_time + time.time() - start
# }}}
def extend_board_top(board): # {{{
    start = time.time()
    board_size_x, board_size_y = get_board_size(board)
    board.insert(0, [])
    for j in range(board_size_y):
        board[0].append(' ')

    global extend_calls
    extend_calls += 1
    global extend_time
    extend_time = extend_time + time.time() - start
# }}}
def extend_board_bottom(board): #{{{
    start = time.time()
    board_size_x, board_size_y = get_board_size(board)
    board.append([])
    for j in range(board_size_y):
        board[board_size_x].append(' ')

    global extend_calls
    extend_calls += 1
    global extend_time
    extend_time = extend_time + time.time() - start
# }}}
def put_new_item(board, x, y, item, missing, roads): # {{{
    board_size_x, board_size_y = get_board_size(board)

    if   item in straights:  roads['straight'] -= 1
    elif item in turns:      roads['turn']     -= 1
    elif item in t_crosses:  roads['tcross']   -= 1
    elif item in xcross:     roads['xcross']   -= 1


    missing.remove((x,y))

    board[x][y] = item
    new_missing = []

    if item in top_open:
        if x == 0:
            extend_board_top(board)
            board_size_x += 1
            x += 1
            for i in range(len(missing)):
                missing[i] = ( missing[i][0]+1, missing[i][1] )
        if board[x-1][y] != '*' and board[x-1][y] not in road_types:
            board[x-1][y] = '*'
            new_missing.append((x-1,y))

    if item in bottom_open:
        if x == board_size_x -1:
            extend_board_bottom(board)
            board_size_x += 1
        if board[x+1][y] != '*' and board[x+1][y] not in road_types:
            board[x+1][y] = '*'
            new_missing.append((x+1,y))

    if item in right_open:
        if y == board_size_y -1:
            extend_board_right(board)
            board_size_y += 1
        if board[x][y+1] != '*' and board[x][y+1] not in road_types:
            board[x][y+1] = '*'
            new_missing.append((x,y+1))

    if item in left_open:
        if y == 0:
            extend_board_left(board)
            board_size_y += 1
            y += 1
            for i in range(len(missing)):
                missing[i] = ( missing[i][0], missing[i][1]+1 )

            for i in range(len(new_missing)):
                new_missing[i] = ( new_missing[i][0], new_missing[i][1]+1 )

        if board[x][y-1] != '*' and board[x][y-1] not in road_types:
            board[x][y-1] = '*'
            new_missing.append((x,y-1))

    missing.extend(new_missing)
    return x, y, new_missing
# }}}
def remove_item(board, x, y, item_caused_missing, missing, roads): # {{{
    if   board[x][y] in straights:  roads['straight'] += 1
    elif board[x][y] in turns:      roads['turn']     += 1
    elif board[x][y] in t_crosses:  roads['tcross']   += 1
    elif board[x][y] in xcross:     roads['xcross']   += 1

    board[x][y] = '*'
    for mx, my in item_caused_missing:
        board[mx][my] = ' '
        missing.remove((mx,my))
    missing.insert(0,(x,y))
    trim_board(board, missing)
# }}}
def is_almost_rectangle_board(board): # {{{
    # True when the board corners are roads (or '*'), but allows holes and
    # bays on the edges
    board_size_x, board_size_y = get_board_size(board)
    n_space = 0
    for c in [ board[0][0],
               board[0][board_size_y-1],
               board[board_size_x-1][0],
               board[board_size_x-1][board_size_y-1] ]:
        if c == ' ':
            n_space += 1
    if n_space == 0:
        return True
    else:
        return False
# }}}
def is_rectangle_board(board): # {{{
    # True when the board edges are roads (or '*'), but allows holes inside
    board_size_x, board_size_y = get_board_size(board)
    for x in range(board_size_x):
        if board[x][0] == ' ' or  board[x][board_size_y-1] == ' ':
            return False
    for y in range(board_size_y):
        if board[0][y] == ' ' or  board[board_size_x-1][y] == ' ':
            return False

    return True
# }}}
def is_hole(board,x,y): # {{{
    # True when the x,y place is part of a hole
    board_size_x, board_size_y = get_board_size(board)
    bubble_inner = set()
    bubble_edge = set([(x,y)])
    out = False
    while len(bubble_edge) > 0 and not out:
        next_bubble_edge = set()
        for a,b in list(bubble_edge):
            if a == 0 or a == board_size_x-1 or b == 0 or b == board_size_y-1:
                out = True
                break
            if board[a][b+1] == ' ': next_bubble_edge.add((a,b+1))
            if board[a][b-1] == ' ': next_bubble_edge.add((a,b-1))
            if board[a+1][b] == ' ': next_bubble_edge.add((a+1,b))
            if board[a-1][b] == ' ': next_bubble_edge.add((a-1,b))
        bubble_edge = next_bubble_edge - bubble_inner
        bubble_inner = next_bubble_edge | bubble_inner
    return not out
# }}}
def is_hole_on_board(board): # {{{
    # True when there is a hole on the board (hole is completely 
    # surrounded by roads (or *))
    board_size_x, board_size_y = get_board_size(board)
    for x in range(1, board_size_x - 1):
        for y in range(1, board_size_y - 1):
            if board[x][y] == ' ' and is_hole(board,x,y):
                return True
    return False
# }}}
def is_perfect_board(board): # {{{
    # True when the boaard is fully filled by roads (or '*')
    # (same as rectangle with no holes)
    board_size_x, board_size_y = get_board_size(board)
    for x in range(board_size_x):
        for y in range(board_size_y):
            if board[x][y] == ' ':
                return False
    return True
# }}}
def is_symmetric_board(board): # {{{

    board_size_x, board_size_y = get_board_size(board)

    if board_size_x != board_size_y:
        #r2
        if get_twice_rotated_board(board)  == board: return True

        m_board = get_updown_mirrored_board(board)
        if m_board == board: return True

        #mr2
        if get_twice_rotated_board(m_board) == board: return True

    else: # square board
        #r1
        if get_right_rotated_board(board) == board: return True

        #r2
        if get_twice_rotated_board(board) == board: return True

        #r3
        if get_left_rotated_board(board) == board: return True

        m_board = get_updown_mirrored_board(board)
        if m_board == board: return True

        #mr1
        if get_right_rotated_board(m_board) == board: return True

        #mr2
        if get_twice_rotated_board(m_board) == board: return True

        #mr3
        if get_left_rotated_board(m_board) == board: return True

    return False
# }}}
def solve_board(progress, solutions, solution_hashes, been_there, missing, board, a,b, new_item, roads, used_items, min_used_items, cache_percent, use_mp, sema, sema_release): # {{{

    real_a, real_b, new_missing = put_new_item(board, a, b, new_item, missing, roads)

    board_size_x, board_size_y = get_board_size(board)

    logging.debug(f'solve_board called: level = {used_items}, new_item: {new_item} ({a},{b})')

    all_roads_left = roads['straight'] + roads['turn'] + roads['tcross'] + roads['xcross']

    if len(missing) > all_roads_left:
        # already too many open ends
        remove_item(board, real_a, real_b, new_missing, missing, roads)
        logging.debug('END. More missing place than free roads.')
        if sema_release: sema.release()
        return False

    if cache_percent == 100 or \
       cache_percent != 0 and cache_percent > randrange(0,100):
        if have_been_there(board, been_there):
            remove_item(board, real_a, real_b, new_missing, missing, roads)
            if sema_release: sema.release()
            return False

    if len(missing) == 0:
        # there are no open ends

        if used_items != min_used_items:
            remove_item(board, real_a, real_b, new_missing, missing, roads)
            logging.debug(f'END. Not a good solution, not enough unused roads (used_items={used_items}).')
            if sema_release: sema.release()
            return False

        if not have_been_there(board, solution_hashes):
            solutions.append(board)
            logging.debug(f'END. Found a new solution! board hash: {get_board_hash(board)}  ({len(solutions)})')
            print(f'\nFound a new solution! Size: {board_size_x}x{board_size_y} ({len(solutions)})')
            show_board(board)
        remove_item(board, real_a, real_b, new_missing, missing, roads)
        if sema_release: sema.release()
        return True

    x, y = missing[0]
    logging.debug(f'picked up x,y={x},{y} from the list: {missing}')

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
        logging.debug(f'END. No fitting road piece for {x},{y}.')
        remove_item(board, real_a, real_b, new_missing, missing, roads)
        if sema_release: sema.release()
        return False


    possible_new_steps = len(possible_new_items)
    logging.debug(f'{possible_new_steps} possible road piece on {x},{y}')

    progress_step = (progress[1] - progress[0]) / possible_new_steps

    step = 0
    mp_proc = []

    for new in possible_new_items:
        next_progress = ( progress[0] + progress_step * step,
                          progress[0] + progress_step * (step+1)
                        )

        if use_mp and used_items < 5 and sema.acquire(block = False):
            logging.info('Forking a new process.')
            mp_proc.append(Process(target = solve_board,
                                   args = (next_progress, solutions, solution_hashes, been_there, missing, board, x, y, new, deepcopy(roads), used_items+1, min_used_items, cache_percent, use_mp, sema, True )))
            mp_proc[-1].start()
        else:
            solve_board(next_progress, solutions, solution_hashes, been_there, missing, board, x, y, new, roads, used_items+1, min_used_items, cache_percent, use_mp, sema, False)

        step += 1

    remove_item(board, real_a, real_b, new_missing, missing, roads)

    if sema_release:
        sema.release()
        logging.info('Fork ends here.')
    for mpp in mp_proc:
        mpp.join()
# }}}
def solve_board_wrapper(roads, min_used_items, cache_percent, use_mp): # {{{
    mpman = Manager()
    solutions = mpman.list()


    progress = (0, 100)
    solution_hashes = mpman.dict()
    #been_there = set()
    #been_there = {}
    been_there = mpman.dict()
    missing = [ (0,0) ]

    board = [ [ '*' ] ]

    sema = Semaphore( multiprocessing.cpu_count())

    solve_board(progress, solutions, solution_hashes, been_there, missing, board, 0, 0, '╭', roads, 1, min_used_items, cache_percent, use_mp, sema, False)

    return solutions
# }}}
def print_solution_report(solutions): # {{{
    if len(solutions) == 0:
        return
    print(f' ------ All solutions ({len(solutions)}) ------')
    solutions = deepcopy(solutions)
    def printoutboards(name, boards):
        if len(boards) > 0:
            print(f' --- {name} ({len(boards)}) ---')
            show_multiple_boards(list(boards))
            print()
    def remove_items(list1, list2):
        for i2 in list2:
            if i2 in list1:
                list1.remove(i2)


    sol_perfect = [ b for b in solutions if is_perfect_board(b) ]
    remove_items(solutions, sol_perfect)
    printoutboards('Perfect (fully filled rectangle, no holes)', sol_perfect)

    sol_rectangle = [ b for b in solutions if is_rectangle_board(b) ]
    remove_items(solutions, sol_rectangle)
    printoutboards('Rectangle with hole(s)', sol_rectangle)

    sol_almost_rectangle = [ b for b in solutions if is_almost_rectangle_board(b) ]
    remove_items(solutions, sol_almost_rectangle)
    sol_almost_rectangle_no_holes = [ b for b in sol_almost_rectangle if not is_hole_on_board(b) ]
    remove_items(sol_almost_rectangle, sol_almost_rectangle_no_holes)
    printoutboards('Almost rectangle (rectangle with bays) without hole(s)', sol_almost_rectangle_no_holes)
    printoutboards('Almost rectangle with hole(s)', sol_almost_rectangle)

    sol_symm = [ b for b in solutions if is_symmetric_board(b) ]
    remove_items(solutions, sol_symm)
    sol_symm_no_holes = [ b for b in sol_symm if not is_hole_on_board(b) ]
    remove_items(sol_symm, sol_symm_no_holes)
    printoutboards('Non rectangle, symmetric shapes without hole(s)', sol_symm_no_holes)
    printoutboards('Non rectangle, symmetric shapes with hole(s)', sol_symm)

    sol_irreg_no_holes = [ b for b in solutions if not is_hole_on_board(b) ]
    remove_items(solutions, sol_irreg_no_holes)
    printoutboards('Irregular shapes without holes', sol_irreg_no_holes)

    printoutboards('Irregular shapes with holes', solutions)
# }}}
def remove_duplicated_boards(board_list): #{{{
    board_hash_set = dict()
    new_list = []
    for b in board_list:
        if not have_been_there(b, board_hash_set):
            new_list.append(b)
    return new_list
#}}}

def main(): # {{{
    ### {{{ Arguments
    parser = argparse.ArgumentParser(description='Gives you all the combinations of closed roads (meaning: no open ends) what you can build from your Lego City road plates. Use the options bellow to tell how many boards you have.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--straight', type=int, action='store', default=0, help='number of straight road plates')
    parser.add_argument('--turn', type=int, action='store', default=0,     help='number of simple turn road plates')
    parser.add_argument('--tcross', type=int, action='store', default=0,   help='number of T (3 way) crossing road plates')
    parser.add_argument('--xcross', type=int, action='store', default=0,   help='number of X (4 way) crossing road plates')

    parser.add_argument('--cache-percent', type=int, action='store', default=0,   help='percentage of stored already known path. Doesn\'t work very well in multiprocessing (which is enabled by default), but reduce search time for single process runs (high cache -> VERY high memory usage, low cache -> slower runs), see the --no-mp option')

    parser.add_argument('--no-mp', action='store_true', help='disable multiprocessing')
    parser.add_argument('--log', action='store_true', help='creates a log file legocityroad.log (useful for debugging, significantly slower runs). ')

    args = parser.parse_args()
    n_straight = args.straight
    n_turn = args.turn
    n_tcross = args.tcross
    n_xcross = args.xcross
    use_mp = not args.no_mp

    cache_percent = args.cache_percent

    if args.log:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.CRITICAL # no logging

    ### }}} Arguments 
    ### {{{ Logging
    logging.basicConfig(
            filename = os.path.join(os.path.dirname(__file__),'legocityroad.log'),
            filemode = 'a',
            format   = '%(asctime)s,%(msecs)d %(process)d %(name)s %(levelname)s %(message)s',
            datefmt  = '%Y-%m-%d,%H:%M:%S',
            level    = loglevel
            )
    log = logging.getLogger('lcr')
    ### }}} /Logging 

    logging.debug('Script started.')
    printlog(' Number of plates:')
    printlog(f'    straight = { n_straight }')
    printlog(f'    turn     = { n_turn }')
    printlog(f'    T-cross  = { n_tcross }')
    printlog(f'    X-cross  = { n_xcross }')
    printlog(f'    total    = { n_straight + n_turn + n_tcross + n_xcross}')
    printlog()

    roads = { 'straight': n_straight, 'turn': n_turn, 'tcross': n_tcross, 'xcross': n_xcross }
    min_used_items = n_straight + n_turn + n_tcross + n_xcross

    solutions = solve_board_wrapper(roads, min_used_items, cache_percent, use_mp)

    print()

    # This is a workaround. There is a racecondition in MP, different processes
    # can put the same solution into the list (even they check it before...):
    solutions = remove_duplicated_boards(solutions)

    if len(solutions) > 1:
        print_solution_report(solutions)
    elif len(solutions) == 0:
        print('There is no solution for this road set!')

    #print(f' rotated_board_time    = { rotated_board_time }   calls: {rotated_board_calls}')
    #print(f' mirrored_board_time   = { mirrored_board_time }   calls: {mirrored_board_calls}')
    #print(f' board_hash_time       = { board_hash_time }   calls: {board_hash_calls}')
    #print(f' extend_time           = { extend_time }   calls: {extend_calls}')
    #print()
    #print(f' size of been_there: {sys.getsizeof(been_there) / 1024**2} MB')
# }}}

if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))
    main()

