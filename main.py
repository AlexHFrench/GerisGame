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
""" CLASSES ------------------------------------------------------------------------------------------------------------
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
        self.backup = None
        colour_generator = white_black()
        self.squares = [[Empty(next(colour_generator)) for _ in range(8)] for _ in range(8)]
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

        for row, col in ((x, y) for x in range(8) for y in range(8)):  # give pieces vision of the board
            square = self.squares[row][col]
            if isinstance(square, Piece):
                square.look(self)

    def __str__(self, ):
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
        output += '\n' * 2
        return output

    def clear(self):
        """ remove all pieces from an already extant Board object
        """
        colour_generator = white_black()
        self.squares = [[Empty(next(colour_generator)) for _ in range(8)] for _ in range(8)]

    def move(self, start_square, fin_square):
        """ move object from start_square to fin_square; remove residue of object from start_square
            accepts squares in SAN chess notation
        """
        pass

    def get_pieces(self, colour=None, kind=None, line_of_sight=None):
        """ Returns all pieces on the board which match the given criteria. """
        pieces = flatten(self.squares)
        pieces = filter(lambda x: isinstance(x, Piece), pieces)
        if colour:
            pieces = filter(lambda x: x.colour == colour, pieces)
        if kind:
            pieces = filter(lambda x: isinstance(x, eval(kind)), pieces)
        if line_of_sight:
            pieces = filter(lambda x: line_of_sight in x.avail_moves
                            or line_of_sight in x.avail_captures, pieces)
        pieces = list(pieces)
        return pieces


class Empty:
    """ Empty square, place holder object. Has a colour."""

    def __init__(self, colour):
        self.colour = colour

    def __str__(self):
        return '―' 


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
        self.avail_moves, self.avail_captures, self.supporting = set(), set(), set()
        self.pattern, self.steps = None, None
        self.colour = colour
        self.location = location
        self.square = board.squares[location[0]][location[1]]
        self.has_moved = has_moved  # important for castling, double-step pawn moves and captures en-passant
        self.char = UNICODES[self.colour][self.__class__.__name__]

    def __str__(self):
        return self.char

    def __repr__(self):
        avail_moves = [convert_board2san(x) for x in self.avail_moves]
        avail_captures = [convert_board2san(x) for x in self.avail_captures]
        supporting = [convert_board2san(x) for x in self.supporting]

        return '\n' + str(self) + '\n'\
            'colour: ' + self.colour + '\n'\
            'location: ' + str(self.location) + '\n'\
            '.. in SAN: ' + convert_board2san(self.location) + '\n'\
            'available moves: ' + str(avail_moves) + '\n'\
            'available captures: ' + str(avail_captures) + '\n' \
            'supporting: ' + str(supporting) + '\n' \
            'has moved: ' + str(self.has_moved)

    def look(self, board):
        """Piece populates self.avail_moves and self.avail_captures with legal board indices."""
        for i, j in self.pattern:
            new_row = self.location[0] + i
            new_col = self.location[1] + j

            for _ in range(self.steps):
                if not legal(new_row, new_col):
                    break
                square = board.squares[new_row][new_col]
                if isinstance(square, Empty):
                    self.avail_moves.add((new_row, new_col))
                    new_row += i
                    new_col += j
                elif square.colour != self.colour:
                    self.avail_captures.add((new_row, new_col))
                    break
                else:
                    self.supporting.add((new_row, new_col))
                    break

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
        self.pattern = [(1, 1), (1, -1)]
        self.steps = 1
        if colour == 'White':
            self.direction = -1  # used to orient the piece on the board; pawns are not omni-directional
        else:
            self.direction = 1

    def look(self, board):
        """Piece populates self.avail_moves and self.avail_captures with legal board indices."""
        new_row, _ = row, col = self.location
        if not self.has_moved:
            self.steps = 2
        # Look for places the pawn can legally move
        for _ in range(self.steps):
            new_row += self.direction
            square = board.squares[new_row][col]
            if isinstance(square, Empty):
                self.avail_moves.add((new_row, col))
            else:
                break
        self.steps = 1
        # Look for pieces the pawn can legally capture
        for i, j in self.pattern:
            new_row = self.location[0] + i * self.direction
            new_col = self.location[1] + j * self.direction
            if not legal(new_row, new_col):
                break
            square = board.squares[new_row][new_col]
            if isinstance(square, Piece) and square.colour != self.colour:
                self.avail_captures.add((new_row, new_col))
            else:
                break


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
        self.steps = 1


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


""" IO -----------------------------------------------------------------------------------------------------------------
"""


def get_player_move():
    """ returns a move selected by the player in SAN
    """
    player_input = input('What is your move?\n\t:\t')

    return player_input


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
    """ validates a string is compliant to the notation conventions of SAN >>
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
        castling: 0-0, 0-0-0 for king and queen side respectively
        check: trailing '+'
        checkmate: trailing '#'
        end of game: 1-0, 0-1, ½-½ for white victory, black victory and draw respectively
    """
    result = re.search('[RNBQK]?[a-h]?[1-8]?[x]?[a-h][1-8][RNBQ]?[+#]?|0-0-?0?', san)
    return result


def decompose_san(san):
    """ for details of SAN see docstring for validate_san above
        take a pre-validated san string and returns:
            (0 - active piece type - STR,
             1 - active piece disambiguation - STR,
             2 - captures - BOOL,
             3 - target square - STR,
             4 - post-promotion piece type - STR,
             5 - check/check-mate claim - STR
             6 - castles - STR)
    """
    result = ['', '', False, '', '', '', '']

    if san == '0-0':
        result = ['King', '', False, '', '', '', 'King']
        return tuple(result)
    if san == '0-0-0':
        result = ['King', '', False, '', '', '', 'Queen']
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
    """ --------------------------- IMPORTS
        """
    global re
    import re

    """ --------------------------- MAIN VARIABLES
    """
    global VALUES, LETTERS, PATTERNS, STEPS, UNICODES, STARTING_ROWS, STANDARD_GAME
    global KING_AND_PAWN_GAME, MINOR_GAME, MAJOR_GAME, FRONT_LINE, BACK_LINE, ROWS, FILES

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
    KING_AND_PAWN_GAME = (4,)  # only the king
    MINOR_GAME = (1, 2, 4, 5, 6)  # minor pieces + king
    MAJOR_GAME = (0, 3, 4, 7)  # major pieces + king

    # Holds all game-type - used in tests.py
    GAME_TYPES = (
        STANDARD_GAME,
        KING_AND_PAWN_GAME,
        MINOR_GAME,
        MAJOR_GAME,
    )

    # Pieces in the order they appear on the board
    FRONT_LINE = ('Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn')
    BACK_LINE = ('Rook', 'Knight', 'Bishop', 'Queen', 'King', 'Bishop', 'Knight', 'Rook')

    # Ranks and Files
    ROWS = (1, 2, 3, 4, 5, 6, 7, 8)
    FILES = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}


""" MAIN ---------------------------------------------------------------------------------------------------------- MAIN
"""

if __name__ == '__main__':
    """ ------------------------------------------------- MAIN BODY ----------------------------------------------------
    """

    MAIN_VARIABLES()






