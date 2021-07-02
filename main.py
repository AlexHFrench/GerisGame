# Gerry's Game
#   ...enjoy!


"""
NOTE:
    board.squares is an array: board.squares[rank][file]
        [
        [a, b, c, d, e, f, g, h],
        [a, b, c, d, e, f, g, h],
        [a, b, c, d, e, f, g, h],
        [a, b, c, d, e, f, g, h],
        [a, b, c, d, e, f, g, h],
        [a, b, c, d, e, f, g, h],
        [a, b, c, d, e, f, g, h],
        [a, b, c, d, e, f, g, h]
        ]
    Significance: the indices of ranks are INVERTED!
        Rank 1 has index 7!
        Rank 8 has index 0!
    By convention in the below code:
        'row'; the integer index(0-7) of the board.squares array pertaining to the ->
        'rank'; an element of the board.squares array, containing pieces and empty squares
        'col'; the integer index(0-7) of the boar.squares array pertaining to the file
        'board location'; the pair of indices (row, col) indexing a square (board.squares[row][col])
        'SAN location'; a string of length two indicating a square on the board in Standard Algebraic Notation

"""
""" IMPORTS & GLOBAL CONSTANTS  ------------------------------------------------------------- IMPORTS & GLOBAL CONSTANTS
"""

import Pieces
from Menus import *
from Exceptions import *
from math import floor


""" GAME CONTROL FLOW -------------------------------------------------------------------------------- MAIN CONTROL FLOW 
"""


def disambiguate(candidates, disambiguation):
    """ Takes two elements:
            List of pieces to choose from,
            String of form:
                "letter" (a-h) | "number" (1-8) | "letter + number"  :  length 1-2
        Will absolutely crash if inputs incorrectly formatted
    """
    if len(disambiguation) == 1:  # if only one character..
        if disambiguation.isalpha():  # ..and it's a letter..
            col = Globals.FILES[disambiguation]  # then it's a file
            results = [x for x in candidates if x.location[1] == col]  # sort by piece.location information
        if disambiguation.isnumeric():  # sort by piece.location information
            results = [x for x in candidates if x.location[0] == 8 - int(disambiguation)]
    else:  # two characters..
        loc = list(disambiguation)
        results = [x for x in candidates if x.location == loc]  # sort by piece.location information
    return results


def decompose_and_assess(board, candidate):
    """ Returns the all relevant move-execution information OR throws exception.
            -> active_piece, active_piece_type, target_location, is_capture, promotion_type, castle_direction
    """

    # if the input SAN notation fails to validate..
    if not validate_san(candidate):
        raise InvalidInput('Move notation failed to validate, potential syntax issue\n')  # raise an exception

    # if the input SAN is good..
    else:
        active_piece_type, disambiguation, is_capture, target_san, \
            promotion_type, _, castle_direction = decompose_san(candidate)  # decompose it into elements

        # if elements indicate we are castling.. specify the target_location
        if castle_direction:
            target_sans = target_san.split()
            if board.player_turn == 'White':  # the target square depends on colour of active_player's king
                target_san = target_sans[0]
            else:  # if player_turn 'Black':
                target_san = target_sans[1]

        # convert target_location into board coords
        target_location = convert_san2board(target_san)  # determine target location coords

        # determine which pieces are capable of making the move
        active_pieces = board.get_pieces(board.player_turn, active_piece_type, target_location)

        # if NO pieces able to make such a move..
        if not active_pieces:  # print some debugging stuff..
            raise InvalidInput('No piece able to execute such a move\n')  # and raise an exception
        # if ONLY ONE piece can make the move..
        elif len(active_pieces) == 1:
            active_piece, = active_pieces  # return it
        # if MORE THAN ONE piece meets criteria: [colour, type, vision]..
        else:
            active_pieces = disambiguate(active_pieces, disambiguation)  # disambiguate
            try:
                active_piece, = active_pieces  # there should now only be 1 piece..
            except ValueError:  # if not raise an exception
                raise InvalidInput('Disambiguation insufficient: more than one piece able to make this move\n')

    return active_piece, active_piece_type, target_location, is_capture, promotion_type, castle_direction


