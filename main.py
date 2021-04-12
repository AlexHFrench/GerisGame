# Gerry's Game
#   ...enjoy! :D


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
        'board indices'; the pair of indices (row, col) indexing a square (board.squares[row][col])

"""
""" --------------------------- IMPORTS
        """

import re
from Exceptions import *

""" BOARD & PIECES --------------------------------------------------------------------------------------------- CLASSES
"""


class Board:
    """ Board():
            ATR:
                squares
                log
            METH:
                __str__
                set_board (initial_position)
                move (piece, target_square)
                capture (piece, target_square)
                promote (pawn, new_type)
                is_check ()
                is_checkmate ()
    """

    def __init__(self, initial_positions=range(8)):
        self.sideboard, self.white_in_check, self.black_in_check, self.draw_counter = [], False, False, 0
        self.white_in_checkmate, self.black_in_checkmate, self.draw = False, False, False
        self.white_agent, self.black_agent, self.player_turn, self.turn_num = None, None, 'White', 1.0
        colour_generator = white_black()
        self.squares = [[Empty(next(colour_generator), (row, col)) for col in range(8)] for row in range(8)]
        for row in STARTING_ROWS:
            for col in range(8):
                if row == 0 and col in initial_positions:  # only instantiate pieces indicated by the type of game
                    type_ = BACK_LINE[col]
                    self.squares[row][col] = eval(type_)('Black', self, (row, col))
                if row == 1:
                    type_ = FRONT_LINE[col]
                    self.squares[row][col] = eval(type_)('Black', self, (row, col))
                if row == 6:
                    type_ = FRONT_LINE[col]
                    self.squares[row][col] = eval(type_)('White', self, (row, col))
                if row == 7 and col in initial_positions:
                    type_ = BACK_LINE[col]
                    self.squares[row][col] = eval(type_)('White', self, (row, col))
        print('just built and set the board, updating pieces..')
        self.update_pieces('Black')

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
            output += file + ' ' * 6
        output += '\n'
        return output

    def clear(self):
        """ remove all pieces from an already extant Board object
        """
        colour_generator = white_black()
        self.squares = [[Empty(next(colour_generator), (row, col)) for col in range(8)] for row in range(8)]

    def update_pieces(self, colour):
        """ This updates each piece s.r.t. their legal moves given current board state.
            Kings are updated last and the King whose move it is is updated last.
            colour is the colour of the King whose turn it is currently.
        """
        kings = list()
        for row, col in ((x, y) for x in range(8) for y in range(8)):  # give pieces vision of the board
            square = self.squares[row][col]
            if isinstance(square, Piece):  # For each piece
                square.location = (row, col)
                if isinstance(square, King):  # unless it's a king
                    kings.append(square)
                    continue
                square.look(self)  # have it look at the board
        # this handles niche case where two kings are "fighting over" a single pawn
        for king in kings:
            king.clear_vision()
        for index, king in enumerate(kings):
            if king.colour == colour:

                kings[abs(index - 1)].look(self)  # first update the non-playing-player's King
                king.look(self)  # then the King whose turn it is

    def get_pieces(self, colour=None, type_=None, move_vision=None, reach_of_check=None):
        """ Returns all pieces on the board which match the given criteria. """
        pieces = flatten(self.squares)
        pieces = filter(lambda x: isinstance(x, Piece), pieces)
        if colour:
            pieces = filter(lambda x: x.colour == colour, pieces)
        if type_:
            pieces = filter(lambda x: isinstance(x, eval(type_)), pieces)
        if move_vision:
            pieces = filter(lambda x: move_vision in x.avail_moves
                            or move_vision in x.avail_captures, pieces)
        elif reach_of_check:
            pieces = filter(lambda x: move_through_check(x, reach_of_check), pieces)
        pieces = list(pieces)
        return pieces

    def blind_move(self, start_location, target_location):
        """ BLIND move of the contents of a start-square to a target-square.
            No checks are made for legality of any kind!
        """
        start_row, start_col = start_location
        active_piece = self.squares[start_row][start_col]
        print(f'\nMoving piece: {repr(active_piece)}')
        end_row, end_col = target_location

        self.squares[start_row][start_col] = active_piece.temp  # replace Empty object in active_piece's location
        active_piece.temp = self.squares[end_row][end_col]  # store content of target_location in active_piece's .temp
        self.squares[end_row][end_col] = active_piece  # place active_piece in target_location

    def test_move(self, active_piece, target_location):
        """ Creates a copy of the board and moves the piece to the target square.
            A check is then made for relevant checks - Returns True if move is legal
        """
        import copy

        test_board = copy.deepcopy(self)  # copy the board
        test_board.blind_move(active_piece.location, target_location)  # move the piece
        test_board.update_pieces(active_piece.colour)  # check for checks

        checks, _ = test_board.get_checks()
        return active_piece.colour not in checks  # return True if move is legal

    def move(self, active_piece, active_piece_type, target_location, is_capture, promotion_type, castle_direction):
        """ Move active_piece from present location to target_location
            Empty [square] objects are stored in active_piece.temp while checks are made for legality of move
            In case of capture: active_piece.temp = target_piece s.t. target_piece.temp = Empty object
        """
        if self.test_move(active_piece, target_location):  # if the move would not leave King in check..
            self.blind_move(active_piece.location, target_location)  # execute the move

            if is_capture:  # if it's a capture
                self.sideboard.append(active_piece.temp)  # move target_piece to self.sideboard
                active_piece.temp = active_piece.temp.temp  # replace taken piece's .temp onto the board
            if promotion_type:  # if it's a promotion
                promote_pawn(self, active_piece, target_location, promotion_type)
            elif castle_direction:  # if we're castling, we now need to move the Rook
                if castle_direction == 'Queen':  # check which direction
                    start_col, end_col = 0, 3
                else:
                    start_col, end_col = 7, 5
                start_row, _ = active_piece.location
                self.blind_move((start_row, start_col), (start_row, end_col))  # ..and move the Rook
                print(repr(self.squares[start_row][end_col]))
                self.squares[start_row][end_col].has_moved = True  # don't forget to mark it as having moved
        else:  # if the original move would not be legal..
            print(f'checking if : {target_location} was in avail_m or avail_cap')
            if target_location in active_piece.avail_moves:  # remove it from the set of possible moves
                print(f'found it in : avail_moves.. removing it from the list')
                active_piece.avail_moves.remove(target_location)
            elif target_location in active_piece.avail_captures:  # remove it from the set of possible moves
                print(f'found it in : avail_captures.. removing it from the list')
                active_piece.avail_captures.remove(target_location)
            print(f'raising IllegalMove exception due to board.test_move returning false!')
            raise IllegalMove(f"{active_piece.colour}'s King would be in check!")  # raise an exception


    def get_checks(self):
        """ Returns: a list of colours currently in check, i.e. ['White', 'White'] for double check
                     a list of pieces currently giving check
            The returned elements are ordered such that zip(elem1, elem2) would form matching pairs.
        """
        # print('\nlooking for checks...')
        checks, checking_pieces = [], []
        for colour in COLOURS:  # For each colour
            # print(f'colour : {colour}')
            king, = self.get_pieces(colour, 'King')  # Find their King
            # print(f'king being checked : {king}')
            target_location = king.location
            # print(f"king's location : {king.location}")
            # List opposition pieces with vision of the King
            any_checking_pieces = self.get_pieces(king.opp_colour, move_vision=target_location)
            # print(f'pieces giving check to the king : {any_checking_pieces}')
            for piece in any_checking_pieces:  # For each of those pieces (if any)
                checks.append(colour)  # indicate the colour in check
            checking_pieces.extend(any_checking_pieces)  # and add those pieces to a list
        # print(f'checks found : {checks}, {checking_pieces}')
        return checks, checking_pieces

    def is_checkmate(self, colour):
        """ Returns True if player of <colour> in checkmate """
        checkmate = True
        checks, checking_pieces = self.get_checks()
        if colour in checks:  # if King is in check..
            print(f'King of colour: {colour} is in CHECK')
            king, = self.get_pieces(colour, 'King')
            legal_king_moves = list(king.avail_moves) + list(king.avail_captures)
            if len(legal_king_moves) == 0:  # and King has no moves..
                print(f'King has no moves available')
                for piece in checking_pieces:  # for each piece checking the king..
                    locations = squares_in_direction(piece.location, king.location)
                    for loc in locations:  # can checking_piece be captured or check interposed?
                        for candidate in self.get_pieces(king.colour, move_vision=loc):  # move_vision also checks caps
                            if self.test_move(candidate, loc):  # legally?
                                checkmate = False  # if so, capture/interposition is legal - no checkmate
                                print(f'it has been noticed that : {candidate} can save the King')
                                break
                            else:
                                pass  # otherwise capture/interposition is not legal - possible checkmate
            else:
                checkmate = False
        else:
            checkmate = False

        return checkmate

    def is_draw(self, colour):
        """ Returns True if any Draw condition has been reached.
            Currently implemented: 50-move-rule, stalemate.
            Not yet implemented: insufficient mating material, 3-fold-rep.
        """
        draw = False

        if self.draw_counter == 50.0:
            print('Draw by 50 move rule!')
            draw = True

        if not draw:  # if 50-move-rule not reached
            draw = True
            for piece in self.get_pieces(colour):  # check every piece on board of active player
                # print(f'Checking  : {piece}')
                # print(f'avail_moves : {piece.avail_moves}')
                # print(f'avail_captures : {piece.avail_captures}')
                if piece.avail_moves == set() and piece.avail_captures == set():
                    pass  # if none turn out to have a legal move then it is a draw
                else:
                    draw = False  # if any have a move, it is not a draw
            if draw:
                print('Draw by no legal moves!')
                print(f'{self.get_pieces(colour)}')

        return draw


class Empty:
    """ Empty square, place holder object. Has colour and location."""

    def __init__(self, colour, location):
        self.colour = colour
        self.location = location

    def __str__(self):
        return '―'

    def __repr__(self):
        san_loc = convert_board2san(self.location)
        return '― >> ' + san_loc


class Piece:
    """ Piece():
            ATR:
                colour
                position
                avail_moves
                avail_captures
                has_moved
            METH:
                __init__
                    colour
                    has_moved
                __str__

                clear_vision
                look_again
    """

    def __init__(self, colour, board, location, has_moved=False):
        self.avail_moves, self.avail_captures, self.supporting = set(), set(), set()  # piece vision
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

        return f'\n {self} \n'\
            f'colour: {self.colour}\n'\
            f'location: {self.location}\n'\
            f'.. in SAN: {convert_board2san(self.location)}\n' \
            f'.. in temp: {repr(self.temp)}\n' \
            f'available moves: {avail_moves}\n'\
            f'available captures: {avail_captures}\n' \
            f'supporting: {supporting}\n' \
            f'has moved: {self.has_moved}'

    def look(self, board):
        """Piece populates self.avail_moves and self.avail_captures with legal board indices."""
        self.avail_moves, self.avail_captures, self.supporting = set(), set(), set()
        for i, j in self.pattern:
            new_row = self.location[0] + i
            new_col = self.location[1] + j

            for _ in range(self.steps):
                if not legal(new_row, new_col):
                    break
                square = board.squares[new_row][new_col]
                if isinstance(square, Empty):
                    if isinstance(self, King):  # Kings cannot move into check >>
                        if board.get_pieces(self.opp_colour, reach_of_check=(new_row, new_col)):
                            break
                    self.avail_moves.add((new_row, new_col))
                    new_row += i
                    new_col += j
                elif square.colour != self.colour:
                    if isinstance(self, King):  # Kings cannot move into check >>
                        if board.get_pieces(self.opp_colour, reach_of_check=(new_row, new_col)):
                            break
                    self.avail_captures.add((new_row, new_col))
                    break
                else:
                    self.supporting.add((new_row, new_col))
                    break

    def clear_vision(self):
        """ Removes a piece's vision of the board completely """
        self.avail_moves, self.avail_captures, self.supporting = set(), set(), set()

    def update_location(self, coord):
        """ Changes the piece's instance variable pertaining to which square it's on """
        self.location = coord


