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
    board.update_pieces('White')
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


def run_through_full_game(series_of_legal_moves):
    board = Board()
    print(board)

    print(series_of_legal_moves)
    count = 2

    for candidate in series_of_legal_moves:

        print(f"{board.player_turn}'s turn!")
        print(board)
        board.update_pieces(board.player_turn)
        if board.is_checkmate(board.player_turn):
            winner, = set(COLOURS) - {board.player_turn}
            print(f'                         CHECKMATE! {winner} wins!')
            print('\n                          GAME OVER!\n')
        else:
            print('\n')

        print(f'move : {candidate}')

        active_piece, active_piece_type, target_location, is_capture, promotion_type,\
            castle_direction = decompose_and_assess(board, candidate)
        board.move(active_piece, active_piece_type, target_location, is_capture, promotion_type, castle_direction)

        active_piece.has_moved = True
        board.player_turn, = set(COLOURS) - {board.player_turn}
        board.turn_num += 0.5
        print(f'Turn count: {board.turn_num}')

        print('\n' * 2)


def run_through_all_games():
    _zip = zip(HENCH_LIST_OF_GAMES, GAME_LENGTHS)
    for game, length in _zip:
        series_of_legal_moves = game.split()
        for i in range(1, length + 1):
            series_of_legal_moves.remove(str(i) + '.')

        run_through_full_game(series_of_legal_moves)


""" MAIN ---------------------------------------------------------------------------------------------------------- MAIN
"""