def squares_in_direction(start_loc, end_loc):
    """ Returns (x, y) positions occurring EN-ROUTE from a given starting location to an target location
        Example:    squares_in_direction((1, 1), (3, 3))     >>     [(1,1), (2,2)]
    """
    start_row, start_col = start_loc
    end_row, end_col = end_loc
    row_diff, col_diff = end_row - start_row, end_col - start_col

    if row_diff != 0:  # if the locations are not on the same row
        r = range(start_row, end_row + Utils.sign(row_diff), Utils.sign(row_diff))
    else:
        r = [start_row for _ in range(abs(col_diff) + 1)]
    if col_diff != 0:  # if the locations are not in the same column
        c = range(start_col, end_col + Utils.sign(col_diff), Utils.sign(col_diff))
    else:
        c = [start_col for _ in range(abs(row_diff) + 1)]
    locations = list(zip(r, c))
    if end_loc in locations:
        locations.remove(end_loc)
    # Knights cannot be interceded, only captured
    knight_move_checker = [1, 2]
    if sorted([abs(row_diff), abs(col_diff)]) == knight_move_checker:
        locations = [start_loc]

    return locations


def promote_pawn(board, active_piece, target_location, promotion_type):
    """ Updates a Board with a promoting Pawn. Does not return
    """
    board.sideboard.append(active_piece)  # Move Pawn to sideboard
    r, c = target_location
    # Initialise and place the promotion piece
    board.squares[r][c] = eval('Pieces.'+promotion_type)(board.player_turn, board, target_location, has_moved=True)
    board.squares[r][c].temp = active_piece.temp  # Replace the Empty object into the new piece's .temp field


def convert_board2fen(board, tmp=False):
    """ Returns a FEN representation of a given board as a string.
        Does not modify the Board.
        "tmp" flag: Returns a truncated version with only first 4 FEN elements (board_rep, colour, castling, en_passant)
    """
    # GENERATE BOARD REPRESENTATION STRING
    empty_count, txt = 0, []
    for row in range(8):
        for col in range(8):
            square = board.squares[row][col]  # for each square on the board..
            if square.__class__.__name__ == 'Empty':  # ..if it's empty..
                empty_count += 1  # ..add it to a running total
            else:  # if it's a piece..
                if empty_count >= 1:  # ..with preceding empty squares..
                    txt.append(str(empty_count))  # ..append the number of those empty squares..
                    empty_count = 0  # ..and reset the running total
                letter = Globals.TYPES[square.colour][square.__class__.__name__]  # then note the type and colour of the piece
                txt.append(letter)
        if empty_count >= 1:  # if no piece at end of a row
            txt.append(str(empty_count))  # append the empty count
            empty_count = 0  # and reset
        if row != 7:  # if at the end of a row, apart from the last, note that
            txt.append('/')

    # COLOUR-TO-MOVE
    letter = 'w' if board.player_turn == 'White' else 'b'
    txt.append(' ' + letter)

    # CASTLING LEGALITIES
    txt.append(' ')
    row, sides = [7, 0], {7: 'King', 0: 'Queen'}
    for index, colour in enumerate(Globals.COLOURS):  # for each colour.. (white first)
        king_sq = board.squares[row[index]][4]  # check the king's home square
        if king_sq.__class__.__name__ == 'King' and not king_sq.has_moved:  # if it is a king, which has not moved..
            for col, side in sides.items():  # go on to check its rooks..
                rook_sq = board.squares[row[index]][col]  # for each side.. (king-side first)
                if rook_sq.__class__.__name__ == 'Rook' and not rook_sq.has_moved:  # if it is a rook, which has not moved..
                    letter = Globals.TYPES[colour][sides[col]]  # note that castling on that side is legal
                    txt.append(letter)
    if txt[-1] == ' ':  # note if no legal castles on board
        txt.append('-')

    # EN PASSANT SQUARE DETAILS
    if board.passant_loc:
        san = convert_board2san(board.passant_loc)
        txt.append(' ' + san)
    else:
        txt.append(' -')

    # FUNCTION TERMINATION - truncated version of FEN for use in 3-fold-rep calculation
    if tmp:  # for 3-fold-rep this is all we need..
        return ''.join(txt)

    # HALF-MOVE CLOCK (Draw counter)
    hmc = str(int(board.draw_count * 2))
    txt.append(' ' + hmc)

    # FULL-MOVE NUMBER (Turn counter)
    fmn = str(floor(board.turn_count))
    txt.append(' ' + fmn)

    return ''.join(txt)