class Pawn(Piece):
    """ Pawn()
            inherits from Piece
            ATR:
                move_rules
                en_passant_rules
                promotion_rules
            METH:
    """

    def __init__(self, colour, board, location, has_moved=False):
        super().__init__(colour, board, location, has_moved)
        self.pattern, self.steps, self.capture_vision = [(1, 1), (1, -1)], 1, None
        if colour == 'White':
            self.direction = -1  # used to orient the piece on the board; pawns are not omni-directional
        else:
            self.direction = 1

    def __repr__(self):
        capture_vision = [convert_board2san(x) for x in self.capture_vision]
        first = super().__repr__()
        return f'{first}\naggro vision: {str(capture_vision)}'

    def look(self, board):
        """Piece populates self.avail_moves and self.avail_captures with legal board indices."""
        self.avail_moves, self.avail_captures, self.supporting, self.capture_vision = set(), set(), set(), set()
        new_row, _ = row, col = self.location
        if not self.has_moved:
            self.steps = 2
        # Examine squares the Pawn can non-aggressively move to
        for _ in range(self.steps):
            new_row += self.direction
            if not legal(new_row, col):  # this means this pawn is promoting
                continue
            square = board.squares[new_row][col]
            if isinstance(square, Empty):
                self.avail_moves.add((new_row, col))
            else:
                break
        self.steps = 1
        # Examine squares the Pawn can aggressively move to
        for i, j in self.pattern:
            new_row = self.location[0] + i * self.direction
            new_col = self.location[1] + j * self.direction
            if not legal(new_row, new_col):  # if off the board ignore them
                continue
            square = board.squares[new_row][new_col]
            if isinstance(square, Piece):  # if there is a piece there
                if square.colour != self.colour:  # and it an opposition piece ..
                    self.avail_captures.add((new_row, new_col))  # note it down
                else:  # if it's ours
                    self.supporting.add((new_row, new_col))  # note it down
            else:  # if it is an empty square, note it down
                self.capture_vision.add((new_row, new_col))  # this is for move-through-check calculations

    def clear_vision(self):
        """ Totally removes a pieces vision of the board """
        super().clear_vision()
        self.capture_vision = set()


