# test.py
""" This file houses the suite of tests for main.py classes and functions
"""


""" TEST FUNCTIONS -------------------------------------------------------------------------------------- TEST FUNCTIONS
"""


def board_initialisations():
    print(Board(STANDARD_GAME))
    print(Board(KING_AND_PAWN_GAME))
    print(Board(MINOR_GAME))
    print(Board(MAJOR_GAME))


def san_validation_decomposition(san_test_strings, string_decompositions):
    for i, elem in enumerate(san_test_strings):
        print('\n' + elem + ' :')
        try:
            assert validate_san(elem)
        except AssertionError:
            print('san FAILED to validate')
        else:
            print('validation: PASSED')
        decomposition = decompose_san(elem)
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
        conversion = convert_san2board(elem[0])
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
        conversion = convert_board2san(elem[1])
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
        if legal(a, b):
            print('LEGAL')
        else:
            print('NOT LEGAL!')


def repr_pieces(board):
    for rank in board.squares:
        for piece in rank:
            if isinstance(piece, Piece):
                print(repr(piece))


def what_checks(board, pieces):
    positions = (0, 3, 4, 7)
    for index, piece in enumerate(pieces):
        type_ = piece[1]
        board.squares[0][positions[index]] = eval(type_)(piece[0], board, (0, positions[index]))
    print(board)
    board.update_pieces()
    return board.in_check()


def test_all_checks(board):
    black_in_check = (('Black', 'King'), ('White', 'Queen'), ('White', 'King'))
    white_in_check = (('White', 'King'), ('Black', 'Queen'), ('Black', 'King'))
    both_in_check = (('White', 'King'), ('Black', 'Queen'), ('White', 'Queen'), ('Black', 'King'))
    no_checks = (('White', 'King'), ('Black', 'King'))

    print('BLACK_IN_CHECK has checks: ' + str(what_checks(board, black_in_check)))
    board.clear()
    print('WHITE_IN_CHECK has checks: ' + str(what_checks(board, white_in_check)))
    board.clear()
    print('BOTH_IN_CHECK has checks: ' + str(what_checks(board, both_in_check)))
    board.clear()
    print('NO_CHECKS has checks: ' + str(what_checks(board, no_checks)))


""" MAIN ---------------------------------------------------------------------------------------------------------- MAIN
"""

if __name__ == '__main__':
    """ Primary imports and initialisation -----------------------------------------------------------------------------
    """
    from Exceptions import *
    from main import *
    MAIN_VARIABLES()
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

    board = Board()
    print(board)

    # print(board.get_pieces('White', 'Pawn'))

    # board_initialisations()
    # san_validation_decomposition(SAN_TEST_STRINGS, STRING_DECOMPOSITIONS)
    # coord_conversions(COORDS)
    # repr_pieces(board)
    # test_legal(LEGAL_TEST)
    # print(board.get_pieces('White', 'King'))
    # board.clear()
    # test_all_checks(board)

    print(SERIES_OF_LEGAL_MOVES)
    turn_options = (('White', 0), ('Black', 1))
    player_turn = None
    move_count = 2

    for candidate in SERIES_OF_LEGAL_MOVES:
        player_turn = turn_options[move_count % 2]
        print(player_turn[0] + "'s turn!")

        print(candidate)

        if validate_san(candidate):
            decomposition = active_piece_type, disambiguation, is_capture,\
                target_san, promotion_type, _, castles = decompose_san(candidate)
        else:
            raise InvalidInput('Move notation failed to validate')
        print(decomposition)
        if not castles:
            target_location = convert_san2board(target_san)
            active_pieces = board.get_pieces(player_turn[0], active_piece_type, target_location)
            print('All pieces that can see the target_square:')
            print(active_pieces)
            if move_count == 16:
                print('Displaying Queen: \n\t\t' + repr(board.get_pieces(player_turn, 'Queen')))
                print(board.get_pieces(player_turn, 'Bishop'))
        else:
            target_sans = target_san.split()
            target_location = convert_san2board(target_sans[player_turn[1]])
            active_pieces = board.get_pieces(player_turn, active_piece_type, target_location)
            print('Time to implement castling!')
        if not active_pieces:
            try:
                raise InvalidInput('No piece able to execute such a move')
            except InvalidInput:
                print('InvalidInput: No piece able to execute such a move')
                print(active_pieces)
                print(active_piece_type)
                print(target_location)
        elif len(active_pieces) == 1:
            active_piece, = active_pieces
        else:
            active_pieces = disambiguate(active_pieces, disambiguation)
            try:
                active_piece, = active_pieces
            except ValueError:
                raise InvalidInput('Disambiguation insufficient: more than one piece able to make this move')
        # print('active pieces: ' + str(repr(active_pieces)))
        # print('active piece: ' + str(repr(active_piece)))

        print('\nActive Piece pre-move:')
        print(repr(active_piece))
        board.move(active_piece, target_location)
        print('Target Square post piece move:')
        print(repr(board.squares[target_location[0]][target_location[1]]))
        print(board)

        move_count += 1
        print('Move Count: ' + str(move_count))