def three_fold_rep():
    """ Returns True if there has been a Draw by 3-fold-repetition """
    with open('tmp.txt', 'r') as tmp:
        lines = tmp.readlines()
        # If there are 3 identical copies of the last element then we have draw by 3-fold-repetition
        return lines.count(lines[-1]) == 3 if lines else False


def prepare_for_game_end(board):
    """ Prepares a Board object for termination of a game.
        Board attributes such as .turn_count are modified after the last move but before the next move.
        The Checkmate/Draw/Player resignation etc. happen in the intervening time.
        This function, then, reverses the end-step board update that happen in preparation to return the board
            at the end of a game.
        (This essentially only happens because we increment turns by 0.5 instead of 1.0)
    """
    board.turn_count -= 0.5


def agent_turn(board, active_player, passive_player):
    """ Logic for a single agent's turn.
        Takes the Board object and both players: active player first, then the passive player.
        Does not return.
    """
    # Print and update board
    print(board)
    board.update_pieces()  # This is the PRIMARY BOARD UPDATE in the turn-by-turn cycle of play

    # General board assessment: Checkmate, Draw, Checks
    board.is_checkmate(passive_player)  # (this updates board.active_player_in_check status)
    board.is_draw(passive_player)
    if board.active_player_in_check:
        print(f'                 {active_player} is in CHECK!')
    else:
        print('\n')

    # Present agent opportunity to move/enter command..
    print(f"{active_player} to move:")
    while True:  # Catches anomalous moving-into-check type illegal moves and checkmates/draws by process of elimination

        # Get agent move/input - contains a terminate program option
        active_piece, active_piece_type, target_location, is_capture, \
            promotion_type, castle_direction = active_player.get_input(board)

        try:  # Execute move on board
            board.move(active_piece, active_piece_type, target_location, is_capture, promotion_type,
                       castle_direction)

        except IllegalMove as II:  # If the move would be Illegal..
            if target_location in active_piece.avail_moves:  # remove it from the set of possible moves
                active_piece.avail_moves.remove(target_location)
            elif target_location in active_piece.avail_captures:  # remove it from the set of possible moves
                active_piece.avail_captures.remove(target_location)
            # Re-check for checkmates and draws..
            board.is_checkmate(passive_player)  # (this updates board.active_player_in_check status)
            board.is_draw(passive_player)
            print(f"{active_player}'s king would have been in Check!")
            print("You'll have to choose another move.\n")

        else:  # If the move was Legal, it has now executed on the board..
            if board.turn_count != board.passant_count:  # if the en passant timer did not start this half-turn..
                board.passant_loc = tuple()  # ..then there is no legal en passant on the board
                board.passant_count = 0
            board.active_player_in_check = False  # by definition, active_player is not in Check
            active_piece.has_moved = True  # mark the active piece as having moved
            board.draw_count += 0.5  # increment draw counter
            if active_piece.__class__.__name__ == 'Pawn':  # if a Pawn was the active piece
                board.draw_count = 0  # reset draw counter
            elif is_capture:  # if there was a capture
                board.draw_count = 0  # reset draw counter

            """ the following breaks from the turn-loop if:
            ..a legal move has been executed on the board or
            ..a Checkmate or Draw was already on-board at the outset of this turn-loop and was only
                discovered through a process of eliminating moves-into-check """
            break


