import Globals
import Utils
from Board import *
from Exceptions import *
from Conversions import *
from Pieces import *
from Agents import *
import sys
import re


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

        if result in ('yes', 'y'):
            return 1
        elif result in ('adv', 'a'):
            return advanced_game_options()
        elif result in ('close', 'quit', 'exit', 'no', 'n'):
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
    games = (Globals.STANDARD_GAME,
             Globals.KING_AND_PAWN_GAME,
             Globals.MINOR_GAME,
             Globals.MAJOR_GAME)

    board = Board.Board(games[result - 1])
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
        row = Utils.flatten(row)  # individuate each element into a string of length 1 per item in the row
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
            type_, has_moved = Globals.LETTERS[letter], True  # prep piece details
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

    player1, player2, gen_colour = 'Player1', 'Player2', Utils.white_black()

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


def exit_program():
    """ Exits the program """
    print('Okay! See you soon :)')
    sys.exit()
