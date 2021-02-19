#!/usr/bin/env python3

import legocityroad as lcr
import os
import sys
import multiprocessing
from multiprocessing import Process, Manager, Semaphore
import time
from termcolor import colored


def solution_test(roads, expected_n_solutions, expected_boards, use_mp):

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
    sema = Semaphore(multiprocessing.cpu_count())

    lcr.solve_board(progress, solutions, solution_hashes, been_there, missing, board, 0, 0, '╭', roads, 1, min_used_items, 0, use_mp, sema)

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
            print('One or more board is missing from solutions.')
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
    },

    {
    'roads': { 'straight': 3, 'turn': 6, 'tcross': 2, 'xcross': 2},
    'expected_n_solutions': 3,
    'expected_boards_str' : [
        '''
         ╭╮
        ╭┼┤
        │││
        ╰┼┤
         ╰╯
        ''',
        '''
         ╭╮
        ╭┼┤
        │││
        ├┼╯
        ╰╯
        ''',
        '''
         ╭┬╮
        ╭┼┼╯
        │││
        ╰┴╯
        '''
        ]
     }
]


exitcode = 0
for testcase in testcases:
    for use_mp in [ False, True ]:
        expected_n_solutions = testcase['expected_n_solutions']
        expected_boards = []
        for b_str in testcase['expected_boards_str']:
            expected_boards.append(lcr.str2board(b_str))

        testcodename = str(testcase['roads']['straight']) + '-'
        testcodename = testcodename + str(testcase['roads']['turn']) + '-'
        testcodename = testcodename + str(testcase['roads']['tcross']) + '-'
        testcodename = testcodename + str(testcase['roads']['xcross'])
        if use_mp:
            testcodename = testcodename + '-mp'

        roads = testcase['roads']


        print(f'Test case {testcodename} starts here.')
        test_start = time.time()
        test_passed = solution_test(testcase['roads'],
                         testcase['expected_n_solutions'],
                         expected_boards,
                         use_mp
                          )
        test_end = time.time()
        test_time = test_end - test_start
        if test_passed:
            test_result = colored('OK', 'green')
        else:
            test_result = colored('FAIL', 'red')
            exitcode += 1
        print(f'Test case {testcodename}: {test_result} ({round(test_time,3)}s)')


if exitcode != 0:
    print('There are test failures!')
else:
    print('ALL tests passed!')
sys.exit(exitcode)



