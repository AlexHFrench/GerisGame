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

from Exceptions import *
from pathlib import Path
from timeit import default_timer as timer
import re
import sys
import copy
import random
import os
import numpy
import math

COLOURS = ('White', 'Black')

VALUES = {
    'Pawn': 1,
    'Rook': 5,
    'Knight': 3,
    'Bishop': 3,
    'King': 100,
    'Queen': 9,
}

LETTERS = {
    'P': 'Pawn',
    'R': 'Rook',
    'N': 'Knight',
    'B': 'Bishop',
    'K': 'King',
    'Q': 'Queen',
    'E': 'Empty',
}

TYPES = {
    'White': {
        'Pawn': 'P', 'Rook': 'R', 'Knight': 'N',
        'Bishop': 'B', 'King': 'K', 'Queen': 'Q'},
    'Black': {
        'Pawn': 'p', 'Rook': 'r', 'Knight': 'n',
        'Bishop': 'b', 'King': 'k', 'Queen': 'q'}
}

PATTERNS = {
    'Pawn': [(1, 1), (1, -1)],
    'Rook': [(1, 0), (0, 1), (-1, 0), (0, -1)],
    'Knight': [(1, 2), (2, 1), (-1, 2), (2, -1), (-2, 1), (1, -2), (-1, -2), (-2, -1)],
    'Bishop': [(1, 1), (1, -1), (-1, 1), (-1, -1)],
    'King': [(0, 1), (1, 0), (1, 1), (-1, 0), (0, -1), (-1, 1), (1, -1), (-1, -1)],
    'Queen': [(0, 1), (1, 0), (1, 1), (-1, 0), (0, -1), (-1, 1), (1, -1), (-1, -1)],
}

STEPS = {
    'Pawn': 1,
    'Rook': 7,
    'Knight': 1,
    'Bishop': 7,
    'King': 1,
    'Queen': 7,
}

# The following have been designated THE WRONG WAY AROUND for the purposes of appearing more visually correct
# on a white-black-inverted terminal window
UNICODES = {
    'Black': {
        'Pawn': '♙',
        'Rook': '♖',
        'Knight': '♘',
        'Bishop': '♗',
        'King': '♔',
        'Queen': '♕',
    },
    'White': {
        'Pawn': '♟',
        'Rook': '♜',
        'Knight': '♞',
        'Bishop': '♝',
        'King': '♚',
        'Queen': '♛',
    },
}

# Columns on which pieces start the game
STANDARD_GAME = (0, 1, 2, 3, 4, 5, 6, 7)  # all pieces
KING_AND_PAWN_GAME = 4,  # only the king
MINOR_GAME = (1, 2, 4, 5, 6)  # minor pieces + king
MAJOR_GAME = (0, 3, 4, 7)  # major pieces + king

# Pieces in the order they appear on the board - could add Fischer-random at some point
BACK_LINE = ('Rook', 'Knight', 'Bishop', 'Queen', 'King', 'Bishop', 'Knight', 'Rook')

# Files
FILES = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

# Non-move commands player can enter during a game
IN_GAME_COMMANDS = ['resign', 'save', 'tmp', 'close']


""" BOARD & PIECE CLASSES ------------------------------------------------------------------------ BOARD & PIECE CLASSES
"""