class Rook(Piece):
    """ Rook()
            inherits from Piece
            ATR:
                move_rules
            METH:
    """

    def __init__(self, colour, board, location, has_moved=False):
        super().__init__(colour, board, location, has_moved)
        self.pattern = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.steps = 7


class Knight(Piece):
    """ Knight()
            inherits from Piece
            ATR:
                move_rules
            METH:
    """

    def __init__(self, colour, board, location, has_moved=False):
        super().__init__(colour, board, location, has_moved)
        self.pattern = [(1, 2), (2, 1), (-1, 2), (2, -1), (-2, 1), (1, -2), (-1, -2), (-2, -1)]
        self.steps = 1


class Bishop(Piece):
    """ Bishop()
            inherits from Piece
            ATR:
                move_rules
            METH:
    """

    def __init__(self, colour, board, location, has_moved=False):
        super().__init__(colour, board, location, has_moved)
        self.pattern = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        self.steps = 7


class King(Piece):
    """ King()
            inherits from Piece
            ATR:
                move_rules
                castle_rules
                in_check
                in_check_mate
            METH:
    """

    def __init__(self, colour, board, location, has_moved=False):
        super().__init__(colour, board, location, has_moved)
        self.pattern = [(0, 1), (1, 0), (1, 1), (-1, 0), (0, -1), (-1, 1), (1, -1), (-1, -1)]
        self.castle_pattern = [(0, 1), (0, -1)]
        self.steps, self.avail_castles = 1, set()
        self.opp_colour, = set(COLOURS) - {self.colour}

    def look(self, board):
        super().look(board)
        # print(f'{self.colour} King is now looking.')
        checks, _ = board.get_checks()
        if not self.has_moved and self.colour not in checks:  # if not moved and not in check
            row = self.location[0]
            for _, j in self.castle_pattern:  # in both directions along the rank
                new_col = self.location[1] + j
                for _ in range(4):
                    if legal(row, new_col):  # if the next square is on the board
                        square = board.squares[row][new_col]  # check it
                        if isinstance(square, Empty):  # if it's empty and not visible to opponent..
                            if board.get_pieces(self.opp_colour, reach_of_check=square.location) is not None:
                                new_col += j  # keep going
                                continue
                        elif isinstance(square, Rook):  # if it's a rook and it's not moved..
                            if not square.has_moved:
                                castle_location = (row, self.location[1] + j*2)
                                self.avail_moves.add(castle_location)  # castling is legal
                        else:
                            break
                    else:
                        break


