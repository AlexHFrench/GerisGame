# Exceptions.py
""" This file houses the suite of custom exceptions used in the program
"""


class Error(Exception):
    """ Base class for other exceptions """
    pass


class IllegalMove(Error):
    """ Raised when a move would leave the King unprotected"""
    pass


class InvalidInput(Error):
    """ Raised when the user inputs a command not recognised by the parser """
    pass


class Draw(Error):
    """ Raised when a game has ended in a draw """
    pass


class Checkmate(Error):
    """ Raised when a game has ended in checkmate on board """
    pass


class Resignation(Error):
    """ Raised when a game has ended by a player resignation """
    pass