class Board:
    """ This is the Board object for the game logic.
        It essentially handles all game calculations.
        If you have access to a given game's Board object you have access to nearly every piece of
            information pertaining to the board state and the capacity to continue a game from any position.
        Exceptions:
            - 3 fold repetition requires a tmp.txt file which is managed in the GAME-LOGIC section below
        Piece Objects & Empty Objects:
            - populate every square on the board at all time
            - have vision attributes which are informed by their movement rules in Chess
    """

    def __init__(self, piece_positions=range(8), pawn_positions=range(8)):
        self.sideboard, self.passant_loc = [], tuple()
        self.player_turn, self.turn_count, self.draw_count, self.passant_count = 'White', 1.0, 0, 0.0
        self.checkmate, self.active_player_in_check, self.draw = False, False, False
        colour_generator = white_black()

        # Generate empty board
        self.squares = [[Empty(next(colour_generator), location=(row, col)) for col in range(8)] for row in range(8)]

        # instantiate pieces
        for col in piece_positions:
            type_ = BACK_LINE[col]
            self.squares[0][col] = eval(type_)('Black', self, (0, col))
            self.squares[7][col] = eval(type_)('White', self, (7, col))
        for col in pawn_positions:
            self.squares[1][col] = Pawn('Black', self, (1, col))
            self.squares[6][col] = Pawn('White', self, (6, col))

        # initialise pieces
        self.update_pieces()

    def __str__(self):
        """ return a printable, human-readable string representation of the board in its current state
        """
        output = ''
        for index, rank in enumerate(self.squares):
            output += str(9 - (index + 1)) + '　'
            for square in rank:
                output += str(square) + '　'
            output += '\n'
        output += '   '
        for file in FILES:
            output += file + ' ' * 10  # ' '
        output += '\n'
        return output

    def clear(self):
        """ remove all pieces from an already extant Board object
        """
        colour_generator = white_black()
        self.squares = [[Empty(next(colour_generator), location=(row, col)) for col in range(8)] for row in range(8)]

    def update_pieces(self):
        """ This updates each piece; i.e. their legal moves in a given board state.
            Kings are updated last
            Of the Kings, he whose move it is updates last.
        """
        kings = list()
        for row, col in ((x, y) for x in range(8) for y in range(8)):  # for every square..
            square = self.squares[row][col]
            if isinstance(square, Piece):  # ..that contains a piece..
                square.location = (row, col)  # update its location attribute
                if isinstance(square, King):  # .. and unless it's a king..
                    kings.append(square)  # (which we handle below)
                    continue
                square.look(self)  # ..have it look at the board

        # This handles niche case where two kings are "fighting over" a square
        if kings:  # in the case no kings on board (eg. empty board)
            kings[0].clear_vision()  # ..clear King vision
            kings[1].clear_vision()  # ..clear King vision

            if kings[0].colour == self.player_turn:  # then reinstate vision..
                kings[1].look(self)  # with passive king first..
                kings[0].look(self)
            else:
                kings[0].look(self)
                kings[1].look(self)

    def get_pieces(self, colour=None, type_=None, move_vision=None, in_check_vision=None, expecting_one=False):
        """ Returns all pieces on the board which match the given criteria.
            move_vision - is supplied coordinate in a piece's available moves or captures
            in_check_vision - is a supplied coordinate in a piece's 'checking distance'
                            required for move-through-check and move-into-check situations
        """
        pieces = []
        for row in range(8):
            for col in range(8):
                square = self.squares[row][col]  # for all squares..
                if isinstance(square, Piece):  # if they contain a piece..
                    if colour is not None:
                        if square.colour != colour:  # ..and match a supplied colour..
                            continue
                    if type_ is not None:
                        if not isinstance(square, eval(type_)):  # ..and match a supplied type..
                            continue
                    if move_vision is not None:  # ..and match a supplied move or capture..
                        if move_vision not in square.avail_moves.union(square.avail_captures):
                            continue
                    if in_check_vision is not None:  # ..and match a supplied checking distance..
                        if in_check_vision not in square.check_vision:
                            continue
                    pieces.append(square)  # ..collect them
                    if expecting_one:  # if we are expecting to find only one piece..
                        return pieces  # ..return it now instead of later
        return pieces

    def blind_move(self, start_location, target_location):
        """ BLIND move of the contents of an initial location to a target location.
                - Other than the one-move duration of opportunity, the following handles the ENTIRE en passant procedure
                - No checks are made for legality of any kind!
                - Will ABSOLUTELY crash if no piece exists at the given initial location!
        """
        start_row, start_col = start_location
        active_piece = self.squares[start_row][start_col]
        end_row, end_col = target_location

        # BASIC MOVE LOGIC
        self.squares[start_row][start_col] = active_piece.temp  # replace Empty object in active_piece's location
        active_piece.temp = self.squares[end_row][end_col]  # store content of target_location in active_piece's .temp
        self.squares[end_row][end_col] = active_piece  # place active_piece in target_location

        # DOUBLE STEP PHASE (en passant)
        if isinstance(active_piece, Pawn):  # if there's a Pawn..
            if abs(start_row - end_row) == 2:  # ..making a double step..
                path = squares_in_direction(start_location, target_location)
                passant_location, = set(path) - {start_location}  # identify the 'single-step' square..
                self.passant_loc = passant_location  # ..update the en_passant flag..
                self.passant_count = self.turn_count  # ..and start the timer
                # THE FOLLOWING IS GHOST CODE, TO BE IMPLEMENTED IF X-FEN IS USED IN FUTURE!
                # see >> https://en.wikipedia.org/wiki/X-FEN#Encoding_en-passant
                # for i in range(-1, 2, 2):  # check left and right
                #     test_col = end_col + i
                #     if not legal(end_row, test_col):  # if the coord is legal..
                #         continue
                #     new_neighbour = self.squares[end_row][test_col]  # look at the square..
                #     # if there's an opposition Pawn..
                #     if isinstance(new_neighbour, Pawn) and new_neighbour.colour != active_piece.colour:
                #         path = squares_in_direction(start_location, target_location)
                #         passant_location, = set(path) - {start_location}
                #         self.passant_loc = passant_location  # ..update the en_passant flag
                #         self.passant_count = self.turn_count  # and start the timer

        # CAPTURE PHASE (en passant)
        if self.passant_loc == target_location:  # if the target square is the en passant location..
            if isinstance(active_piece, Pawn):  # ..and active_piece is a Pawn
                dir_ = active_piece.direction  # note which direction is "behind"
                row_behind = end_row + (-1 * dir_)  # ..and therefore which row is "behind"
                captured_pawn = self.squares[row_behind][end_col]  # select the captured pawn
                self.squares[row_behind][
                    end_col] = captured_pawn.temp  # place captured_pawn's Empty object into its previous location
                captured_pawn.temp = active_piece.temp  # target location's Empty object into captured_pawn's .temp
                active_piece.temp = captured_pawn  # ..and captured_pawn into active_piece's .temp field

    def test_move(self, active_piece, target_location):
        """ Creates a copy of the board and moves the active piece to the target location.
            A search is then made for any Checks - Returns TRUE if move IS LEGAL - i.e no Checks found
        """
        import copy

        test_board = copy.deepcopy(self)  # copy the board
        test_board.blind_move(active_piece.location, target_location)  # move the piece
        test_board.update_pieces()  # update all pieces
        checks, _ = test_board.get_checks()  # ..and looks for checks

        return active_piece.colour not in checks  # return True if move is legal

    def move(self, active_piece, active_piece_type, target_location,
             is_capture=False, promotion_type=None, castle_direction=None):
        """ Move active_piece from present location to target_location
            Empty [square] objects are stored in active_piece.temp while checks are made for legality of move
            In case of capture: active_piece.temp = target_piece s.t. target_piece.temp = Empty object
        """
        original_location = active_piece.location
        if self.test_move(active_piece, target_location):  # if the move would not leave King in check..
            self.blind_move(original_location, target_location)  # execute the move.

            # if it's a capture..
            if is_capture:
                self.sideboard.append(active_piece.temp)  # move captured_piece to board.sideboard
                active_piece.temp = active_piece.temp.temp  # replace taken piece's .temp onto the board

            # if it's a promotion..
            if promotion_type:
                promote_pawn(self, active_piece, target_location, promotion_type)  # make the promotion

            # if we're castling
            elif castle_direction:  # ..we now need to move the Rook
                if castle_direction == 'Queen':  # check in which direction to move..
                    start_col, end_col = 0, 3
                else:
                    start_col, end_col = 7, 5
                start_row, _ = active_piece.location
                self.blind_move((start_row, start_col), (start_row, end_col))  # ..and move the Rook
                self.squares[start_row][end_col].has_moved = True  # don't forget to mark it as having moved
        else:  # if the original move would not be legal..
            raise IllegalMove(f"{active_piece.colour}'s King would be in check!")  # raise an exception

    def get_checks(self):
        """ Returns: a list of colours currently in check, i.e. ['White', 'White'] for double check
                     a list of pieces currently giving check
            The returned elements are ordered such that zip(elem1, elem2) would form matching pairs.
        """
        checks, checking_pieces = [], []
        for colour in COLOURS:  # For each colour..
            king, = self.get_pieces(colour, 'King', expecting_one=True)  # find the King..
            king_location = king.location  # and his location
            # list opposition pieces with vision of the King, i.e. giving check
            checking_pieces.extend(self.get_pieces(king.opp_colour, in_check_vision=king_location))
        for piece in checking_pieces:  # For each piece giving check..
            checks.append(piece.opp_colour)  # indicate the colour of the king in check

        return checks, checking_pieces

    def is_checkmate(self, last_player_to_move):
        """ Raises relevant Checkmate exception if checkmate found | Otherwise passes without action
            Exception raised has args: string(checkmate text), board_object, victorious player_object
        """
        checks, checking_pieces = self.get_checks()

        # If active_player's King is in check..
        if self.player_turn in checks:
            self.active_player_in_check = True
            king, = self.get_pieces(self.player_turn, 'King', expecting_one=True)

            # Check king's possible moves
            for move_set in [king.avail_moves, king.avail_captures]:
                # if the king thinks he can move..
                while move_set:  # ..while he still has candidate moves remaining
                    move = move_set.pop()  # remove a move from the list of possible moves..
                    if self.test_move(king, move):  # ..and establish whether it avoids Check
                        move_set.add(move)  # ..if it does, re-enable the move
                        return  # if avoids Check: no checkmate
                    else:
                        pass  # if not: possible checkmate

            # At this point we have determined the King has no legal moves
            for piece in checking_pieces:  # in which case, for each piece checking the king..
                # determine the 'path' of the check to the King, not including the king's location
                locations = squares_in_direction(piece.location, king.location)
                for loc in locations:  # for each location..
                    for defender in self.get_pieces(king.colour, move_vision=loc):  # if a friendly piece can reach it..
                        if self.test_move(defender, loc):  # ..can they reach it legally?
                            return  # if so defense is good: no checkmate
                        else:
                            pass  # if not: possible checkmate
                    else:
                        pass  # no defender to step in: possible checkmate
        else:
            return  # No checks: no checkmate

        prepare_for_game_end(self)
        self.checkmate = True
        raise Checkmate('Checkmate on board!', self, last_player_to_move)

    def is_draw(self, last_player_to_move):
        """ Raises relevant Draw exception if a condition is met | Otherwise passes without action
            Exception raised has args: string(Draw text), board_object, player_object-who-last-moved
            50-move-rule, Stalemate, Insufficient mating material & 3-fold-rep. all implemented
        """
        # 50 MOVE RULE
        if self.draw_count == 50.0:
            prepare_for_game_end(self)
            raise Draw('Draw by 50 move rule!', self, last_player_to_move)

        # 3 FOLD REPETITION
        if three_fold_rep():
            with open('tmp.txt', 'r') as tmp:
                lines = tmp.readlines()
                print(''.join(lines))
            prepare_for_game_end(self)
            raise Draw('Draw by 3 fold repetition!', self, last_player_to_move)

        # STALEMATE
        draw = True
        pieces = self.get_pieces(self.player_turn)
        for piece in pieces:  # check every piece belonging to active player
            if piece.avail_moves == set() and piece.avail_captures == set():
                pass  # if none turn out to have a legal move then it is a draw
            else:
                draw = False  # if any have a move: no draw
                break
        if draw:
            prepare_for_game_end(self)
            raise Draw('Draw by stalemate!', self, last_player_to_move)

        # INSUFFICIENT MATERIAL
        white_count, black_count = 0, 0
        for row in range(8):  # for all squares of the board
            for col in range(8):
                square = self.squares[row][col]
                # if there is a Pawn, Queen or Rook..
                if (isinstance(square, Pawn) or isinstance(square, Queen)) or isinstance(square, Rook):
                    return  # no draw
                # it it's a minor piece..
                if isinstance(square, Knight) or isinstance(square, Bishop):
                    if square.colour == 'White':
                        white_count += 1  # ..count white instances
                    else:
                        black_count += 1  # ..and black instances
        if white_count >= 2 or black_count >= 2:  # if either colour has two or more minor pieces
            return  # then no draw
        else:
            prepare_for_game_end(self)
            raise Draw('Draw by insufficient material!', self, last_player_to_move)