def play_a_game(board, player1, player2):
    """ The Master logic for execution of a game.
        Takes a live Board object and two agents >> White, Black
        This function handles the management of the tmp.txt file; used to keep track of board states for 3-fold-rep.
        Does not return.
    """

    players, game_on = [player1, player2], True

    # Initialise a clean 'tmp.txt' file
    with open('tmp.txt', 'w') as tmp:
        tmp.write(convert_board2fen(board, tmp=True) + ' \n')

    # START THE GAME
    while game_on:
        print(f'                                   Turn No.  : {floor(board.turn_count)}.')
        try:
            agent_turn(board, *players)  # Execute the active_player's turn
        except Checkmate as Cm:
            txt, board, player_of_final_move = Cm.args
            print(f'                CHECKMATE! {player_of_final_move} wins! After {floor(board.turn_count)} moves')
            print('\n                 GAME OVER!\n')
            game_on = False
            continue
        except Draw as D:
            txt, board, player_of_final_move = D.args
            print(f'                        {txt} After {floor(board.turn_count)} moves')
            print('\n                         GAME OVER!\n')
            game_on = False
            continue

        board.turn_count += 0.5  # half-step the turn counter
        players.reverse()  # Swap the active_player with the passive_player
        board.player_turn, = set(Globals.COLOURS) - {board.player_turn}  # Swap the colour of the player who is on-turn

        # Update tmp.txt
        if board.draw_count:  # If there was not a pawn move or capture last turn..
            with open('tmp.txt', 'a') as tmp:  # append another truncated FEN to the 3-fold-rep tracker
                tmp.write(convert_board2fen(board, tmp=True) + ' \n')
        else:  # If there was..
            with open('tmp.txt', 'w') as tmp:  # we overwrite this most recent state
                tmp.write(convert_board2fen(board, tmp=True) + ' \n')

    return board, player_of_final_move


""" MAIN CONTROL FLOW -------------------------------------------------------------------------------- MAIN CONTROL FLOW 
"""


def main():
    """ Main control logic of the program
            - chose board starting position from selection of variants, saved games or FENs
            - chose type of agents to play the game (human, random, etc)
            - play the game out
        Repeat until user closes program
    """

    # META PROGRAM LOOP
    while True:

        decision = False
        while not decision:
            result = player_wants_game()  # Prompt player as to what kind of game they would like to play.
            print(result)

            if result in range(1, 5):
                board = set_board(result)
                decision = True
                continue

            elif result == 5:  # Load from local Saved Game
                print('Apologies, feature not yet implemented.\n')
                pass
            elif result == 6:  # load from local Saved FEN
                print('Apologies, feature not yet implemented.\n')
                pass
            elif result == 7:  # load from a FEN manually entered into the terminal
                print('Please enter the FEN                                                              <back>')
                fen = input('          :    ')
                if fen.isalpha():  # a valid FEN will always contain numbers
                    if fen.lower() == 'back':  # provides the ability to drop back to the previous menus
                        continue
                try:
                    board = convert_fen2board(fen)  # attempt to generate a Board from the FEN
                except InvalidInput as II:
                    print({II})
                    pass
                except:
                    print('Something went wrong, FEN likely incorrectly formatted')
                    pass
                else:
                    decision = True
                    continue
        # Board now generated..
        print(board)
        # Initialise Agents..
        player1, player2 = assign_players()  # player1: "White" , player2: "Black"
        players = [player1, player2]
        # Can happen when loading game from FEN
        if board.player_turn == 'Black':
            players.reverse()

        # Play the game
        play_a_game(board, *players)

        # Loops until player terminates the program


""" MAIN LOGIC ---------------------------------------------------------------------------------------------- MAIN LOGIC
"""
if __name__ == '__main__':

    main()


