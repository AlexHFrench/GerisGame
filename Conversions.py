import Globals
import re


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
        coord = (8 - int(number), Globals.FILES[letter])
    return coord


def convert_board2san(coord):
    """ Takes a PRE-VALIDATED coordinate of the form:   tuple(row, col)
        Returns a coordinate in SAN (Standard Algebraic Notation) : "a4" or "h6" for example
        Completely capable of crashing the program if input is not valid
    """
    result = []
    if coord:
        rank = 8 - coord[0]
        files = list(Globals.FILES.keys())
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
        if elem in Globals.LETTERS:
            result[i] = Globals.LETTERS[elem]

    return tuple(result)