class Empty:
    """ Empty square - place holder object. Has colour and location.
        It is possible that these are almost entirely redundant and that, with small change to a small number of
            functions they could be entirely removed from the game.
    """

    def __init__(self, colour, location, has_moved=None):
        """ This has fields that are not used so that initialisation logic
                can be commensurate with that of normal Pieces
        """
        self.colour = colour
        self.location = location
        self.has_moved = has_moved

    def __str__(self):
        return '―'

    def __repr__(self):
        san_loc = convert_board2san(self.location)
        return '― >> ' + san_loc


class Piece:
    """ Parent class for all Pieces including Pawns.
        They have:
            - Colour - Location - Has-Moved boolean - Unicode character for board printing
            - A movement pattern which encodes the piece's movement rules in Chess
                this includes a "steps" attribute which indicates how "far" they can see
            - available moves (empty squares within their vision)
            - available captures (opposition pieces within their vision)
            - supporting (friendly pieces within their vision)
            - check vision (any square which exists within their capture vision)
                this is relevant for Pawns and Kings whose available
                captures are not a 1-1 mapping to their capture vision
    """

    def __init__(self, colour, board, location, has_moved=False):
        self.avail_moves, self.avail_captures, self.supporting, self.check_vision = set(), set(), set(), set()
        self.pattern, self.steps = None, None  # pattern of movement allowed in the rules
        self.colour = colour
        self.opp_colour, = set(COLOURS) - {self.colour}
        self.location = location
        self.temp = board.squares[location[0]][location[1]]  # important during piece capture and elsewhere
        self.has_moved = has_moved  # important for castling, double-step pawn moves and captures en-passant
        self.char = UNICODES[self.colour][self.__class__.__name__]

    def __str__(self):
        return self.char

    def __repr__(self):
        avail_moves = [convert_board2san(x) for x in self.avail_moves]
        avail_captures = [convert_board2san(x) for x in self.avail_captures]
        supporting = [convert_board2san(x) for x in self.supporting]
        check_vision = [convert_board2san(x) for x in self.check_vision]

        return f'\n {self} \n'\
            f'colour: {self.colour}\n'\
            f'location: {self.location}\n'\
            f'.. in SAN: {convert_board2san(self.location)}\n' \
            f'.. in temp: {repr(self.temp)}\n' \
            f'available moves: {avail_moves}\n'\
            f'available captures: {avail_captures}\n' \
            f'supporting: {supporting}\n' \
            f'check_vision: {check_vision}\n' \
            f'has moved: {self.has_moved}'

    def look(self, board):
        """ Populates:
            self.check_vision
            self.avail_moves
            self.avail_captures
            self.supporting
        """
        self.clear_vision()
        # According to movement rules..
        for i, j in self.pattern:
            new_row = self.location[0] + i
            new_col = self.location[1] + j

            # ..and for as far as they can see..
            for _ in range(self.steps):
                # if the square is on the board..
                if not legal(new_row, new_col):
                    break
                self.check_vision.add((new_row, new_col))  # ..add coord to .check_vision
                square = board.squares[new_row][new_col]
                # ..and if square is empty..
                if isinstance(square, Empty):
                    self.avail_moves.add((new_row, new_col))  # add coord to .avail_moves
                    new_row += i  # and increment for next square
                    new_col += j  # and increment for next square
                # if it's an opposition piece..
                elif square.colour != self.colour:
                    self.avail_captures.add((new_row, new_col))  # ..add coord to .avail_captures
                    break
                # if it's an allied piece..
                else:
                    self.supporting.add((new_row, new_col))  # ..add coord to .supporting
                    break

    def clear_vision(self):
        """ Removes a piece's vision of the board completely """
        self.avail_moves, self.avail_captures, self.supporting, self.check_vision = set(), set(), set(), set()


