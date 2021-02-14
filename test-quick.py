#!/usr/bin/env python3

import legocityroad as lcr
import os
import sys
from multiprocessing import Process, Manager


def solution_test(roads, expected_n_solutions, expected_boards):

    min_used_items = roads['straight'] + roads['turn'] + roads['tcross'] + roads['xcross']

    mpman = Manager()

    progress = (0, 100)
    solutions = mpman.list()
    solution_hashes = mpman.dict()
    been_there = mpman.dict()
    missing = [ (0,0) ]

    board = [ [ '*' ] ]

    f = open(os.devnull, 'w')
    origstdout = sys.stdout
    sys.stdout = f

    lcr.solve_board(progress, solutions, solution_hashes, been_there, missing, board, 0, 0, '╭', roads, 1, min_used_items, 100)

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
    'roads': { 'straight': 0, 'turn': 4, 'tcross': 0, 'xcross': 0},
    'expected_n_solutions': 1,
    'expected_boards_str' : [
        '''
        ╭╮
        ╰╯
        '''
        ]
    },

    {
    'roads': { 'straight': 2, 'turn': 12, 'tcross': 0, 'xcross': 0},
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

    testcodename = str(testcase['roads']['straight']) + '-'
    testcodename = testcodename + str(testcase['roads']['turn']) + '-'
    testcodename = testcodename + str(testcase['roads']['tcross']) + '-'
    testcodename = testcodename + str(testcase['roads']['xcross'])

    roads = testcase['roads']


    print(f'Test case {testcodename} starts here.')
    if solution_test(roads, expected_n_solutions, expected_boards ):
        print(f'Test case {testcodename}: OK')
    else:
        print(f'Test case {testcodename}: FAIL')
        exitcode += 1


if exitcode != 0:
    print('There are test failures!')
else:
    print('ALL tests passed!')
sys.exit(exitcode)



