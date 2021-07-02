import Globals
import main
import Board
import Pieces
import Exceptions
import random

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
            if main.validate_san(user_input):
                try:
                    active_piece, active_piece_type, target_location, is_capture, \
                        promotion_type, castle_direction = main.decompose_and_assess(board, user_input)
                except Exceptions.InvalidInput as II:  # if it flags inform the agent and re-ask for a move
                    print(f"Apologies, '{user_input}' failed to identify a unique, legal move.")
                    print(f'     :  {II}')
                    continue

                # In case promotion identifier forgotten..
                if (active_piece.__class__.__name__ == 'Pawn' and   # Moving piece is pawn..
                        (target_location[0] == 0 or target_location[0] == 7) and  # and target square is final rank
                        promotion_type == ''):  # .. and no promotion type is designated..
                    print("\nThis move will promote the pawn! What to promote to?")
                    print("k<N>ight <B>ishop <R>ook <Q>ueen")  # prompt user for info.
                    choice = input("    :    ").upper()
                    if choice in ['N', 'B', 'R', 'Q']:
                        promotion_type = Globals.LETTERS[choice]

                return active_piece, active_piece_type, target_location, is_capture, promotion_type, castle_direction

            # COMMAND PARSING AND ACTION
            elif user_input.isalpha():
                user_input = user_input.lower()
                if user_input == 'cmd':
                    main.in_game_commands()
                elif user_input == 'resign':
                    main.not_implemented('resign')
                elif user_input == 'save':
                    print(f'FEN: {main.convert_board2fen(board)}')
                    main.not_implemented('save')
                elif user_input == 'tmp':
                    with open('tmp.txt', 'r') as tmp:
                        lines = tmp.readlines()
                        print(''.join(lines))
                elif user_input in ('close', 'quit', 'exit', 'no'):
                    main.exit_program()
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
        if active_piece.__class__.__name__ == 'King':
            if abs(active_piece.location[1] - target_location[1]) == 2:  # and he's moving two squares..
                if active_piece.location < target_location:  # we're castling
                    castle_direction = 'King'  # ..note in which direction
                else:
                    castle_direction = 'Queen'  # ..note in which direction
        # If we chose a Pawn who is arriving at a final rank..
        if active_piece.__class__.__name__ == 'Pawn' and (target_location[0] == 0 or target_location[0] == 7):
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
        if main.validate_san(scripted_move):
            try:
                active_piece, active_piece_type, target_location, is_capture, \
                    promotion_type, castle_direction = main.decompose_and_assess(board, scripted_move)
            except Exceptions.InvalidInput as II:  # if it flags there is some issue in the script
                print(f"Move '{scripted_move}' loaded from script is not legal!")
                print(f'     :  {II}')
                raise
        else:
            raise Exceptions.InvalidInput(f"Move '{scripted_move}' loaded from script is not legal!")

        return active_piece, active_piece_type, target_location, is_capture, promotion_type, castle_direction


class Engine(Agent):
    """ Not implemented """

    def __init__(self, name, colour):
        super().__init__(name, colour)

    pass