class Pawn(Piece):
    """ Pawns inherit from Piece()
        Due to their movement patterns being do distinct from other pieces in the game the Pawn's look() method fully
            overwrites that of the parent class
        Additionally, they have:
            - Direction. Which is to say they are not omni-directional w.r.t the rules. Unlike all other pieces.
    """

    def __init__(self, colour, board, location, has_moved=False):
        super().__init__(colour, board, location, has_moved)
        self.pattern, self.steps = [(1, 1), (1, -1)], 1
        if colour == 'White':
            self.direction = -1  # used to orient the piece on the board; pawns are not omni-directional
        else:
            self.direction = 1

    def look(self, board):
        """ Additionally to parent class:
                - Populates available captures with squares pertaining to captures En Passant
        """
        self.clear_vision()
        new_row, _ = row, col = self.location

        # On their first move they are privileged with a double move should they chose it
        if not self.has_moved:
            self.steps = 2
        else:
            self.steps = 1

        # PAWNS move straight forward..
        for _ in range(self.steps):
            new_row += self.direction  # look one square ahead..
            if not legal(new_row, col):  # if it's on the board..
                continue
            square = board.squares[new_row][col]
            if isinstance(square, Empty):  # ..and empty..
                self.avail_moves.add((new_row, col))  # add it to .avail_moves
            else:
                break

        # PAWNS capture diagonally..
        for i, j in self.pattern:  # for each forward-diagonal-direction..
            new_row = self.location[0] + i * self.direction  # step once
            new_col = self.location[1] + j * self.direction  # step once
            # if square is on the board..
            if not legal(new_row, new_col):
                continue
            self.check_vision.add((new_row, new_col))  # ..add coord to .check_vision
            # if the square is the en passant location..
            if board.passant_loc == (new_row, new_col):
                self.avail_captures.add((new_row, new_col))  # ..add it to .avail_captures
            square = board.squares[new_row][new_col]
            # if there is a piece there..
            if isinstance(square, Piece):
                if square.colour != self.colour:  # and it's an opposition piece ..
                    self.avail_captures.add((new_row, new_col))  # ..add coord to .avail_captures
                else:  # if it's an allied piece..
                    self.supporting.add((new_row, new_col))  # ..add coord to .supporting


class Rook(Piece):
    """ Rooks inherit from Piece()
        They are very regular in their behaviour and so do not have much additional function over their parent
    """

    def __init__(self, colour, board, location, has_moved=False):
        super().__init__(colour, board, location, has_moved)
        self.pattern = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.steps = 7


class Knight(Piece):
    """ Knights inherit from Piece()
        They are very regular in their behaviour and so do not have much additional function over their parent
    """

    def __init__(self, colour, board, location, has_moved=False):
        super().__init__(colour, board, location, has_moved)
        self.pattern = [(1, 2), (2, 1), (-1, 2), (2, -1), (-2, 1), (1, -2), (-1, -2), (-2, -1)]
        self.steps = 1


class Bishop(Piece):
    """ Bishops inherit from Piece()
        They are very regular in their behaviour and so do not have much additional function over their parent
    """

    def __init__(self, colour, board, location, has_moved=False):
        super().__init__(colour, board, location, has_moved)
        self.pattern = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        self.steps = 7


class King(Piece):
    """ Knights inherit from Piece()
        Due to their movement patterns being do distinct from other pieces in the game the King's look() method fully
            overwrites that of the parent class
    """

    def __init__(self, colour, board, location, has_moved=False):
        super().__init__(colour, board, location, has_moved)
        self.pattern = [(0, 1), (1, 0), (1, 1), (-1, 0), (0, -1), (-1, 1), (1, -1), (-1, -1)]
        self.castle_pattern = [(0, 1), (0, -1)]
        self.steps = 1

    def look(self, board):
        """ Additionally to parent class:
                - Populates available moves with squares pertaining to legal Castling maneuvers.
                    In these cases the Rook has no knowledge of the potential of Castling and is moved
                    'manually' by the game logic embedded in the Board.move() method.
                - Prevents population of available moves and available captures with moves that
                    would result in the King being in Check.
        """
        self.clear_vision()

        # NORMAL MOVEMENT
        for i, j in self.pattern:
            new_row = self.location[0] + i
            new_col = self.location[1] + j

            # If the square is on the board..
            if not legal(new_row, new_col):
                continue
            self.check_vision.add((new_row, new_col))  # ..add coord to .check_vision
            square = board.squares[new_row][new_col]
            # If the coord is empty..
            if isinstance(square, Empty):
                # and is not covered..
                if board.get_pieces(self.opp_colour, in_check_vision=(new_row, new_col)):
                    continue
                self.avail_moves.add((new_row, new_col))  # ..add coord to .avail_moves
            # If it's an opposition piece..
            elif square.colour != self.colour:
                # and is not covered..
                if board.get_pieces(self.opp_colour, in_check_vision=(new_row, new_col)):
                    continue
                self.avail_captures.add((new_row, new_col))  # ..add coord to their .avail_captures
            # If it's an allied piece..
            else:
                self.supporting.add((new_row, new_col))  # ..add coord to .supporting

        # CASTLING MOVEMENT
        if not self.has_moved:  # if not yet moved..
            checks, _ = board.get_checks()
            if self.colour not in checks:  # ..and not in check..
                row = self.location[0]
                for _, j in self.castle_pattern:  # look in both directions along the rank
                    new_col = self.location[1] + j
                    for _ in range(4):
                        if legal(row, new_col):  # if the next square is on the board..
                            square = board.squares[row][new_col]  # check it
                            if isinstance(square, Empty):  # if it's empty and not visible to opponent..
                                if board.get_pieces(self.opp_colour, in_check_vision=square.location) is not None:
                                    new_col += j  # keep going
                                    continue
                            elif isinstance(square, Rook):  # if it's a rook and it's not moved..
                                if not square.has_moved:
                                    castle_location = (row, self.location[1] + j*2)
                                    self.avail_moves.add(castle_location)  # ..then castling is legal
                            else:  # otherwise: no castling on this side
                                break
                        else:  # then we are off the board
                            break


class Queen(Piece):
    """ Queens inherit from Piece()
        They are very regular in their behaviour and so do not have much additional function over their parent
    """

    def __init__(self, colour, board, location, has_moved=False):
        super().__init__(colour, board, location, has_moved)
        self.pattern = [(0, 1), (1, 0), (1, 1), (-1, 0), (0, -1), (-1, 1), (1, -1), (-1, -1)]
        self.steps = 7