class Queen(Piece):
    """ Queen()
            inherits from Piece
            ATR:
                move_rules
            METH:

    """

    def __init__(self, colour, board, location, has_moved=False):
        super().__init__(colour, board, location, has_moved)
        self.pattern = [(0, 1), (1, 0), (1, 1), (-1, 0), (0, -1), (-1, 1), (1, -1), (-1, -1)]
        self.steps = 7


""" AGENTS ----------------------------------------------------------------------------------------------------- CLASSES
"""


class Agent:
    """ The Base class for all game-playing-agents: human, random, engine, etc. """
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
    """ The human-player class - Manages player actions. """

    def __init__(self, name, colour):
        super().__init__(name, colour)

    def get_input(self, board):
        """ Prompts user for their command - Returns the string.
            Ensures it is a viable command or of correct SAN syntax before returning.
        """
        while True:
            print('<cmd> for a list of commands.')
            result = input('                   Your move:  ')
            print('\n')
            if validate_san(result):
                try:
                    active_piece, active_piece_type, target_location, is_capture, \
                        promotion_type, castle_direction = determine_active_piece(board, self.colour, result)
                except InvalidInput as II:  # if it flags inform the agent and re-ask for a move
                    print(f'Apologies, {result} failed to identify a unique, legal move.')
                    print(f'{II}')
                    continue
                return active_piece, target_location, castle_direction
            elif result.isalpha():
                result = result.lower()
                if result == 'cmd':
                    in_game_commands()
                if result == 'resign':
                    not_implemented('resign')
                if result == 'save':
                    not_implemented('save')
                if result == 'close':
                    exit_program()


class Random(Agent):
    """ The random-action-player class - Manages random-action-player decisions and actions. """

    def __init__(self, name, colour):
        super().__init__(name, colour)

    def get_input(self, board):
        """ selects a random piece, from that piece selects a random move or capture and returns the values """
        pieces = board.get_pieces(self.colour)
        pieces_with_moves = []
        for piece in pieces:
            if piece.avail_moves == set() and piece.avail_captures == set():
                pass
            else:
                pieces_with_moves.append(piece)

        # if pieces_with_moves:
        active_piece = random.choice(pieces_with_moves)
        # else:

        print(repr(active_piece) + '\n')
        possible_moves = list(active_piece.avail_moves) + list(active_piece.avail_captures)
        target_location = random.choice(possible_moves)
        is_capture = bool(target_location in active_piece.avail_captures)
        print(f'Target square : {target_location}\n')

        castle_direction, promotion_type = '', ''
        if isinstance(active_piece, King):
            print(active_piece.location)
            print(target_location)
            if abs(active_piece.location[1] - target_location[1]) == 2:
                if active_piece.location < target_location:
                    castle_direction = 'King'
                else:
                    castle_direction = 'Queen'
        if isinstance(active_piece, Pawn) and (target_location[1] == 0 or target_location[1] == 7):
            promotions = ['R', 'N', 'B', 'Q']
            promotion_type = random.choice(promotions)

        return active_piece, active_piece.__class__.__name__, target_location, is_capture, promotion_type, castle_direction


