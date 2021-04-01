# test.py
""" This file houses the suite of tests for main.py classes and functions

"""
""" TEST FUNCTIONS -------------------------------------------------------------------------------------- TEST FUNCTIONS
"""


def board_initialisations():
    print(main.Board(main.STANDARD_GAME))
    print(main.Board(main.KING_AND_PAWN_GAME))
    print(main.Board(main.MINOR_GAME))
    print(main.Board(main.MAJOR_GAME))


def san_validation_decomposition(san_test_strings, string_decompositions):
    for i, elem in enumerate(san_test_strings):
        print('\n' + elem + ' :')
        try:
            assert main.validate_san(elem)
        except AssertionError:
            print('san FAILED to validate')
        else:
            print('validation: PASSED')
        decomposition = main.decompose_san(elem)
        print(decomposition)
        try:
            assert decomposition == string_decompositions[i]
        except AssertionError:
            print('san FAILED to decompose')
            print('got instead: ' + str(decomposition))
        else:
            print('decomposition: PASSED >>')
            print(decomposition)


def coord_conversions(coords):
    for elem in coords:
        print('\n' + elem[0] + ' :')
        conversion = main.convert_san2board(elem[0])
        try:
            assert conversion == elem[1]
        except AssertionError:
            print('san FAILED to convert')
            print('got instead: ' + str(conversion))
        else:
            print('conversion: PASSED >>')
            print(conversion)

    for elem in coords:
        print('\n' + str(elem[1]) + ' :')
        conversion = main.convert_board2san(elem[1])
        try:
            assert conversion == elem[0]
        except AssertionError:
            print('san FAILED to convert')
            print('got instead: ' + str(conversion))
        else:
            print('conversion: PASSED >>')
            print(conversion)


def test_legal(coords):
    for coord in coords:
        print(coord)
        a, b = coord
        if main.legal(a, b):
            print('LEGAL')
        else:
            print('NOT LEGAL!')


def repr_pieces(board):
    for row, rank in enumerate(board.squares):
        for piece in rank:
            if isinstance(piece, main.Piece):
                print(repr(piece))


""" MAIN ---------------------------------------------------------------------------------------------------------- MAIN
"""

if __name__ == '__main__':
    """ Primary imports and initialisation -----------------------------------------------------------------------------
    """
    import main
    main.MAIN_VARIABLES()
    """ Local imports and initialisation -----------------------------------------------------------------------------
    """
    SAN_TEST_STRINGS = (
        'e4', 'Nxf5', 'exd4', 'Rdf8', 'R1a3', 'Qh4e1',
        'Qh4xe1+', 'e8Q', 'fxe8Q#', 'f8N', '0-0', '0-0-0',
    )
    STRING_DECOMPOSITIONS = (
        ('Pawn', '', False, 'e4', '', '', ''),
        ('Knight', '', True, 'f5', '', '', ''),
        ('Pawn', 'e', True, 'd4', '', '', ''),
        ('Rook', 'd', False, 'f8', '', '', ''),
        ('Rook', '1', False, 'a3', '', '', ''),
        ('Queen', 'h4', False, 'e1', '', '', ''),
        ('Queen', 'h4', True, 'e1', '', '+', ''),
        ('Pawn', '', False, 'e8', 'Queen', '', ''),
        ('Pawn', 'f', True, 'e8', 'Queen', '#', ''),
        ('Pawn', '', False, 'f8', 'Knight', '', ''),
        ('King', '', False, '', '', '', 'King'),
        ('King', '', False, '', '', '', 'Queen'),
    )
    COORDS = (
        ('e4', (4, 4)),
        ('a1', (7, 0)),
        ('a8', (0, 0)),
        ('h1', (7, 7)),
        ('h8', (0, 7)),
        ('d3', (5, 3))
    )
    LEGAL_TEST = [(x, 4) for x in range(-2, 10)] + [(4, x) for x in range(-2, 10)]
    KASPAROV_TOPALOV_WIJKAANZEE_1999 = \
        '1. e4 d6 2. d4 Nf6 3. Nc3 g6 4. Be3 Bg7 5. Qd2 c6 6. f3 b5 7. Nge2 Nbd7 ' \
        '8. Bh6 Bxh6 9. Qxh6 Bb7 10. a3 e5 11. O-O-O Qe7 12. Kb1 a6 13. Nc1 O-O-O 14. Nb3 exd4 15. Rxd4 c5 ' \
        '16. Rd1 Nb6 17. g3 Kb8 18. Na5 Ba8 19. Bh3 d5 20. Qf4+ Ka7 21. Rhe1 d4 22. Nd5 Nbxd5 23. exd5 Qd6 ' \
        '24. Rxd4 cxd4 25. Re7+ Kb6 26. Qxd4+ Kxa5 27. b4+ Ka4 28. Qc3 Qxd5 29. Ra7 Bb7 30. Rxb7 Qc4 31. Qxf6 Kxa3 ' \
        '32. Qxa6+ Kxb4 33. c3+ Kxc3 34. Qa1+ Kd2 35. Qb2+ Kd1 36. Bf1 Rd2 37. Rd7 Rxd7 38. Bxc4 bxc4 39. Qxh8 Rd3 ' \
        '40. Qa8 c3 41. Qa4+ Ke1 42. f4 f5 43. Kc1 Rd2 44. Qa7'
    SERIES_OF_LEGAL_MOVES = KASPAROV_TOPALOV_WIJKAANZEE_1999.split()
    for i in range(1, 45):
        SERIES_OF_LEGAL_MOVES.remove(str(i) + '.')

    """ Main -----------------------------------------------------------------------------------------------------------
    """

    board = main.Board()
    print(board)

    # board_initialisations()
    # san_validation_decomposition(SAN_TEST_STRINGS, STRING_DECOMPOSITIONS)
    # coord_conversions(COORDS)
    # repr_pieces(board)
    # test_legal(LEGAL_TEST)

    print(board.get_pieces('White', 'Pawn', main.convert_san2board('h4')))

