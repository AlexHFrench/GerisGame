
import Globals
import main
import Conversions


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
        san_loc = main.convert_board2san(self.location)
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
        self.opp_colour, = set(Globals.COLOURS) - {self.colour}
        self.location = location
        self.temp = board.squares[location[0]][location[1]]  # important during piece capture and elsewhere
        self.has_moved = has_moved  # important for castling, double-step pawn moves and captures en-passant
        self.char = Globals.UNICODES[self.colour][self.__class__.__name__]

    def __str__(self):
        return self.char

    def __repr__(self):
        avail_moves = [main.convert_board2san(x) for x in self.avail_moves]
        avail_captures = [main.convert_board2san(x) for x in self.avail_captures]
        supporting = [main.convert_board2san(x) for x in self.supporting]
        check_vision = [main.convert_board2san(x) for x in self.check_vision]

        return f'\n {self} \n'\
            f'colour: {self.colour}\n'\
            f'location: {self.location}\n'\
            f'.. in SAN: {main.convert_board2san(self.location)}\n' \
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
                if not Conversions.legal(new_row, new_col):
                    break
                self.check_vision.add((new_row, new_col))  # ..add coord to .check_vision
                square = board.squares[new_row][new_col]
                # ..and if square is empty..
                if square.__class__.__name__ == 'Empty':
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
            if not Conversions.legal(new_row, col):  # if it's on the board..
                continue
            square = board.squares[new_row][col]
            if square.__class__.__name__ == 'Empty':  # ..and empty..
                self.avail_moves.add((new_row, col))  # add it to .avail_moves
            else:
                break

        # PAWNS capture diagonally..
        for i, j in self.pattern:  # for each forward-diagonal-direction..
            new_row = self.location[0] + i * self.direction  # step once
            new_col = self.location[1] + j * self.direction  # step once
            # if square is on the board..
            if not Conversions.legal(new_row, new_col):
                continue
            self.check_vision.add((new_row, new_col))  # ..add coord to .check_vision
            # if the square is the en passant location..
            if board.passant_loc == (new_row, new_col):
                self.avail_captures.add((new_row, new_col))  # ..add it to .avail_captures
            square = board.squares[new_row][new_col]
            # if there is a piece there..
            if square.__class__.__name__ == 'Piece':
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
            if not Conversions.legal(new_row, new_col):
                continue
            self.check_vision.add((new_row, new_col))  # ..add coord to .check_vision
            square = board.squares[new_row][new_col]
            # If the coord is empty..
            if square.__class__.__name__ == 'Empty':
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
                        if Conversions.legal(row, new_col):  # if the next square is on the board..
                            square = board.squares[row][new_col]  # check it
                            if square.__class__.__name__ == 'Empty':  # if it's empty and not visible to opponent..
                                if board.get_pieces(self.opp_colour, in_check_vision=square.location) is not None:
                                    new_col += j  # keep going
                                    continue
                            elif square.__class__.__name__ == 'Rook':  # if it's a rook and it's not moved..
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