class Engine(Agent):
    """ The engine class - Manages engine decisions and actions. """

    def __init__(self, name, colour):
        super().__init__(name, colour)

    pass


""" UTILS --------------------------------------------------------------------------------------------------------------
"""


def white_black():
    """ Infinitely yields 'White', 'Black', 'White', 'Black', etc."""
    while True:
        yield 'White'
        yield 'Black'


def flatten(l, ltypes=(list, tuple)):
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
    return bool(a > 0) - bool(a < 0)


""" CONVERSIONS --------------------------------------------------------------------------------------------------------
"""


def legal(a, b):
    """Returns True if the given index is on the board (both indices in 0-7)"""
    return a in range(8) and b in range(8)


def convert_san2board(san):
    """ accepts a board location in SAN (Standard Algebraic Notation) - must be pre-validated
        returns a board location as tuple of form (row, col)
    """
    letter, number = list(san)
    coord = (8 - int(number), FILES[letter])
    return coord


def convert_board2san(coord):
    """ accepts a board location as tuple of integers of form (row, col)
        returns a board location in SAN (Standard Algebraic Notation)
    """
    file = None
    for letter, number in FILES.items():
        if coord[1] == number:
            file = letter
    rank = 8 - coord[0]
    return ''.join([file, str(rank)])


