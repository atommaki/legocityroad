#!/usr/bin/env python3

import legocityroad as lcr
import os
import sys

def solution_test(n_straight, n_turn, n_tcross, n_xcross, expected_n_solutions, expected_boards):

    min_used_items = n_straight + n_turn + n_tcross + n_xcross

    progress = (0, 100)
    solutions = [ ]
    already_tried = set([])
    missing = []

    board = [ [ '*' ] ]

    f = open(os.devnull, 'w')
    origstdout = sys.stdout
    sys.stdout = f

    lcr.solve_board(progress, solutions, already_tried, missing, board, 0, 0, '╭', n_straight, n_turn, n_tcross, n_xcross, 1, min_used_items)

    sys.stdout = origstdout

    if len(solutions) != expected_n_solutions:
        print('len(solutions) != expected_n_solutions')
        print(f'{len(solutions)} != {expected_n_solutions}')
        return False

    for expected_board in expected_boards:

        expected_board_all_direction = []

        expected_board_all_direction.append(expected_board)
        expected_board_all_direction.append(lcr.get_right_rotated_board(expected_board))
        expected_board_all_direction.append(lcr.get_twice_rotated_board(expected_board))
        expected_board_all_direction.append(lcr.get_left_rotated_board(expected_board))

        m_board    = lcr.get_updown_mirrored_board(expected_board)
        expected_board_all_direction.append(m_board)
        expected_board_all_direction.append(lcr.get_right_rotated_board(m_board))
        expected_board_all_direction.append(lcr.get_twice_rotated_board(m_board))
        expected_board_all_direction.append(lcr.get_left_rotated_board(m_board))

        found = False
        for b in expected_board_all_direction:
            if b in solutions:
                found = True
                break
        if not found:
            print('One or more missing board hashes.')
            return False

    return True


testcases = [
    {
    'roads': { 'n_straight': 0, 'n_turn': 4, 'n_tcross': 0, 'n_xcross': 0},
    'expected_n_solutions': 1,
    'expected_boards_str' : [
        '''
        ╭╮
        ╰╯
        '''
        ]
    },

    {
    'roads': { 'n_straight': 2, 'n_turn': 12, 'n_tcross': 0, 'n_xcross': 0},
    'expected_n_solutions': 8,
    'expected_boards_str' : [
        '''
         ╭─╮
        ╭╯ ╰╮
        ╰╮ ╭╯
         ╰─╯
        ''',
        '''
          ╭╮
        ╭─╯╰╮
        ╰╮╭─╯
         ╰╯
        ''',
        '''
        ╭─╮
        ╰╮╰╮
         ╰╮╰╮
          ╰─╯
        '''
        ]
     }
]


exitcode = 0
for testcase in testcases:
    expected_n_solutions = testcase['expected_n_solutions']
    expected_boards = []
    for b_str in testcase['expected_boards_str']:
        expected_boards.append(lcr.str2board(b_str))

    n_straight = testcase['roads']['n_straight']
    n_turn =     testcase['roads']['n_turn']
    n_tcross =   testcase['roads']['n_tcross']
    n_xcross =   testcase['roads']['n_xcross']


    print(f'Test case {n_straight} {n_turn} {n_tcross} {n_xcross} starts here.')
    if solution_test(n_straight, n_turn, n_tcross, n_xcross, expected_n_solutions, expected_boards ):
        print(f'Test case {n_straight} {n_turn} {n_tcross} {n_xcross}: OK')
    else:
        print(f'Test case {n_straight} {n_turn} {n_tcross} {n_xcross}: FAIL')
        exitcode += 1


if exitcode != 0:
    print('There are test failures!')
else:
    print('ALL tests passed!')
sys.exit(exitcode)



