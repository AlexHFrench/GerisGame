import Globals
import main
import Pieces
import Exceptions
import Utils
import copy


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
        colour_generator = Utils.white_black()

        # Generate empty board
        self.squares = [[Pieces.Empty(next(colour_generator), location=(row, col)) for col in range(8)] for row in range(8)]

        # instantiate pieces
        for col in piece_positions:
            type_ = Globals.BACK_LINE[col]
            self.squares[0][col] = eval('Pieces.'+type_)('Black', self, (0, col))
            self.squares[7][col] = eval('Pieces.'+type_)('White', self, (7, col))
        for col in pawn_positions:
            self.squares[1][col] = Pieces.Pawn('Black', self, (1, col))
            self.squares[6][col] = Pieces.Pawn('White', self, (6, col))

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
        for file in Globals.FILES:
            output += file + ' ' * 2  # ' ' ' '
        output += '\n'
        return output

    def clear(self):
        """ remove all pieces from an already extant Board object
        """
        colour_generator = main.white_black()
        self.squares = [[Pieces.Empty(next(colour_generator), location=(row, col)) for col in range(8)] for row in range(8)]

    def update_pieces(self):
        """ This updates each piece; i.e. their legal moves in a given board state.
            Kings are updated last
            Of the Kings, he whose move it is updates last.
        """
        kings = list()
        for row, col in ((x, y) for x in range(8) for y in range(8)):  # for every square..
            square = self.squares[row][col]
            if isinstance(square, Pieces.Piece):  # ..that contains a piece..
                square.location = (row, col)  # update its location attribute
                if isinstance(square, Pieces.King):  # .. and unless it's a king..
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
                if isinstance(square, Pieces.Piece):  # if they contain a piece..
                    if colour is not None:
                        if square.colour != colour:  # ..and match a supplied colour..
                            continue
                    if type_ is not None:
                        if not isinstance(square, eval('Pieces.'+type_)):  # ..and match a supplied type..
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
        if isinstance(active_piece, Pieces.Pawn):  # if there's a Pawn..
            if abs(start_row - end_row) == 2:  # ..making a double step..
                path = main.squares_in_direction(start_location, target_location)
                passant_location, = set(path) - {start_location}  # identify the 'single-step' square..
                self.passant_loc = passant_location  # ..update the en_passant flag with that location..
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
            if isinstance(active_piece, Pieces.Pawn):  # ..and active_piece is a Pawn
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
        if self.test_move(active_piece, target_location):  # if the move would not leave the King in check..
            self.blind_move(original_location, target_location)  # execute the move.

            # if it's a capture..
            if is_capture:
                self.sideboard.append(active_piece.temp)  # move captured_piece to board.sideboard
                active_piece.temp = active_piece.temp.temp  # replace taken piece's .temp onto the board

            # if it's a promotion..
            if promotion_type:
                main.promote_pawn(self, active_piece, target_location, promotion_type)  # make the promotion

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
            raise Exceptions.IllegalMove(f"{active_piece.colour}'s King would be in check!")  # raise an exception

    def get_checks(self):
        """ Returns: a list of colours currently in check, i.e. ['White', 'White'] for double check
                     a list of pieces currently giving check
            The returned elements are ordered such that zip(elem1, elem2) would form matching pairs.
        """
        checks, checking_pieces = [], []
        for colour in Globals.COLOURS:  # For each colour..
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
                locations = main.squares_in_direction(piece.location, king.location)
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

        main.prepare_for_game_end(self)
        self.checkmate = True
        raise Exceptions.Checkmate('Checkmate on board!', self, last_player_to_move)

    def is_draw(self, last_player_to_move):
        """ Raises relevant Draw exception if a condition is met | Otherwise passes without action
            Exception raised has args: string(Draw text), board_object, player_object-who-last-moved
            50-move-rule, Stalemate, Insufficient mating material & 3-fold-rep. all implemented
        """
        # 50 MOVE RULE
        if self.draw_count == 50.0:
            main.prepare_for_game_end(self)
            raise Exceptions.Draw('Draw by 50 move rule!', self, last_player_to_move)

        # 3 FOLD REPETITION
        if main.three_fold_rep():
            with open('tmp.txt', 'r') as tmp:
                lines = tmp.readlines()
                print(''.join(lines))
            main.prepare_for_game_end(self)
            raise Exceptions.Draw('Draw by 3 fold repetition!', self, last_player_to_move)

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
            main.prepare_for_game_end(self)
            raise Exceptions.Draw('Draw by stalemate!', self, last_player_to_move)

        # INSUFFICIENT MATERIAL
        white_count, black_count = 0, 0
        for row in range(8):  # for all squares of the board
            for col in range(8):
                square = self.squares[row][col]
                # if there is a Pawn, Queen or Rook..
                if (isinstance(square, Pieces.Pawn) or isinstance(square, Pieces.Queen)) or isinstance(square, Pieces.Rook):
                    return  # no draw
                # it it's a minor piece..
                if isinstance(square, Pieces.Knight) or isinstance(square, Pieces.Bishop):
                    if square.colour == 'White':
                        white_count += 1  # ..count white instances
                    else:
                        black_count += 1  # ..and black instances
        if white_count >= 2 or black_count >= 2:  # if either colour has two or more minor pieces
            return  # then no draw
        else:
            main.prepare_for_game_end(self)
            raise Exceptions.Draw('Draw by insufficient material!', self, last_player_to_move)