def validate_san(san):
    """ validates a string, is compliant to the notation conventions of SAN >>
        (https://en.wikipedia.org/wiki/Algebraic_notation_(chess))
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
    """ for details of SAN see docstring for validate_san above
        take a pre-validated san string and returns:
            (0 - active piece type - STR,
             1 - active piece disambiguation - STR,
             2 - capture - BOOL,
             3 - target square - STR,
             4 - post-promotion piece type - STR,
             5 - check/check-mate claim - STR
             6 - castles - STR)
    """
    result = ['', '', False, '', '', '', '']

    if san == '0-0' or san == 'O-O':
        result = ['King', '', False, 'g1 g8', '', '', 'King']
        return tuple(result)
    if san == '0-0-0' or san == 'O-O-O':
        result = ['King', '', False, 'c1 c8', '', '', 'Queen']
        return tuple(result)
    if san.endswith('#'):
        result[5] = '#'
        san = san[:-1]
    if san.endswith('+'):
        result[5] = '+'
        san = san[:-1]
    if san.endswith(('R', 'N', 'B', 'Q')):
        result[4] = san[-1]
        san = san[:-1]
    result[3] = san[-2:]
    san = san[:-2]
    if san.startswith(('R', 'N', 'B', 'Q', 'K')):
        result[0] = san[0]
        san = san[1:]
    else:
        result[0] = 'Pawn'
    if 'x' in san:
        result[2] = True
        san = san[:-1]
    result[1] = san

    for i, j in enumerate(result):
        if j == 'R':
            result[i] = 'Rook'
        elif j == 'N':
            result[i] = 'Knight'
        elif j == 'B':
            result[i] = 'Bishop'
        elif j == 'K':
            result[i] = 'King'
        elif j == 'Q':
            result[i] = 'Queen'

    return tuple(result)


""" GLOBAL IMPORT & VARIABLE DEFINITIONS -------------------------------------------------------------------------------
"""


def MAIN_VARIABLES():
    """ All variables and imports for the main logic of the program
        I separated this into a function to make tests.py function more cleanly
    """

    """ --------------------------- MAIN VARIABLES
    """
    global COLOURS, VALUES, LETTERS, PATTERNS, STEPS, UNICODES, STARTING_ROWS, STANDARD_GAME
    global KING_AND_PAWN_GAME, MINOR_GAME, MAJOR_GAME, FRONT_LINE, BACK_LINE, ROWS, FILES
    global IN_GAME_COMMANDS

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

    # rows on which pieces start the game (the first and last two)
    STARTING_ROWS = (7, 6, 1, 0)

    # Columns on which pieces start the game
    STANDARD_GAME = (0, 1, 2, 3, 4, 5, 6, 7)  # all pieces
    KING_AND_PAWN_GAME = 4,  # only the king
    MINOR_GAME = (1, 2, 4, 5, 6)  # minor pieces + king
    MAJOR_GAME = (0, 3, 4, 7)  # major pieces + king

    # Pieces in the order they appear on the board
    FRONT_LINE = ('Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn')
    BACK_LINE = ('Rook', 'Knight', 'Bishop', 'Queen', 'King', 'Bishop', 'Knight', 'Rook')

    # Ranks and Files
    ROWS = (1, 2, 3, 4, 5, 6, 7, 8)
    FILES = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

    # Non-move commands player can enter during a game
    IN_GAME_COMMANDS = ['resign', 'save', 'close']


""" MENU CONTROL FLOW -------------------------------------------------------------------------------- MAIN CONTROL FLOW 
"""


def player_wants_game():
    """ Determines if player wants to play a game, see more advanced game options or quit the program """
    while True:
        print('Do you want to play a game? <yes/no>')
        print('Advanced options             <adv>')
        result = input('    :  ').lower()

        if result == 'yes':
            return 1
        elif result == 'no':
            exit_program()
        elif result == 'adv':
            return advanced_game_options()


def advanced_game_options():
    """ Gives player options about the kind of game to set up """
    while True:
        print('Play which game?')
        print('    1 - Standard game')
        print('    2 - King and Pawn game')
        print('    3 - Minor piece game')
        print('    4 - Major piece game')
        print('    help - <help>')
        print('    exit - <quit/exit/no>')
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
            print('\n')
            pass
        elif result.lower() in ('quit', 'exit', 'no'):
            exit_program()


def set_board(result):
    """ Returns a board, initialised and ready for play """
    games = (STANDARD_GAME, KING_AND_PAWN_GAME, MINOR_GAME, MAJOR_GAME)

    board = Board(games[result - 1])
    return board


def get_agent_type(player):
    """ Prompts user for info as to the type of agent to be created """
    print('There are three kinds of Agents you can initialise.')
    print('    1 - <Human> - This would be a totally manually operated agent.')
    print('                You are playing the game yourself.')
    print('    2 - <Random> - This is an agent who simply makes totally random moves.')
    print('                 They select from the set of all legal moves.')
    print('    3 - <Engine> - This is an agent which selects moves on the basis of some')
    print('                 pre-programmed algorithm.')
    print(f'\nWhich type of agent should {player} be?')

    while True:
        result = input('        :  ')
        if result.isalpha():
            result = result.lower()
            if result.lower() == 'human':
                agent_type = result.capitalize()
                break
            elif result.lower() == 'random':
                agent_type = result.capitalize()
                break
            elif result.lower() == 'engine':
                agent_type = result.capitalize()
                break
        elif result.isnumeric():
            if result == '1':
                agent_type = 'Human'
                break
            elif result == '2':
                agent_type = 'Random'
                break
            elif result == '3':
                agent_type = 'Engine'
                break

    agent_name = player
    print(f'And their name? Typing nothing will use the default name: {player}')
    while True:
        result = input('        :  ')
        if result == '':
            break
        elif result.isalnum():
            agent_name = result
            break
        else:
            print('\n        Can only include letters or numbers.\n')

    return agent_type, agent_name


def in_game_commands():
    print('    <resign> the game')
    print('    <save> the game for later continuation from current position')
    print('    <close> the program\n')


""" GAME CONTROL FLOW -------------------------------------------------------------------------------- MAIN CONTROL FLOW 
"""


def assign_players():
    """ Takes operator through process of initialising the two agents involved
        in the game - Returns two Agent() instances as player1 & player2
    """
    print('This is the Agent Creation Wizard.\n')
    print("We'll take you through the process of initialising the Agents who will be playing the game.")
    print('Player1 (white) and Player2 (black).')
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


def disambiguate(candidates, disambiguation):
    if len(disambiguation) == 1:
        if disambiguation.isalpha():
            col = FILES[disambiguation]
            results = filter(lambda x: x.location[1] == col, candidates)
        if disambiguation.isnumeric():
            results = filter(lambda x: x.location[0] == 8 - int(disambiguation), candidates)
    else:
        loc = list(disambiguation)
        results = filter(lambda x: x.location == loc, candidates)
    results = list(results)
    return results


def determine_active_piece(board, colour, candidate):
    """ Returns the active piece and target square OR throws exception.
            -> active_piece, target_location, castle_direction
    """
    if validate_san(candidate):  # if the input SAN notation is of valid format
        decomposition = active_piece_type, disambiguation, is_capture,\
            target_san, promotion_type, _, castle_direction = decompose_san(candidate)  # decompose into elements
        # print(decomposition)
        if not castle_direction:  # for any move other than castles
            target_location = convert_san2board(target_san)  # determine target location coords
            # determine which pieces are capable of making the move
            active_pieces = board.get_pieces(colour, active_piece_type, target_location)
        else:  # if we are castling
            target_sans = target_san.split()
            if colour == 'White':
                index = 0
            else:
                index = 1
            target_location = convert_san2board(target_sans[index])  # target square depends on colour
            try:  # determine which pieces are capable of making the move
                active_pieces = board.get_pieces(colour, active_piece_type, target_location)
            except ValueError('Such a castling move is not legal at this time!'):  # if none raise an exception
                raise
            print('Time to implement castling!')
        if not active_pieces:  # if the board returned 0 pieces that match the move notation
            print(active_pieces)
            print(active_piece_type)
            print(target_location)
            try:
                raise InvalidInput('No piece able to execute such a move')  # raise an exception
            except InvalidInput:
                raise
        elif len(active_pieces) == 1:  # if only 1 piece fits the criteria (colour, type, move_vision)
            active_piece, = active_pieces  # return it
        else:  # if there are more than 1 pieces  that fit
            active_pieces = disambiguate(active_pieces, disambiguation)  # utilise disambiguation string
            try:
                active_piece, = active_pieces  # there should now only be 1 piece
            except ValueError:  # if not raise an exception
                raise InvalidInput('Disambiguation insufficient: more than one piece able to make this move')
    else:  # in the case of the SAN initially failing to validate
        raise InvalidInput('Move notation failed to validate')
    return active_piece, active_piece_type, target_location, is_capture, promotion_type, castle_direction


def move_through_check(piece, location):
    """ Function specifically for use by Board.get_pieces() in the case of move-into-check calculations """
    if isinstance(piece, Pawn):
        return location in piece.capture_vision or (location in piece.supporting or location in piece.avail_captures)
    else:
        return location in piece.avail_moves or (location in piece.supporting or location in piece.avail_captures)


def squares_in_direction(start_loc, end_loc):
    """ Returns (x, y) positions occurring en-route from start_loc to end_loc.
        Must be vertical, horizontal or diagonal No Knight moves.
    """
    start_row, start_col = start_loc
    end_row, end_col = end_loc
    row_diff, col_diff = end_row - start_row, end_col - start_col

    if row_diff != 0:
        r = range(start_row, end_row + sign(row_diff), sign(row_diff))
    else:
        r = [start_row for _ in range(abs(col_diff) + 1)]
    if col_diff != 0:
        c = range(start_col, end_col + sign(col_diff), sign(col_diff))
    else:
        c = [start_col for _ in range(abs(col_diff) + 1)]

    locations = list(zip(r, c))
    print(f'locations: {locations}')
    print(f'end_loc : {end_loc}')
    if end_loc in locations:
        locations.remove(end_loc)

    return locations


def promote_pawn(board, active_piece, target_location, promotion_type):
    board.sideboard.append(active_piece)
    r, c = target_location
    board.squares[r][c] = eval(LETTERS[promotion_type])(board.player_turn, board, target_location, has_moved=True)
    board.squares[r][c].temp = active_piece.temp



def look_for_checkmate(board, colour):
    """ Raises a Checkmate exception if the designated colour is in checkmate """
    pass


def play_a_game(board, player1, player2):

    players, game_on = [player1, player2], True

    while game_on:

        try:
            agent_turn(board, *players)
        except Checkmate as checkmate:
            board, victor = checkmate.args
            print(f'                         CHECKMATE! {victor} wins!')
            print('\n                          GAME OVER!\n')
            game_on = False
            continue
        except Draw as draw:
            board = draw.args
            print('                        DRAWN GAME!')
            print('\n                         GAME OVER!\n')
            game_on = False
            continue

        board.turn_num += 0.5
        players.reverse()
        board.player_turn, = set(COLOURS) - {board.player_turn}




""" MAIN CONTROL FLOW -------------------------------------------------------------------------------- MAIN CONTROL FLOW 
"""


def exit_program():
    """ Exits the program """
    print('Okay! See you soon :)')
    sys.exit()


def not_implemented(cmd):
    print(f'<{cmd}> not implemented at this time.')
    exit_program()


def agent_turn(board, active_player, passive_player):
    """ Logic for a single player's turn """

    print(board)
    board.update_pieces(board.player_turn)

    if board.is_checkmate(active_player.colour):
        raise Checkmate(board, passive_player)
    elif board.is_draw(active_player.colour):
        raise Draw(board)
    elif board.white_in_check or board.black_in_check:
        print(f'                    {active_player.colour} in CHECK!')
    else:
        print('\n')

    print(f"{active_player} to move:")
    while True:  # this catches moving-into-check type illegal moves
        # get agent move/input - contains a close program option
        active_piece, active_piece_type, target_location, is_capture, \
            promotion_type, castle_direction = active_player.get_input(board)
        # execute move on board
        try:
            board.move(active_piece, active_piece_type, target_location, is_capture, promotion_type, castle_direction)
        # if the move would be Illegal..
        except IllegalMove as II:
            print(f'checking if : {target_location} was in avail_m or avail_cap')
            if target_location in active_piece.avail_moves:  # remove it from the set of possible moves
                print(f'found it in : avail_moves.. removing it from the list')
                active_piece.avail_moves.remove(target_location)
                print(active_piece.avail_moves)
            elif target_location in active_piece.avail_captures:  # remove it from the set of possible moves
                print(f'found it in : avail_captures.. removing it from the list')
                active_piece.avail_captures.remove(target_location)
                print(active_piece.avail_captures)
            if board.is_checkmate(active_player.colour):  # after removing the illegal move, recheck for checkmates..
                raise Checkmate(board, passive_player)
            elif board.is_draw(active_player.colour):  # and draws
                raise Draw(board)
            print(f"{active_player}'s king would have been in Check!")
            print("You'll have to choose another move.\n")
        # in the case the move is Legal and is implemented on-board..
        else:
            active_piece.has_moved = True  # mark active piece as having moved
            board.draw_counter += 0.5  # increment draw counter
            print(f'Draw counter: {board.draw_counter}')
            if isinstance(active_piece, Pawn):  # if a Pawn was the active piece
                board.draw_counter = 0  # reset draw counter
            elif is_capture:  # if there was a legal capture
                board.draw_counter = 0  # reset draw counter
            break

    # likely have to look more at CHECK situations
    # Still haven't addressed the infinite-miss of checkmate and draws via elimination


