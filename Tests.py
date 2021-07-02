# test.py
""" This file houses the suite of tests for main.py classes and functions

    THIS FILE IS A MESS AND TOTALLY BROKEN AT THIS POINT
    IT WILL NOT RUN
    IT IS HERE THAT IT MAY BE CANABALISED FOR FUTURE ITERATIONS OF THE PROJECT

"""


def test_variables():
    """ variables needed for various tests """
    global game_1, game_2, game_3, game_4, game_5, game_6, game_7, game_8, game_9
    global game_10, game_11, game_12, game_13, game_14, game_15, game_16, game_17, game_18
    global game_19, game_20, game_21, game_22, game_23, game_24, game_25, game_26, game_27
    global game_28, game_29, game_30, game_31, game_32, game_33, game_34, game_35, game_36
    global game_37, game_38, game_39, game_40, game_41, game_42, game_43, game_44, game_45
    global game_46, game_47, game_48, game_49, legal_checkmates
    global fens, fen_1, fen_2, fen_3, fen_4

    fen_1 = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    fen_2 = 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1'
    fen_3 = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2'
    fen_4 = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2'

    fens = [fen_1, fen_2, fen_3, fen_4]

    game_1 = '1. e4 d5 '\
        '2. exd5 Qxd5 3. Nc3 Qd8 4. Bc4 Nf6 5. Nf3 Bg4 6. h3 Bxf3 '\
        '7. Qxf3 e6 8. Qxb7 Nbd7 9. Nb5 Rc8 10. Nxa7 Nb6 11. Nxc8 Nxc8 '\
        '12. d4 Nd6 13. Bb5+ Nxb5 14. Qxb5+ Nd7 15. d5 exd5 16. Be3 Bd6 '\
        '17. Rd1 Qf6 18. Rxd5 Qg6 19. Bf4 Bxf4 20. Qxd7+ Kf8 21. Qd8#'
    game_2 = '1.e4 b6 2.d4 Bb7 3.Bd3 f5 4.exf5 Bxg2 5.Qh5+ g6 6.fxg6 Nf6 ' \
        '7.gxh7 Nxh5 8.Bg6#'
    game_3 = '1.e4 e5 2.Nf3 Nc6 3.Bc4 Nf6 4.Ng5 d5 5.exd5 Nxd5 6.Nxf7 Kxf7 '\
        '7.Qf3+ Ke6 8.Nc3 Nce7 9.O-O c6 10.Re1 Bd7 11.d4 Kd6 12.Rxe5 Ng6 '\
        '13.Nxd5 Nxe5 14.dxe5+ Kc5 15.Qa3+ Kxc4 16.Qd3+ Kc5 17.b4#'
    game_4 = '1. e4 e5 2. Nf3 d6 3. Bc4 Bg4 4. Nc3 g6 5. Nxe5 Bxd1 6. Bxf7+ '\
        'Ke7 7. Nd5#'
    game_5 = '1. e4 e5 2. Bc4 Bc5 3. d3 c6 4. Qe2 d6 5. f4 exf4 6. Bxf4 Qb6 '\
        '7. Qf3 Qxb2 8. Bxf7+ Kd7 9. Ne2 Qxa1 10. Kd2 Bb4+ 11. Nbc3 '\
        'Bxc3+ 12. Nxc3 Qxh1 13. Qg4+ Kc7 14. Qxg7 Nd7 15. Qg3 b6 '\
        '16. Nb5+ cxb5 17. Bxd6+ Kb7 18. Bd5+ Ka6 19. d4 b4 20. Bxb4 '\
        'Kb5 21. c4+ Kxb4 22. Qb3+ Ka5 23. Qb5#'
    game_6 = '1.e4 e5 2.f4 exf4 3.Bc4 Qh4+ 4.Kf1 b5 5.Bxb5 Nf6 6.Nf3 Qh6 '\
        '7.d3 Nh5 8.Nh4 Qg5 9.Nf5 c6 10.g4 Nf6 11.Rg1 cxb5 12.h4 Qg6 '\
        '13.h5 Qg5 14.Qf3 Ng8 15.Bxf4 Qf6 16.Nc3 Bc5 17.Nd5 Qxb2 18.Bd6 '\
        "Bxg1 {It is from this move that Black's defeat stems. Wilhelm "\
        'Steinitz suggested in 1879 that a better move would be '\
        '18... Qxa1+; likely moves to follow are 19. Ke2 Qb2 20. Kd2 '\
        'Bxg1.} 19. e5 Qxa1+ 20. Ke2 Na6 21.Nxg7+ Kd8 22.Qf6+ Nxf6 '\
        '23.Be7#'
    game_7 = '1.e4 e5 2.Nf3 Nc6 3.Bc4 Bc5 4.c3 Qe7 5.O-O d6 6.d4 Bb6 7.Bg5 '\
        'f6 8.Bh4 g5 9.Nxg5 fxg5 10.Qh5+ Kf8 11.Bxg5 Qe8 12.Qf3+ Kg7 '\
        '13.Bxg8 Rxg8 14.Qf6#'
    game_8 = '1.e4 e5 2.Nf3 Nc6 3.Bc4 Bc5 4.b4 Bxb4 5.c3 Ba5 6.d4 exd4 7.O-O '\
        'd3 8.Qb3 Qf6 9.e5 Qg6 10.Re1 Nge7 11.Ba3 b5 12.Qxb5 Rb8 13.Qa4 '\
        'Bb6 14.Nbd2 Bb7 15.Ne4 Qf5 16.Bxd3 Qh5 17.Nf6+ gxf6 18.exf6 '\
        'Rg8 19.Rad1 Qxf3 20.Rxe7+ Nxe7 21.Qxd7+ Kxd7 22.Bf5+ Ke8 '\
        '23.Bd7+ Kf8 24.Bxe7#'
    game_9 = '1.e4 e5 2.Nf3 Nc6 3.Bc4 Nf6 4.d4 exd4 5.Ng5 d5 6.exd5 Nxd5 '\
        '7.O-O Be7 8.Nxf7 Kxf7 9.Qf3+ Ke6 10.Nc3 dxc3 11.Re1+ Ne5 '\
        '12.Bf4 Bf6 13.Bxe5 Bxe5 14.Rxe5+ Kxe5 15.Re1+ Kd4 16.Bxd5 Re8 '\
        '17.Qd3+ Kc5 18.b4+ Kxb4 19.Qd4+ Ka5 20.Qxc3+ Ka4 21.Qb3+ Ka5 '\
        '22.Qa3+ Kb6 23.Rb1#'
    game_10 = '1. e4 e5 2. d4 exd4 3. Bc4 Nf6 4. e5 d5 5. Bb3 Ne4 6. Ne2 Bc5 '\
        '7. f3 Qh4+ 8. g3 d3 9. gxh4 Bf2+ 10. Kf1 Bh3#'
    game_11 = '1. e4 e5 2. Nf3 d6 3. Bc4 f5 4. d4 Nf6 5. Nc3 exd4 6. Qxd4 Bd7 '\
        '7. Ng5 Nc6 8. Bf7+ Ke7 9. Qxf6+ Kxf6 10. Nd5+ Ke5 11. Nf3+ '\
        'Kxe4 12. Nc3#'
    game_12 = '1. e4 e5 2. d4 exd4 3. c3 dxc3 4. Bc4 d6 5. Nxc3 Nf6 6. Nf3 '\
        'Bg4 7. O-O Nc6 8. Bg5 Ne5 9. Nxe5 Bxd1 10. Bxf7+ Ke7 11. Nd5#'
    game_13 = '1.e4 e5 2.Nf3 Nc6 3.Bc4 Nh6 4.O-O Ng4 5.d4 exd4 6.Bxf7+ Kxf7 '\
        '7.Ng5+ Kg6 8.Qxg4 d5 9.Ne6+ Kf6 10.Qf5+ Ke7 11.Bg5+ Kd6 '\
        '12.Qxd5#'
    game_14 = '1. e4 e6 2. d4 d5 3. Nc3 Bb4 4. Bd3 Bxc3+ 5. bxc3 h6 6. Ba3 '\
        'Nd7 7. Qe2 dxe4 8. Bxe4 Ngf6 9. Bd3 b6 10. Qxe6+ fxe6 11. Bg6#'
    game_15 = '1.e4 e5 2.d4 exd4 3.Nf3 Nc6 4.Bc4 Be7 5.c3 dxc3 6.Qd5 d6 '\
        '7.Qxf7+ Kd7 8.Be6#'
    game_16 = '1. Nf3 Nf6 2. c4 c5 3. d4 Nc6 4. d5 Nb8 5. Nc3 d6 6. g3 g6 '\
        '7. Bg2 Bg7 8. O-O O-O 9. Bf4 h6 10. Qd2 Kh7 11. e4 Nh5 12. Be3 '\
        'Nd7 13. Rae1 Rb8 14. Nh4 Ndf6 15. h3 Ng8 16. g4 Nhf6 17. f4 e6 '\
        '18. Nf3 exd5 19. cxd5 b5 20. e5 b4 21. Nd1 Ne4 22. Qd3 f5 '\
        '23. e6 Qa5 24. gxf5 gxf5 25. Nh4 Ba6 26. Qxe4 fxe4 27. Bxe4+ '\
        'Kh8 28. Ng6+ Kh7 29. Nxf8+ Kh8 30. Ng6+ Kh7 31. Ne5+ Kh8 '\
        '32. Nf7#'
    game_17 = '1. e4 e5 2. f4 exf4 3. Nf3 Nf6 4. e5 Ng4 5. d4 g5 6. Nc3 Ne3 '\
        '7. Qe2 Nxf1 8. Ne4 Ne3 9. Nf6+ Ke7 10. Bd2 Nxc2+ 11. Kf2 Nxa1 '\
        '12. Nd5+ Ke6 13. Qc4 b5 14. Nxg5+ Qxg5 15. Nxc7+ Ke7 16. Nd5+ '\
        'Ke6 17. Nxf4+ Ke7 18. Nd5+ Ke8 19. Qxc8+ Qd8 20. Nc7+ Ke7 '\
        '21. Bb4+ d6 22. Bxd6+ Qxd6 23. Qe8#'
    game_18 = '1. d4 { Notes by Raymond Keene. Here is a brilliant win by '\
        'Tarrasch. } d5 2. Nf3 c5 3. c4 e6 4. e3 Nf6 5. Bd3 Nc6 6. O-O '\
        'Bd6 7. b3 O-O 8. Bb2 b6 9. Nbd2 Bb7 10. Rc1 Qe7 11. cxd5 {11 '\
        'Qe2!? } 11...exd5 12. Nh4 g6 13. Nhf3 Rad8 14. dxc5 bxc5 '\
        '15. Bb5 Ne4 16. Bxc6 Bxc6 17. Qc2 Nxd2 18. Nxd2 {"The guardian '\
        "of the king's field leaves his post for a moment, assuming "\
        'wrongly that 19 Qc3 is a major threat" -- Tartakower. If 18 '\
        'Qxd2 d4 19 exd4 Bxf3 20 gxf3 Qh4 } 18...d4 {!} 19. exd4 {19 '\
        'Rfe1! } Bxh2+ 20. Kxh2 Qh4+ 21. Kg1 Bxg2 {!} 22. f3 {22 Kxg2 '\
        'Qg4+ 23 Kh2 Rd5-+ } 22...Rfe8 23. Ne4 Qh1+ 24. Kf2 Bxf1 25. d5 '\
        '{25 Rxf1 Qh2+ or 25 Nf6+ Kf8 26 Nxe8 Qg2+ } 25...f5 26. Qc3 '\
        'Qg2+ 27. Ke3 Rxe4+ 28. fxe4 f4+ {28...Qg3+! } 29. Kxf4 Rf8+ '\
        '30. Ke5 Qh2+ 31. Ke6 Re8+ 32. Kd7 Bb5#'
    game_19 = '1. e4 e5 2. Nc3 Nc6 3. Nf3 d6 4. Bb5 Bg4 5. Nd5 Nge7 6. c3 a6 '\
        '7. Ba4 b5 8. Bb3 Na5 9. Nxe5 Bxd1 10. Nf6+ gxf6 11. Bxf7#'
    game_20 = '1.e4 {Notes by Karel Traxler} e5 2.Nf3 Nc6 3.Bc4 Nf6 4.Ng5 Bc5 '\
        '{An original combination that is better than it looks. A small '\
        'mistake by white can give black a decisive attack. It is not '\
        'easy to find the best defense against it in a practical game '\
        'and it is probably theoretically correct. ... It somewhat '\
        'resembles the Blackmar-Jerome gambit: 1.e4 e5 2.Nf3 Nc6 3.Bc4 '\
        'Bc5 4.Bxf7+?! Kxf7 5.Nxe5+?!} 5.Nxf7 Bxf2+ 6.Ke2 {The best '\
        'defense is 6.Kf1! although after 6...Qe7 7.Nxh8 d5 8.exd5 Nd4 '\
        'Black gets a strong attack.} Nd4+ 7.Kd3 b5 8.Bb3 Nxe4 9.Nxd8 '\
        '{White has no defense; the mating finale is pretty.} Nc5+ '\
        '10.Kc3 Ne2+ 11.Qxe2 Bd4+ 12.Kb4 a5+ 13.Kxb5 Ba6+ 14.Kxa5 Bd3+ '\
        '15.Kb4 Na6+ 16.Ka4 Nb4+ 17.Kxb4 c5#'
    game_21 = '1. e4 {Some sources indicate that this game is actually a '\
        'post-mortem of a twenty-three move draw.} e5 2. f4 Bc5 3. Nf3 '\
        'd6 4. Nc3 Nf6 5. Bc4 Nc6 6. d3 Bg4 7. Na4 exf4 8. Nxc5 dxc5 '\
        '9. Bxf4 Nh5 10. Be3 Ne5 11. Nxe5 Bxd1 12. Bxf7+ Ke7 13. Bxc5+ '\
        'Kf6 14. O-O+ Kxe5 15. Rf5#'
    game_22 = '1. e4 e5 2. Nf3 Nc6 3. d4 exd4 4. Bc4 Nf6 5. e5 d5 6. Bb5 Ne4 '\
        '7. Nxd4 Bd7 8. Bxc6 bxc6 9. O-O Be7 10. f3 Nc5 11. f4 f6 '\
        '12. f5 fxe5 13. Qh5+ Kf8 14. Ne6+ Bxe6 15. fxe6+ Bf6 16. Qf7#'
    game_23 = '1.e4 d5 2.exd5 Qxd5 3.Ke2 {White intended to play 3.Nc3, bu t '\
        'by accident moved the Bc1 to c3 instead. The rules at the time '\
        'required that an illegal move be retracted and replaced with a '\
        'legal king move, so 3.Ke2 was the penalty. What happened next '\
        'is unclear. The usual account is that Black simply played '\
        '3...Qe4#. (See, for example, Irving Chernev, "Wonders and '\
        'Curiosities of Chess", New York, 1974, p. 119.) However, some '\
        'contemporary accounts indicate that Black did not play the '\
        'mate because he did not see it ("Deutsche Schachzeitung" of '\
        'September 1893, p. 283). The tournament book is more '\
        'ambiguous, claiming that Black let White wriggle for a while '\
        '(Kiel, 1893 tournament book, p. 60 (in the original "[...] zog '\
        'es aber vor, den Gegner erst noch zappeln zu lassen, ehe er '\
        'ihn endlich erschlug.")), indicating either a pause before '\
        'playing 3...Qe4# or preference for a slower win. If additional '\
        'moves were played after 3.Ke2, they have not been '\
        "recorded. Information was retrieved from Edward Winter's C.N "\
        '5381.} Qe4#'
    game_24 = '1. e4 d5 2. exd5 Qxd5 3. Nc3 Qd8 4. d4 Nc6 5. Nf3 Bg4 6. d5 '\
        'Ne5 7. Nxe5 Bxd1 8. Bb5+ c6 9. dxc6 Qc7 10. cxb7+ Kd8 '\
        '11. Nxf7#'
    game_25 = '1.e4 d5 2.exd5 Qxd5 3.Nc3 Qa5 4.d4 c6 5.Nf3 Bg4 6.Bf4 e6 7.h3 '\
        'Bxf3 8.Qxf3 Bb4 9.Be2 Nd7 10.a3 O-O-O 11.axb4 Qxa1+ 12.Kd2 '\
        'Qxh1 13.Qxc6+ bxc6 14.Ba6#'
    game_26 = '1. e4 e5 2. d4 exd4 3. Qxd4 Nc6 4. Qe3 Bb4+ 5. c3 Ba5 6. Bc4 '\
        'Nge7 7. Qg3 O-O 8. h4 Ng6 9. h5 Nge5 10. Bg5 Qe8 11. Bf6 g6 '\
        '12. hxg6 Nxg6 13. Qxg6+ hxg6 14. Rh8#'
    game_27 = '1. e4 e5 2. Bc4 Bc5 3. Qh5 g6 4. Qxe5+ Ne7 5. Qxh8+ Ng8 '\
        '6. Qxg8+ Bf8 7. Qxf7#'
    game_28 = '1.e4 e5 2.Bc4 Bc5 3.Qe2 Qe7 4.f4 Bxg1 5.Rxg1 exf4 6.d4 Qh4+ '\
        '7.g3 fxg3 8.Rxg3 Nf6 9.Nc3 Nh5 10.Bxf7+ Kxf7 11.Bg5 Nxg3 '\
        '12.Qf3+ Kg6 13.Bxh4 Nh5 14.Qf5+ Kh6 15.Qg5#'
    game_29 = '1.e4 e5 2.Nc3 Nc6 3.f4 exf4 4.d4 Qh4+ 5.Ke2 b6 6.Nb5 Nf6 7.Nf3 '\
        'Qg4 8.Nxc7+ Kd8 9.Nxa8 Nxe4 10.c4 Bb4 11.Qa4 Nxd4+ 12.Kd1 Nf2#'
    game_30 = '1. e4 e5 2. Nc3 Nc6 3. f4 d6 4. Nf3 a6 5. Bc4 Bg4 6. fxe5 Nxe5 '\
        '7. Nxe5 Bxd1 8. Bxf7+ Ke7 9. Nd5#'
    game_31 = '1.e4 e5 2.Nc3 Nc6 3.f4 exf4 4.Nf3 g5 5.h4 g4 6.Ng5 h6 7.Nxf7 '\
        'Kxf7 8.Bc4+ Ke8 9.Qxg4 Ne5 10.Qh5+ Ke7 11.Qxe5#'
    game_32 = '1. e4 e5 2. f4 exf4 3. Nf3 Nc6 4. Nc3 d6 5. Bc4 Bg4 6. Ne5 '\
        'Bxd1 7. Bxf7+ Ke7 8. Nd5#'
    game_33 = '1. e4 e5 2. Nf3 f5 3. Nxe5 Qf6 4. d4 d6 5. Nc4 fxe4 6. Be2 Nc6 '\
        '7. d5 Ne5 8. O-O Nxc4 9. Bxc4 Qg6 10. Bb5+ Kd8 11. Bf4 h5 '\
        '12. f3 Bf5 13. Nc3 exf3 14. Qxf3 Bxc2 15. Bg5+ Nf6 16. Rae1 c6 '\
        '17. Bxf6+ Qxf6 18. Qe2 Qd4+ 19. Kh1 Bg6 20. Rxf8+ Kc7 21. Bxc6 '\
        'bxc6 22. Nb5+ cxb5 23. Qxb5 Re8 24. Re7+ Rxe7 25. Qc6#'
    game_34 = '1. e4 e5 2. f4 exf4 3. Bc4 d5 4. Bxd5 Nf6 5. Nc3 Bb4 6. Nf3 '\
        'O-O 7. O-O Nxd5 8. Nxd5 Bd6 9. d4 g5 10. Nxg5 Qxg5 11. e5 Bh3 '\
        '12. Rf2 Bxe5 13. dxe5 c6 14.Bxf4 Qg7 15. Nf6+ Kh8 16. Qh5 Rd8 '\
        '17. Qxh3 Na6 18. Rf3 Qg6 19. Rc1 Kg7 20. Rg3 Rh8 21. Qh6#'
    game_35 = '1.e4 e5 2.Bc4 Nf6 3.Nf3 Nc6 4.O-O Bc5 5.d3 d6 6.Bg5 Bg4 7.h3 '\
        'h5 8.hxg4 hxg4 9.Nh2 g3 10.Nf3 Ng4 11.Bxd8 Bxf2+ 12.Rxf2 gxf2+ '\
        '13.Kf1 Rh1+ 14.Ke2 Rxd1 15.Nfd2 Nd4+ 16.Kxd1 Ne3+ 17.Kc1 Ne2#'
    game_36 = '1.e4 e5 2.f4 exf4 3.Nf3 g5 4.h4 g4 5.Ne5 Nf6 6.Bc4 d5 7.exd5 '\
        'Bd6 8.d4 Nh5 9.Bb5+ c6 10.dxc6 bxc6 11.Nxc6 Nxc6 12.Bxc6+ Kf8 '\
        '13.Bxa8 Ng3 14.Rh2 Bf5 15.Bd5 Kg7 16.Nc3 Re8+ 17.Kf2 Qb6 '\
        '18.Na4 Qa6 19.Nc3 Be5 20.a4 Qf1+ 21.Qxf1 Bxd4+ 22.Be3 Rxe3 '\
        '23.Kg1 Re1#'
    game_37 = '1. e4 e5 2. Nf3 Nc6 3. Bc4 Nf6 4. d3 Bc5 5. O-O d6 6. Bg5 h6 '\
        '7. Bh4 g5 8. Bg3 h5 9. Nxg5 h4 10. Nxf7 hxg3 11. Nxd8 Bg4 '\
        '12. Qd2 Nd4 13. h3 Ne2+ 14. Kh1 Rxh3+ 15. gxh3 Bf3#'
    game_38 = '1.d4 f5 2.c4 Nf6 3.Nc3 e6 4.Nf3 d5 5.e3 c6 6.Bd3 Bd6 7.O-O O-O '\
        '8.Ne2 Nbd7 9.Ng5 Bxh2+ 10.Kh1 Ng4 11.f4 Qe8 12.g3 Qh5 13.Kg2 '\
        'Bg1 14.Nxg1 Qh2+ 15.Kf3 e5 16.dxe5 Ndxe5+ 17.fxe5 Nxe5+ 18.Kf4 '\
        'Ng6+ 19.Kf3 f4 20.exf4 Bg4+ 21.Kxg4 Ne5+ 22.fxe5 h5#'
    game_39 = '1.e4 {Notes by Frank Marshall} e5 2.Nf3 Nc6 3.Bc4 Bc5 4.b4 Bb6'\
        '{Declining the gambit. This is supposed to be better for Black'\
        'than the acceptance. However, White gets dangerous attacks in'\
        'both branches} 5.c3 {To support d4, but to slow. 5 O-O is'\
        'stronger. Another good suggestion by Ulvestad is 5 a4 followed'\
        'by Ba3.} d6 6.O-O Bg4 7.d4 exd4 8.Bxf7+ {?} Kf8 {? Black'\
        'should have accepted. The sacrifice is unsound.} 9.Bd5 Nge7'\
        '{9...Nf6 is better as after 10 h3 Black could play 10...Bxf3'\
        'without the dangerous recapture by the White queen with a'\
        'check. The text move enables White to finish with a killing'\
        'attack.} 10.h3 Bh5 11.g4 Bg6 12.Ng5 {!} Qd7 13.Ne6+ Ke8'\
        '14.Nxg7+ Kf8 15.Be6 Qd8 16.Bh6 Bxe4 17.Nh5+ Ke8 18.Nf6#'
    game_40 = '1. e4 e5 2. f4 d5 3. exd5 Qxd5 4. Nc3 Qd8 5. fxe5 Bc5 6. Nf3 '\
        'Bg4 7. Be2 Nc6 8. Ne4 Bb6 9. c3 Qd5 10. Qc2 Bf5 11. Nf6+ Nxf6 '\
        '12. Qxf5 Ne7 13. Qg5 Ne4 14. Qxg7 Bf2+ 15. Kf1 Rg8 16. Qxh7 '\
        'Bb6 17. d4 O-O-O 18. Qh6 Rh8 19. Qf4 Rdg8 20. Rg1 Ng6 21. Qe3 '\
        'Re8 22. Qd3 Nh4 23. Nxh4 Rxh4 24. h3 c5 25. Bg4+ f5 26. exf6+ '\
        'Rxg4 27. hxg4 Ng3+ 28. Qxg3 Qc4+ 29. Kf2 Qe2#'
    game_41 = '1.d4 d5 2.c4 e6 3.Nc3 Nc6 4.Nf3 Nf6 5.Bf4 Bd6 6.Bg3 Ne4 7.e3 '\
        'O-O 8.Bd3 f5 9.a3 b6 10.Rc1 Bb7 11.cxd5 exd5 12.Nxd5 Nxd4 '\
        '13.Bc4 Nxf3+ 14.gxf3 Nxg3 15.Ne7+ Kh8 16.Ng6+ hxg6 17.hxg3+ '\
        'Qh4 18.Rxh4#'
    game_42 = '1. e4 e5 2. Nf3 Nc6 3. Bc4 Nf6 4. d4 exd4 5. O-O Nxe4 6. Re1 '\
        'd5 7. Bxd5 Qxd5 8. Nc3 Qa5 9. Nxd4 Nxd4 10. Qxd4 f5 11. Bg5 '\
        'Qc5 12. Qd8+ Kf7 13. Nxe4 fxe4 14. Rad1 Bd6 15. Qxh8 Qxg5 '\
        '16. f4 Qh4 17. Rxe4 Bh3 18. Qxa8 Bc5+ 19. Kh1 Bxg2+ 20. Kxg2 '\
        'Qg4+ 21. Kf1 Qf3+ 22. Ke1 Qf2#'
    game_43 = '1. e4 c6 2. d4 d5 3. Nc3 dxe4 4. Nxe4 Nf6 5. Qd3 e5 6. dxe5 '\
        'Qa5+ 7. Bd2 Qxe5 8. O-O-O Nxe4 9. Qd8+ Kxd8 10. Bg5+ Kc7 '\
        '11. Bd8#'
    game_44 = '1. f4 e5 2. fxe5 d6 3. exd6 Bxd6 4. Nf3 g5 5. h3 Bg3#'
    game_45 = '1. f4 e5 2. fxe5 d6 3. exd6 Bxd6 4. Nf3 h5 5. g3 h4 6. Nxh4 '\
        'Rxh4 7. gxh4 Qxh4#'
    game_46 = '1.e4 e6 2.d4 d5 3.Nd2 h6 4.Bd3 c5 5.dxc5 Bxc5 6.Ngf3 Nc6 7.O-O '\
        'Nge7 8.Qe2 O-O 9.Nb3 Bb6 10.c3 dxe4 11.Qxe4 Ng6 12.Bc4 Kh8 '\
        '13.Qc2 Nce5 14.Nxe5 Nxe5 15.Be2 Qh4 16.g3 Qh3 17.Be3 Bxe3 '\
        '18.fxe3 Ng4 19.Bxg4 Qxg4 20.Rad1 f6 21.Nd4 e5 22.Nf5 Be6 23.e4 '\
        'Rfd8 24.Ne3 Qg6 25.Kg2 b5 26.b3 a5 27.c4 bxc4 28.bxc4 Qh5 '\
        '29.h4 Bd7 30.Rf2 Bc6 31.Nd5 Rab8 32.Qe2 Qg6 33.Qf3 Rd7 34.Kh2 '\
        'Rdb7 35.Rdd2 a4 36.Qe3 Bd7 37.Qf3 Bg4 38.Qe3 Be6 39.Qf3 Rb1 '\
        '40.Ne3 Rc1 41.Rd6 Qf7 42.Rfd2 Rbb1 43.g4 Kh7 44.h5 Rc3 45.Kg2 '\
        'Rxe3 46.Qxe3 Bxg4 47.Rb6 Ra1 48.Qc3 Re1 49.Rf2 Rxe4 50.c5 Bxh5 '\
        '51.Rb4 Bg6 52.Kh2 Qe6 53.Rg2 Bf5 54.Rb7 Bg4 55.Rf2 f5 56.Rb4 '\
        'Rxb4 57.Qxb4 e4 58.Qd4 e3 59.Rf1 Qxa2+ 60.Kg3 Qe2 61.Qf4 Qd2 '\
        '62.Qe5 e2 63.Rg1 h5 64.c6 f4+ 65.Kh4 Qd8+ 66.Qg5 Qxg5+ 67.Kxg5 '\
        'f3 68.c7 f2 69.Rxg4 f1Q 70.c8Q Qf6+ 71.Kxh5 Qh6#'
    game_47 = '1.e4 e5 2.Nc3 Nf6 3.f4 d5 4.fxe5 Nxe4 5.Nf3 Bb4 6.Qe2 Bxc3 '\
        '7.bxc3 Bg4 8.Qb5+ c6 9.Qxb7 Bxf3 10.Qxa8 Bxg2 11.Be2 Qh4+ '\
        '12.Kd1 Nf2+ 13.Ke1 Nd3+ 14.Kd1 Qe1+ 15.Rxe1 Nf2#'
    game_48 = '1. e4 e5 2. Nf3 Nc6 3. Bb5 Nf6 4. O-O Nxe4 5. Re1 Nd6 6. Nxe5 '\
        'Be7 7. Bf1 O-O 8. d4 Nf5 9. c3 d5 10. Qd3 Re8 11. f4 Nd6 '\
        '12. Re3 Na5 13. Nd2 Nf5 14. Rh3 Nh4 15. g4 Ng6 16. Rh5 Nc6 '\
        '17. Ndc4 dxc4 18. Qxg6 hxg6 19. Nxg6 fxg6 20. Bxc4+ Kf8 '\
        '21. Rh8#'
    game_49 = '1. Nf3 Nc6 2. e4 e5 3. d4 exd4 4. c3 dxc3 5. Bc4 cxb2 6. Bxb2 '\
        'Bb4+ 7. Nc3 Nf6 8. Qc2 O-O 9. O-O-O Re8 10. e5 Ng4 11. Nd5 a5 '\
        '12. Nf6+ gxf6 13. Bxf7+ Kf8 14. Qxh7 Ngxe5 15. Nh4 Ne7 '\
        '16. Bxe5 fxe5 17. Rd3 Ra6 18. Rg3 Ba3+ 19. Kd1 Ng6 20. Qg8+ '\
        'Ke7 21. Nf5+ Kf6 22. Qxg6#'

    legal_checkmates = [game_1, game_2, game_3, game_4, game_5, game_6, game_7, game_8, game_9,
                        game_10, game_11, game_12, game_13, game_14, game_15, game_16, game_17,
                        game_18, game_19, game_20, game_21, game_22, game_23, game_24, game_25,
                        game_26, game_27, game_28, game_29, game_30, game_31, game_32, game_33,
                        game_34, game_35, game_36, game_37, game_38, game_39, game_40, game_41,
                        game_42, game_43, game_44, game_45, game_46, game_47, game_48, game_49]


def strip_to_scripts(text):
    new_text = text
    new_text = re.sub(r'\{.*?\}', '', new_text)
    new_text = re.sub(r'\d?\d\.\.?\.?', ' ', new_text)

    moves = new_text.split()
    white_script, black_script = [], []
    while moves:
        white_script.append(moves.pop(0))
        if moves:
            black_script.append(moves.pop(0))

    return white_script, black_script


def test():
    """ Misc test function - contains arbitrary code for testing """
    board = Board()
    # print(board)

    player1, player2 = Random('Player1', 'White'), Random('Player2', 'Black')

    play_a_game(board, player1, player2)


def test_checkmates(legal_checkmates):
    """ Loads 49 games ending in checkmate into the play_a_game function """
    for index, game in enumerate(legal_checkmates):
        board = Board()
        white_script, black_script = strip_to_scripts(game)
        player1, player2 = Scripted('Player1', 'White', white_script), Scripted('Player2', 'Black', black_script)

        board, player_of_last_move = play_a_game(board, player1, player2)
        if board.checkmate:  # game ended in checkmate
            print(f'game {index + 1} PASSED!')
        else:  # game did not end in checkmate
            print(f'game {index + 1} FAILED!')


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