""" AGENT CLASSES ---------------------------------------------------------------------------------------- AGENT CLASSES
"""


class Agent:
    """ The Base class for all game-playing-agents: human, random, script, engine, etc. """
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'Name:        {self.name}\n' \
               f'Colour:      {self.colour}\n' \
               f'Agent_type:  {self.__class__.__name__}\n\n'


class Human(Agent):
    """ The human-player class.. inherits from Agent()
        Manages player actions in relationship to the Board object and game logic more generally
    """

    def __init__(self, name, colour):
        super().__init__(name, colour)

    def get_input(self, board):
        """ Prompts user for their command.
            If the command is a move it decomposes it into its relevant components and Returns them:
                active_piece, active_piece_type, target_location, is_capture, promotion_type, castle_direction
        """
        while True:
            print('<cmd> for a list of commands.')
            user_input = input('                   Your move:  ')
            print('\n')

            # MOVE PARSING AND PACKAGING
            if validate_san(user_input):
                try:
                    active_piece, active_piece_type, target_location, is_capture, \
                        promotion_type, castle_direction = decompose_and_assess(board, user_input)
                except InvalidInput as II:  # if it flags inform the agent and re-ask for a move
                    print(f"Apologies, '{user_input}' failed to identify a unique, legal move.")
                    print(f'     :  {II}')
                    continue
                return active_piece, active_piece_type, target_location, is_capture, promotion_type, castle_direction

            # COMMAND PARSING AND ACTION
            elif user_input.isalpha():
                user_input = user_input.lower()
                if user_input == 'cmd':
                    in_game_commands()
                elif user_input == 'resign':
                    not_implemented('resign')
                elif user_input == 'save':
                    print(f'FEN: {convert_board2fen(board)}')
                    not_implemented('save')
                elif user_input == 'tmp':
                    with open('tmp.txt', 'r') as tmp:
                        lines = tmp.readlines()
                        print(''.join(lines))
                elif user_input in ('close', 'quit', 'exit', 'no'):
                    exit_program()
            else:
                print(f"Apologies, '{user_input}' failed to identify recognisable move or command.")


class Random(Agent):
    """ The random move playing class.. inherits from Agent()
        Manages the selection of random moves on the board as follows:
            - Select a piece at random
            - From that piece's legal moves and captures one is selected
                If the move would take a Pawn to a final rank then a promotion is selected at random
            - The details are returned for execution:
                active_piece, active_piece_type, target_location, is_capture, promotion_type, castle_direction
    """

    def __init__(self, name, colour):
        super().__init__(name, colour)

    def get_input(self, board):
        """ Selects a random piece
            From that piece selects a random move or capture
            And derives the remaining, relevant information necessary to execute the move:
                active_piece, active_piece_type, target_location, is_capture, promotion_type, castle_direction
        """
        pieces = board.get_pieces(self.colour)  # select all pieces of the correct colour on the board
        pieces_with_moves = []
        for piece in pieces:
            if piece.avail_moves or piece.avail_captures:  # prune pieces with no legal moves
                pieces_with_moves.append(piece)

        active_piece = random.choice(pieces_with_moves)  # select a piece at random

        possible_moves = list(active_piece.avail_moves) + list(active_piece.avail_captures)  # from all possible moves
        target_location = random.choice(possible_moves)  # select one at random
        is_capture = bool(target_location in active_piece.avail_captures)

        castle_direction, promotion_type = '', ''
        # If we chose a King..
        if isinstance(active_piece, King):
            if abs(active_piece.location[1] - target_location[1]) == 2:  # and he's moving two squares..
                if active_piece.location < target_location:  # we're castling
                    castle_direction = 'King'  # ..note in which direction
                else:
                    castle_direction = 'Queen'  # ..note in which direction
        # If we chose a Pawn who is arriving at a final rank..
        if isinstance(active_piece, Pawn) and (target_location[0] == 0 or target_location[0] == 7):
            promotions = ['Rook', 'Knight', 'Bishop', 'Queen']  # ..pick a random promotion piece
            promotion_type = random.choice(promotions)

        return active_piece, active_piece.__class__.__name__, target_location,\
            is_capture, promotion_type, castle_direction


class Scripted(Agent):
    """ The scripted game playing class.. inherits from Agent()
        Manages the presentation of moves from an imported game to a Board object for execution.
        Only really used in testing as present.
        Could be implemented into user accessible functionality theoretically for game review and study etc.
    """

    def __init__(self, name, colour, script):
        super().__init__(name, colour)
        self.script = script

    def get_input(self, board):
        """ Reads the moves off the script in order.
            Completely capable of crashing the game if the script has been incorrectly formatted or contains errors.
        """
        try:
            scripted_move = self.script.pop(0)
        except IndexError as IE:
            print(f"Script has run out of moves!")
            print(f'     :  {IE}')
            raise
        if validate_san(scripted_move):
            try:
                active_piece, active_piece_type, target_location, is_capture, \
                    promotion_type, castle_direction = decompose_and_assess(board, scripted_move)
            except InvalidInput as II:  # if it flags there is some issue in the script
                print(f"Move '{scripted_move}' loaded from script is not legal!")
                print(f'     :  {II}')
                raise
        else:
            raise InvalidInput(f"Move '{scripted_move}' loaded from script is not legal!")

        return active_piece, active_piece_type, target_location, is_capture, promotion_type, castle_direction


class Engine(Agent):
    """ Not implemented """

    def __init__(self, name, colour):
        super().__init__(name, colour)

    pass