def lets_play(board, player1, player2):
    """ Main game control logic """

    # initialise game
    turn_no, game_on = 1, True

    # start game loop
    while game_on:
        print(f'Turn No. : {turn_no}.')

        print(board)
        checks, _ = board.get_checks()
        if board.is_checkmate('White'):
            print(f'                         CHECKMATE! {player2} wins!')
            print('\n                          GAME OVER!\n')
            game_on = False
            continue
        elif board.is_draw(player1.colour):
            print('                        DRAWN GAME!')
            print('\n                         GAME OVER!\n')
            game_on = False
            continue
        elif checks:
            print('                             CHECK!')
        else:
            print('\n')

        print(f"{player1} to move:")
        while True:  # this catches moving-into-check type illegal moves
            # get agent move/input - contains a close program option
            active_piece, target_location, castle_direction = player1.get_input(board)
            sideboard = len(list(board.sideboard))  # remember number of pieces on sideboard
            print(f'Side board : {sideboard}')
            # execute move on board
            try:
                board.move(active_piece, target_location, castle_direction)
                active_piece.has_moved = True  # mark active piece as having moved
                board.draw_counter += 0.5  # increment draw counter
                print(f'Draw counter: {board.draw_counter}')
                if isinstance(active_piece, Pawn):  # if a Pawn was the active piece
                    board.draw_counter = 0  # reset draw counter
                elif len(list(board.sideboard)) > sideboard:  # if there was a legal capture
                    board.draw_counter = 0  # reset draw counter
                break
            except IllegalMove as II:
                print(f'{player1.name} your king would have been in Check!')
                print("You'll have to choose another move.\n")

        print(board)
        checks, _ = board.get_checks()
        if board.is_checkmate('Black'):
            print(f'                         CHECKMATE! {player1} wins!')
            print('\n                          GAME OVER!\n')
            game_on = False
            continue
        elif board.is_draw(player2.colour):
            print('                        DRAWN GAME!')
            print('\n                         GAME OVER!\n')
            game_on = False
            continue
        elif checks:
            print('                             CHECK!')
        else:
            print('\n')

        print(f"{player2} to move:")
        while True:  # this catches moving-into-check type illegal moves
            # get agent move/input - contains a close program option
            active_piece, target_location, castle_direction = player2.get_input(board)
            sideboard = len(list(board.sideboard))  # remember number of pieces on sideboard
            print(f'Side board : {sideboard}')
            # execute move on board
            try:
                board.move(active_piece, target_location, castle_direction)
                active_piece.has_moved = True  # mark active piece as having moved
                board.draw_counter += 0.5  # increment draw counter
                print(f'Draw counter: {board.draw_counter}')
                if isinstance(active_piece, Pawn):  # if a Pawn was the active piece
                    board.draw_counter = 0  # reset draw counter
                elif len(list(board.sideboard)) > sideboard:  # if there was a legal capture
                    board.draw_counter = 0  # reset draw counter
                break
            except IllegalMove as II:
                print(f'{player2.name} your king would have been in Check!')
                print("You'll have to choose another move.\n")

        # increment turn number
        turn_no += 1


def main():
    """ Main control logic of the program
        Starts by opening up a menu suite for the player to select a game to play
        Then starts up a game
    """
    result = player_wants_game()

    board = set_board(result)
    print(board)

    player1, player2 = assign_players()

    lets_play(board, player1, player2)


def test():
    board = Board()
    print(board)

    player1, player2 = Random('Player1', 'White'), Random('Player2', 'Black')

    # lets_play(board, player1, player2)
    play_a_game(board, player1, player2)


if __name__ == '__main__':
    """ ------------------------------------------------- MAIN LOGIC ---------------------------------------------------
    """

    from Exceptions import *
    import sys
    import copy
    import random
    import math
    MAIN_VARIABLES()

    # main()

    for x in range(311):
        test()
        print(f'GAMES SINCE LAST CRASH/INFINITE LOOP!                                                              : {x}')