if __name__ == '__main__':
    """ Primary imports and initialisation -----------------------------------------------------------------------------
    """
    from Exceptions import *
    from main import *
    import copy
    MAIN_VARIABLES()
    COLOURS = ('White', 'Black')

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
        '8. Bh6 Bxh6 9. Qxh6 Bb7 10. a3 e5 11. 0-0-0 Qe7 12. Kb1 a6 13. Nc1 0-0-0 14. Nb3 exd4 15. Rxd4 c5 ' \
        '16. Rd1 Nb6 17. g3 Kb8 18. Na5 Ba8 19. Bh3 d5 20. Qf4+ Ka7 21. Rhe1 d4 22. Nd5 Nbxd5 23. exd5 Qd6 ' \
        '24. Rxd4 cxd4 25. Re7+ Kb6 26. Qxd4+ Kxa5 27. b4+ Ka4 28. Qc3 Qxd5 29. Ra7 Bb7 30. Rxb7 Qc4 31. Qxf6 Kxa3 ' \
        '32. Qxa6+ Kxb4 33. c3+ Kxc3 34. Qa1+ Kd2 35. Qb2+ Kd1 36. Bf1 Rd2 37. Rd7 Rxd7 38. Bxc4 bxc4 39. Qxh8 Rd3 ' \
        '40. Qa8 c3 41. Qa4+ Ke1 42. f4 f5 43. Kc1 Rd2 44. Qa7'
    MORPHY_DUKE_1858 = \
        '1. e4 e5 2. Nf3 d6 3. d4 Bg4 4. dxe5 Bxf3 5. Qxf3 dxe5 6. Bc4 Nf6 7. Qb3 Qe7 8. ' \
        'Nc3 c6 9. Bg5 b5 10. Nxb5 cxb5 11. Bxb5+ Nbd7 12. O-O-O Rd8 13. Rxd7 Rxd7 14. ' \
        'Rd1 Qe6 15. Bxd7+ Nxd7 16. Qb8+ Nxb8 17. Rd8#'
    ARONIAN_ANAND_WIJKAANZEE_2013 = \
        '1. d4 d5 2. c4 c6 3. Nf3 Nf6 4. Nc3 e6 5. e3 Nbd7 6. Bd3 dxc4 7. Bxc4 b5 8. Bd3 ' \
        'Bd6 9. O-O O-O 10. Qc2 Bb7 11. a3 Rc8 12. Ng5 c5 13. Nxh7 Ng4 14. f4 cxd4 15. ' \
        'exd4 Bc5 16. Be2 Nde5 17. Bxg4 Bxd4+ 18. Kh1 Nxg4 19. Nxf8 f5 20. Ng6 Qf6 21. h3 ' \
        'Qxg6 22. Qe2 Qh5 23. Qd3 Be3'
    KARPOV_KASPAROV_WORLD_CH_1985 = \
        '1. e4 c5 2. Nf3 e6 3. d4 cxd4 4. Nxd4 Nc6 5. Nb5 d6 6. c4 Nf6 7. N1c3 a6 8. Na3 ' \
        'd5 9. cxd5 exd5 10. exd5 Nb4 11. Be2 Bc5 12. O-O O-O 13. Bf3 Bf5 14. Bg5 Re8 15. ' \
        'Qd2 b5 16. Rad1 Nd3 17. Nab1 h6 18. Bh4 b4 19. Na4 Bd6 20. Bg3 Rc8 21. b3 g5 22. ' \
        'Bxd6 Qxd6 23. g3 Nd7 24. Bg2 Qf6 25. a3 a5 26. axb4 axb4 27. Qa2 Bg6 28. d6 g4 ' \
        '29. Qd2 Kg7 30. f3 Qxd6 31. fxg4 Qd4+ 32. Kh1 Nf6 33. Rf4 Ne4 34. Qxd3 Nf2+ 35. ' \
        'Rxf2 Bxd3 36. Rfd2 Qe3 37. Rxd3 Rc1 38. Nb2 Qf2 39. Nd2 Rxd1+ 40. Nxd1 Re1+'
    BYRNE_FISCHER_MEMORIAL_ROSENWALD_1956 = \
        '1. Nf3 Nf6 2. c4 g6 3. Nc3 Bg7 4. d4 O-O 5. Bf4 d5 6. Qb3 dxc4 7. Qxc4 c6 8. e4 ' \
        'Nbd7 9. Rd1 Nb6 10. Qc5 Bg4 11. Bg5 Na4 12. Qa3 Nxc3 13. bxc3 Nxe4 14. Bxe7 Qb6 ' \
        '15. Bc4 Nxc3 16. Bc5 Rfe8+ 17. Kf1 Be6 18. Bxb6 Bxc4+ 19. Kg1 Ne2+ 20. Kf1 Nxd4+ ' \
        '21. Kg1 Ne2+ 22. Kf1 Nc3+ 23. Kg1 axb6 24. Qb4 Ra4 25. Qxb6 Nxd1 26. h3 Rxa2 27. ' \
        'Kh2 Nxf2 28. Re1 Rxe1 29. Qd8+ Bf8 30. Nxe1 Bd5 31. Nf3 Ne4 32. Qb8 b5 33. h4 h5 ' \
        '34. Ne5 Kg7 35. Kg1 Bc5+ 36. Kf1 Ng3+ 37. Ke1 Bb4+ 38. Kd1 Bb3+ 39. Kc1 Ne2+ 40. ' \
        'Kb1 Nc3+ 41. Kc1 Rc2#'
    IVANCHUK_YUSUPOV_WORLD_CH_1991 = \
        '1. c4 e5 2. g3 d6 3. Bg2 g6 4. d4 Nd7 5. Nc3 Bg7 6. Nf3 Ngf6 7. O-O O-O 8. Qc2 ' \
        'Re8 9. Rd1 c6 10. b3 Qe7 11. Ba3 e4 12. Ng5 e3 13. f4 Nf8 14. b4 Bf5 15. Qb3 h6 ' \
        '16. Nf3 Ng4 17. b5 g5 18. bxc6 bxc6 19. Ne5 gxf4 20. Nxc6 Qg5 21. Bxd6 Ng6 22. ' \
        'Nd5 Qh5 23. h4 Nxh4 24. gxh4 Qxh4 25. Nde7+ Kh8 26. Nxf5 Qh2+ 27. Kf1 Re6 28. ' \
        'Qb7 Rg6 29. Qxa8+ Kh7 30. Qg8+ Kxg8 31. Nce7+ Kh7 32. Nxg6 fxg6 33. Nxg7 Nf2 34. ' \
        'Bxf4 Qxf4 35. Ne6 Qh2 36. Rdb1 Nh3 37. Rb7+ Kh8 38. Rb8+ Qxb8 39. Bxh3 Qg3'
    SHORT_TIMMAN_TILBURG_1991 = \
        '1. e4 Nf6 2. e5 Nd5 3. d4 d6 4. Nf3 g6 5. Bc4 Nb6 6. Bb3 Bg7 7. Qe2 Nc6 8. O-O ' \
        'O-O 9. h3 a5 10. a4 dxe5 11. dxe5 Nd4 12. Nxd4 Qxd4 13. Re1 e6 14. Nd2 Nd5 15. ' \
        'Nf3 Qc5 16. Qe4 Qb4 17. Bc4 Nb6 18. b3 Nxc4 19. bxc4 Re8 20. Rd1 Qc5 21. Qh4 b6 ' \
        '22. Be3 Qc6 23. Bh6 Bh8 24. Rd8 Bb7 25. Rad1 Bg7 26. R8d7 Rf8 27. Bxg7 Kxg7 28. ' \
        'R1d4 Rae8 29. Qf6+ Kg8 30. h4 h5 31. Kh2 Rc8 32. Kg3 Rce8 33. Kf4 Bc8 34. Kg5'
    BAI_LIREN_CHINESE_CH_LEAGUE_2017 = \
        '1. d4 Nf6 2. c4 e6 3. Nc3 Bb4 4. Nf3 O-O 5. Bg5 c5 6. e3 cxd4 7. Qxd4 Nc6 8. Qd3 ' \
        'h6 9. Bh4 d5 10. Rd1 g5 11. Bg3 Ne4 12. Nd2 Nc5 13. Qc2 d4 14. Nf3 e5 15. Nxe5 ' \
        'dxc3 16. Rxd8 cxb2+ 17. Ke2 Rxd8 18. Qxb2 Na4 19. Qc2 Nc3+ 20. Kf3 Rd4 21. h3 h5 ' \
        '22. Bh2 g4+ 23. Kg3 Rd2 24. Qb3 Ne4+ 25. Kh4 Be7+ 26. Kxh5 Kg7 27. Bf4 Bf5 28. ' \
        'Bh6+ Kh7 29. Qxb7 Rxf2 30. Bg5 Rh8 31. Nxf7 Bg6+ 32. Kxg4 Ne5+'
    ROTLEVI_RUBINSTEIN_RUSSIAN_CH_1907 = \
        '1. d4 d5 2. Nf3 e6 3. e3 c5 4. c4 Nc6 5. Nc3 Nf6 6. dxc5 Bxc5 7. a3 a6 8. b4 Bd6 ' \
        '9. Bb2 O-O 10. Qd2 Qe7 11. Bd3 dxc4 12. Bxc4 b5 13. Bd3 Rd8 14. Qe2 Bb7 15. O-O ' \
        'Ne5 16. Nxe5 Bxe5 17. f4 Bc7 18. e4 Rac8 19. e5 Bb6+ 20. Kh1 Ng4 21. Be4 Qh4 22. ' \
        'g3 Rxc3 23. gxh4 Rd2 24. Qxd2 Bxe4+ 25. Qg2 Rh3'
    GELLER_EUWE_CANDIDATES_ZURICH_1953 = \
        '1. d4 Nf6 2. c4 e6 3. Nc3 Bb4 4. e3 c5 5. a3 Bxc3+ 6. bxc3 b6 7. Bd3 Bb7 8. f3 ' \
        'Nc6 9. Ne2 O-O 10. O-O Na5 11. e4 Ne8 12. Ng3 cxd4 13. cxd4 Rc8 14. f4 Nxc4 15. ' \
        'f5 f6 16. Rf4 b5 17. Rh4 Qb6 18. e5 Nxe5 19. fxe6 Nxd3 20. Qxd3 Qxe6 21. Qxh7+ ' \
        'Kf7 22. Bh6 Rh8 23. Qxh8 Rc2 24. Rc1 Rxg2+ 25. Kf1 Qb3 26. Ke1 Qf3'
    HENCH_LIST_OF_GAMES = [
        KASPAROV_TOPALOV_WIJKAANZEE_1999,
        MORPHY_DUKE_1858,
        ARONIAN_ANAND_WIJKAANZEE_2013,
        KARPOV_KASPAROV_WORLD_CH_1985,
        BYRNE_FISCHER_MEMORIAL_ROSENWALD_1956,
        IVANCHUK_YUSUPOV_WORLD_CH_1991,
        SHORT_TIMMAN_TILBURG_1991,
        BAI_LIREN_CHINESE_CH_LEAGUE_2017,
        ROTLEVI_RUBINSTEIN_RUSSIAN_CH_1907,
        GELLER_EUWE_CANDIDATES_ZURICH_1953,
    ]
    GAME_LENGTHS = [44, 17, 23, 40, 41, 39, 34, 32, 25, 26]


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

    run_through_all_games()