""" TEST FUNCTIONS & VARIABLE DEFINITIONS ---------------------------------------- TEST FUNCTIONS & VARIABLE DEFINITIONS
    Switched testing here - test.py became too cumbersome
        with imports and function & variable definitions..
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


""" UTILS -------------------------------------------------------------------------------------------------------- UTILS
"""


def white_black():
    """ Infinitely yields:
                'White'
                'Black'
                'White'
                'Black'
                ..etc..
    """
    while True:
        yield 'White'
        yield 'Black'


def flatten(l, ltypes=(list, tuple)):
    """ Flattens an arbitrarily large list or tuple
        Apparently very fast
        Pulled from online >> https://rightfootin.blogspot.com/2006/09/more-on-python-flatten.html
        Author: Mike C. Fletcher, Distribution: BasicTypes library.
    """
    ltype = type(l)
    l = list(l)
    i = 0
    while i < len(l):
        while isinstance(l[i], ltypes):
            if not l[i]:
                l.pop(i)
                i -= 1
                break
            else:
                l[i:i + 1] = l[i]
        i += 1
    return ltype(l)


def sign(a):
    """ Returns one of (-1, 0, 1) for a given integer or float as a representation of its sign
    """
    return bool(a > 0) - bool(a < 0)


""" CONVERSIONS -------------------------------------------------------------------------------------------- CONVERSIONS
"""


def legal(a, b):
    """ Returns True if the given index is on the board
            - that is, both indices in the range 0 -> 7
    """
    return a in range(8) and b in range(8)


def convert_san2board(san):
    """ Takes a PRE-VALIDATED coordinate in SAN (Standard Algebraic Notation)
        Returns a board coordinate of the form:     tuple(row, col)
        Completely capable of crashing the program if input is not valid
    """
    coord = []
    if san:
        letter, number = list(san)
        coord = (8 - int(number), FILES[letter])
    return coord


def convert_board2san(coord):
    """ Takes a PRE-VALIDATED coordinate of the form:   tuple(row, col)
        Returns a coordinate in SAN (Standard Algebraic Notation) : "a4" or "h6" for example
        Completely capable of crashing the program if input is not valid
    """
    result = []
    if coord:
        rank = 8 - coord[0]
        files = list(FILES.keys())
        file = files[coord[1]]
        result = ''.join([file, str(rank)])
    return result


def validate_san(san):
    """ validates that a string is compliant to the notation conventions of SAN >>
        https://en.wikipedia.org/wiki/Algebraic_notation_(chess)
        returns: MatchObject OR None

        pieces: R - rook, N - knight, B - bishop, K - king, Q - queen, pawns are not denoted by a character
        captures: x placed immediately before the target's square - eg: Nxf5
            pawns making captures are designated by their file prior to capturing: a, b, c, d, e, f, g, h - eg: exd4
        when disambiguating the active piece one may (in descending order of preference):
            indicate the file of departure
            indicate the rank of departure
            indicate both (very rare)
            eg: Rdf8, R1a3, Qh4e1
        promotion: trailing notation of piece being promoted to - eg: e8Q, f8N
        none-san valid strings: 'draw', 'resign', 'save', 'quit'
        castling: 0-0, 0-0-0 for king and queen side respectively, note those are ZEROs
        check: trailing '+'
        checkmate: trailing '#'
        end of game: 1-0, 0-1, ½-½ for white victory, black victory and draw respectively
    """
    result = re.search('[RNBQK]?[a-h]?[1-8]?[x]?[a-h][1-8][RNBQ]?[+#]?|0-0-?0?|O-O-?O?', san)
    return result


def decompose_san(san):
    """ For details of SAN see docstring for validate_san above
        Takes a pre-validated san string and returns:
            (0 - active piece type - STR,
             1 - active piece disambiguation - STR,
             2 - capture - BOOL,
             3 - target square - STR,
             4 - post-promotion piece type - STR,
             5 - check/check-mate claim - STR
             6 - castles - STR)
        Will absolutely not return correct results for an improperly formatted SAN
    """
    result = ['', '', False, '', '', '', '']

    if san.endswith('#'):
        result[5] = '#'
        san = san[:-1]
    if san.endswith('+'):
        result[5] = '+'
        san = san[:-1]
    if san == '0-0' or san == 'O-O':
        result[0], result[3], result[6] = 'King', 'g1 g8', 'King'
        return tuple(result)
    if san == '0-0-0' or san == 'O-O-O':
        result[0], result[3], result[6] = 'King', 'c1 c8', 'Queen'
        return tuple(result)
    if san.endswith(('R', 'N', 'B', 'Q')):
        result[4] = san[-1]
        san = san[:-1]
    result[3] = san[-2:]
    san = san[:-2]
    if san.startswith(('R', 'N', 'B', 'Q', 'K')):
        result[0] = san[0]
        san = san[1:]
    elif not san.startswith(('0', 'O')):
        result[0] = 'Pawn'
    if 'x' in san:
        result[2] = True
        san = san[:-1]
    result[1] = san

    for i, elem in enumerate(result):  # converts letter IDs into full words indicating Piece Type
        if elem in LETTERS:
            result[i] = LETTERS[elem]

    return tuple(result)


""" MENU CONTROL FLOW -------------------------------------------------------------------------------- MAIN CONTROL FLOW 
"""


def not_implemented(cmd):
    """ Basic function. Simply prints a given text is not implemented at this time and EXITS THE PROGRAM"""
    print(f'<{cmd}> not implemented at this time.')


def player_wants_game():
    """ Determines if player wants to play a game, see more advanced game options or quit the program """
    while True:
        print('Do you want to play a game?  <yes/no>                                every menu..  <close/quit/exit/no>')
        print('Advanced options             <adv>')
        try:
            result = input('    :  ').lower()
        except:
            continue

        if result == 'yes':
            return 1
        elif result == 'adv':
            return advanced_game_options()
        elif result in ('close', 'quit', 'exit', 'no'):
            exit_program()


def player_wants_to_load():
    """ Determines if player wants to load a saved game, load a saved FEN or manually enter a FEN """
    while True:
        print('Load what from where?')
        print('    5 - Saved game from local storage')
        print('    6 - FEN from local storage')
        print('    7 - FEN by manually entering')
        print('    <back>')
        print('    <help>')
        print('    <close/quit/exit/no>')
        result = input('    :  ')
        print('\n')

        if result.isnumeric():
            if result == '5':
                # if not save_games:
                #     print('Save-game functionality not possible. There was an error generating the local directory')
                #     continue
                not_implemented('LOAD FROM LOCAL SAVE')
            if result == '6':
                not_implemented('LOAD FROM LOCAL FEN')
            if result == '7':
                return int(result)
        elif result.isalpha():
            if result.lower() == 'back':
                return
            elif result.lower() == 'help':
                print('    FEN - https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation')
                print('    Saved games to be found locally in dir "SavedGames" ')
                print('    FENs stored locally can be found locally in dir "FENs"')
                input('\n')
            elif result.lower() in ('close', 'quit', 'exit', 'no'):
                exit_program()


def advanced_game_options():
    """ Gives player options about the kind of game to set up """
    while True:
        print('Play which game?')
        print('    1 - Standard game')
        print('    2 - King and Pawn game')
        print('    3 - Minor piece game')
        print('    4 - Major piece game')
        print('    <load>')
        print('    <help>')
        print('    <close/quit/exit/no>')
        result = input('    :  ')
        print('\n')

        if result.isnumeric():
            if result in ('1', '2', '3', '4'):
                return int(result)
        elif result.lower() == 'help':
            print('    Standard game      - Normal pieces on board')
            print('    King and Pawn game - Both sides have only King and Pawns')
            print('    Minor piece game   - Both side have only King, Pawns and Bishops and Knights')
            print('    Major piece game   - Both side have only King, Pawns and Queen and Rooks')
            input('\n')
        elif result.lower() == 'load':
            result = player_wants_to_load()
            if result in range(5, 8):
                return result
        elif result.lower() in ('close', 'quit', 'exit', 'no'):
            exit_program()


def set_board(result):
    """ Returns a Board, initialised and ready for play corresponding to the integer input.
        1 - STANDARD_GAME
        2 - KING_AND_PAWN_GAME
        3 - MINOR_GAME
        4 - MAJOR_GAME
    """
    games = (STANDARD_GAME, KING_AND_PAWN_GAME, MINOR_GAME, MAJOR_GAME)

    board = Board(games[result - 1])
    return board


def convert_fen2board(fen):
    """ Validates a string compliant to the notation conventions of FEN >>
                https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation

        Returns: MatchObject OR None

        There are six fields:
            1 - placement of pieces..
                pieces: Pp - pawn, Rr - rook, Nn - knight, Bb - bishop, Kk - king, Qq - queen
                colour: White - uppercase, Black - lowercase
                position: rank8/rank7/rank6/..
                empty squares: indicated by numbers 1-8
            2 - Colour of active_player..
                White - 'w', Black - 'b'
            3 - Castling availability..
                k, K, q, Q - black_king_side, white_king_side, black_queen_side, white_queen_side
            4 - En passant target square in SAN.. 'e3', 'f5, etc.
            5 - Half-move clock.. number of 'halfmoves' since last pawn move or piece capture for 50-move-rule
            6 - Full-move clock.. number of turns executed thus far, starting at 1 and +1 at end of black's turn
        """
    print(fen)
    sections = fen.split()  # split FEn into sections..
    if len(sections) != 6:
        raise InvalidInput('Not six elements in FEN')  # confirm there are 6 sections..
    positions, active_player_colour, castling_avail, en_passant_target, half_move_count, full_move_count = sections

    # BUILD BOARD AND PIECES - first elem
    rows = positions.split('/')  # split board-state-string into rows
    if len(rows) != 8:
        raise InvalidInput('Elem1 of FEN incorrect syntax; not 8 rows delineated')
    board, new_board = Board([], []), []  # Generate an Empty board.

    # Check each FEN row for syntax..
    for row in rows:
        if not re.match(r'[1-8pPrRnNbBkKqQ-]{1,8}$', row):  # Confirm syntax
            raise InvalidInput('Elem1 of FEN incorrect syntax; format of a row is incorrect')
        # Convert numbers into strings of "e"s relating to their magnitude
        row = [x if x not in '12345678' else list('e'*int(x)) for x in list(row)]
        row = flatten(row)  # individuate each element into a string of length 1 per item in the row
        new_board.append(row)  # load the row into an array, analogous to that of the board.squares array

    # Load FEN onto the board..
    for row in range(8):
        for col in range(8):
            count = row * 8 + col  # Keep track of how many squares "onto" the board we are.
            letter = new_board[row][col]
            if letter == 'e':  # If an element is an Empty square..
                if count % 2 == 0:  # ..and it would be a White square..
                    letter = letter.upper()  # ..make it uppercase
            if letter.isupper():  # All Uppercase letters..
                colour = 'White'  # ..are White
            else:  # all Lowercase
                colour = 'Black'  # ..are Black
                letter = letter.upper()  # and normalise all letters to upper case for next step
            type_, has_moved = LETTERS[letter], True  # prep piece details
            if letter == 'P' and (row == 1 or row == 6):
                has_moved = False  # identify unmoved Pawns (colour irrelevant due to proximity to edge of board)
            board.squares[row][col] = eval(type_)(colour, board, (row, col), has_moved)  # ..and fill the board

    # ACTIVE PLAYER COLOUR - second elem
    if active_player_colour == 'w':
        colour = 'White'
    elif active_player_colour == 'b':
        colour = 'Black'
    else:
        raise InvalidInput('Elem2 of FEN incorrect; must be "w" or "b"')
    board.player_turn = colour

    # CASTLING AVAILABILITY - third elem
    if 'q' in castling_avail:  # Black's queen-side castling still legal
        board.squares[0][0].has_moved, board.squares[0][4].has_moved = False, False
        print("Black's queen-side castling still legal")
    if 'k' in castling_avail:  # Black's king-side castling still legal
        board.squares[0][7].has_moved, board.squares[0][4].has_moved = False, False
        print("Black's king-side castling still legal")
    if 'Q' in castling_avail:  # White's queen-side castling still legal
        board.squares[7][0].has_moved, board.squares[7][4].has_moved = False, False
        print("White's queen-side castling still legal")
    if 'K' in castling_avail:  # White's king-side castling still legal
        board.squares[7][7].has_moved, board.squares[7][4].has_moved = False, False
        print("White's king-side castling still legal")

    # EN PASSANT INDICATION - fourth elem
    #   if en passant indication present and of correct form..
    if en_passant_target != '-' and re.match('[a-h][1-8]$', en_passant_target):
        coord = convert_san2board(en_passant_target)
        if coord[0] == 4 or coord[0] == 2:  # if coordinate is on the correct ranks
            board.passant_loc = coord  # ..run with it
    elif en_passant_target == '-':  # in case of no indication of legal en passant
        pass
    else:  # ..otherwise: raise exception
        raise InvalidInput('Elem4 of FEN incorrect; must be legal coord of 3rd or 5th rank')

    # HALF-MOVE COUNTER - fifth elem
    if int(half_move_count) < 0:
        raise InvalidInput('Elem5 of FEN incorrect; must be int of 0 or greater')
    else:
        board.draw_count = int(half_move_count)/2  # Board increments 0.5 for half moves.. FEN increments 1.0

    # TURN NUMBER COUNTER - sixth elem
    if int(full_move_count) < 1:
        raise InvalidInput('Elem6 of FEN incorrect; must be int of 1 or greater')
    else:
        board.turn_count = int(full_move_count)
        if board.player_turn == 'Black':
            board.turn_count += 0.5  # Board increments turns by 0.5 per player move
        if board.passant_loc:  # if en passant is on the board then set the en passant timer
            board.passant_count = board.turn_count - 0.5

    # DEBUG PRINT CHAFF
    print(board)
    print(f'board.player_turn: {board.player_turn}')
    print(f'\nboard.draw_count    {board.draw_count}')
    print(f'board.passant_loc   {board.passant_loc}')
    print(f'board.passant_count   {board.passant_count}')
    print(f'board.turn_count  {board.turn_count}')

    return board


def get_agent_type(player):
    """ Prompts user for info as to the type of agent to be created """
    print('There are two kinds of Agents you can initialise.')
    print('    1 - <Human> - This would be a totally manually operated agent.')
    print('                You are playing the game yourself.')
    print('    2 - <Random> - This is an agent who simply makes totally random moves.')
    print('                 They select from the set of all legal moves.')
    # print('    3 - <Engine> - This is an agent which selects moves on the basis of some')
    # print('                 pre-programmed algorithm.')
    print(f'\nWhich type of agent should {player} be?')

    while True:
        result = input('        :  ')
        if result.isalpha():  # check response is all letters
            result = result.lower()  # make them all lowercase
            if result.lower() == 'human':
                agent_type = result.capitalize()
                break
            elif result.lower() == 'random':
                agent_type = result.capitalize()
                break
            # elif result.lower() == 'engine':
            #     not_implemented('Engine')
            #     continue
            elif result.lower() in ('close', 'quit', 'exit', 'no'):
                exit_program()
        elif result.isnumeric():
            if result == '1':
                agent_type = 'Human'
                break
            elif result == '2':
                agent_type = 'Random'
                break
            # elif result == '3':
            #     not_implemented('Engine')
            #     continue

    agent_name = player
    print(f'And their name? Typing nothing will use the default name: {player}')
    while True:
        result = input('        :  ')
        if result == '':
            break
        elif result.isalnum():
            if result.lower() in ('close', 'quit', 'exit', 'no'):
                exit_program()
            agent_name = result
            break
        else:
            print('\n        Can only include letters or numbers.\n')

    return agent_type, agent_name


def assign_players():
    """ Takes user through the process of initialising the two agents
        Returns two Agent() instances as player1 & player2:
            Player1 is always 'White',
            Player2 is always 'Black'
    """
    print('This is the Agent Creation Wizard.\n')
    print("We'll take you through the process of initialising the Agents who will be playing the game.")
    print('Player1 (White) and Player2 (Black).')
    print("Let's start!\n\n")

    player1, player2, gen_colour = 'Player1', 'Player2', white_black()

    # Agent 1 - white
    agent_type, agent_name = get_agent_type(player1)
    player1 = eval(agent_type)(agent_name, next(gen_colour))

    print("Let's start!\n\n")

    # Agent 2 - black
    agent_type, agent_name = get_agent_type(player2)
    player2 = eval(agent_type)(agent_name, next(gen_colour))

    return player1, player2


def in_game_commands():
    print('    <resign> the game')
    print('    <save> the game for later continuation from current position')
    print('    <tmp> displays the contents of the tmp.txt file associated with 3 fold repetition')
    print('    <close/quit/exit/no> the program\n')


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
            col = FILES[disambiguation]  # then it's a file
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
        r = range(start_row, end_row + sign(row_diff), sign(row_diff))
    else:
        r = [start_row for _ in range(abs(col_diff) + 1)]
    if col_diff != 0:  # if the locations are not in the same column
        c = range(start_col, end_col + sign(col_diff), sign(col_diff))
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
    board.squares[r][c] = eval(promotion_type)(board.player_turn, board, target_location, has_moved=True)
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
            if isinstance(square, Empty):  # ..if it's empty..
                empty_count += 1  # ..add it to a running total
            else:  # if it's a piece..
                if empty_count >= 1:  # ..with preceding empty squares..
                    txt.append(str(empty_count))  # ..append the number of those empty squares..
                    empty_count = 0  # ..and reset the running total
                letter = TYPES[square.colour][square.__class__.__name__]  # then note the type and colour of the piece
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
    for index, colour in enumerate(COLOURS):  # for each colour.. (white first)
        king_sq = board.squares[row[index]][4]  # check the king's home square
        if isinstance(king_sq, King) and not king_sq.has_moved:  # if it is a king, which has not moved..
            for col, side in sides.items():  # go on to check its rooks..
                rook_sq = board.squares[row[index]][col]  # for each side.. (king-side first)
                if isinstance(rook_sq, Rook) and not rook_sq.has_moved:  # if it is a rook, which has not moved..
                    letter = TYPES[colour][sides[col]]  # note that castling on that side is legal
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
    fmn = str(math.floor(board.turn_count))
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
    while True:  # This catches moving-into-check type illegal moves and checkmates/draws by process of elimination

        # Get agent move/input - contains a close program option
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
            if isinstance(active_piece, Pawn):  # if a Pawn was the active piece
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
        print(f'                                   Turn No.  : {math.floor(board.turn_count)}.')
        try:
            agent_turn(board, *players)  # Execute the active_player's turn
        except Checkmate as CM:
            txt, board, player_of_final_move = CM.args
            print(f'                CHECKMATE! {player_of_final_move} wins! After {math.floor(board.turn_count)} moves')
            print('\n                 GAME OVER!\n')
            game_on = False
            continue
        except Draw as D:
            txt, board, player_of_final_move = D.args
            print(f'                        {txt} After {math.floor(board.turn_count)} moves')
            print('\n                         GAME OVER!\n')
            game_on = False
            continue

        board.turn_count += 0.5  # half-step the turn counter
        players.reverse()  # Swap the active_player with the passive_player
        board.player_turn, = set(COLOURS) - {board.player_turn}  # Swap the colour of the player who is on-turn

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


def exit_program():
    """ Exits the program """
    print('Okay! See you soon :)')
    sys.exit()


def main():
    """ Main control logic of the program
            - chose board starting position from selection of variants, saved games or FENs
            - chose type of agents to play the game (human, random, etc)
            - play the game out
        Repeat until user closes program
    """
    # INITIALISE LOCAL DIRECTORY FOR VARIOUS SCRIPT FUNCTIONALITY (SavedGames, tmp.txt)
    # global save_games
    # SaveGames directory creation if not already in CWD
    # path = os.path.dirname(os.path.abspath(__file__))
    # try:
    #     Path(path + '\\SavedGames').mkdir(exist_ok=True)
    # except FileExistsError as FEE:
    #     print('Something went wrong, likely an operating system mismatch, this script is Windows only')
    #     print(f'{FEE}')
    #     print('Without this functionality Saving games will not be possible')
    #     save_games = False
    # else:
    #     save_games = True

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
        # Can happen due to loading game from FEN
        if board.player_turn == 'Black':
            players.reverse()

        # Play the game
        play_a_game(board, *players)

        # Loops until player terminates the program


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


""" MAIN LOGIC ---------------------------------------------------------------------------------------------- MAIN LOGIC
"""
if __name__ == '__main__':

    # test_variables()

    # for x in range(100):
    #     test()
    #     print(f'{x}, ' * 30)

    # for fen in fens:
    #     convert_fen2board(fen)

    # test_checkmates(legal_checkmates)

    main()


