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
        'Bishop': 'B', 'King': 'K', 'Queen': 'Q',
        'Empty': ''},
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