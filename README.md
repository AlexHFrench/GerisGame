# GerrysGame
Toy project - Creating a chess program

## Introduction

This is my first actual program (outside of courses and problems, etc.)
I chose chess because I enjoy the game and wanted to work on something that matched my personal interests.

I also thought it would provide a rich place to start as a problem space and have many potential features
to itteratively add as I progress in my skills, all the way up to eventually experimenting with ML.

## Scope

The primary purpose of the project was to develop basic skills and get my teeth into building a "real" project from scratch.

As a result the overall ethos was, "if it will run, that's good enough", with function taking precedence over space and time efficiency.

I just wanted the capacity to play a full, legal game against another human with all rules and win/draw conditions built into the program.

## Decisions

The program running in the terminal seemed perfectly fine.
And OOP (Object Oriented Programming) was the natural choice.

I also thought it natural that the Pieces "see" the board, in that they are responsible for knowing their currently legal moves.
Further, the `Board` should handle all elements of actually moving the Pieces and resetting itself to the previous state should the move prove to be illegal.
Which meant the Board was also responsible for Checks and Mates and making the information available for Draw assessments. 

Each piece has knowledge of it's currently legal move, capture and any friendly pieces it is supporting.
`Knight`, `Bishop`, etcc. inherrit from `Piece` and all appart from `King` and `Pawn` are almost entirely generic. 

I would come to see this for the error it was as it would bring about a circular dependency between the Kings.
Navigating this issue when it arose was fidly and my eventual solution was inneficient and unnecessarily delicate for what seems a very generic problem.

This is a very common problem with poorly thougtht out OO architectures and I've learned that I placed far too much of the raw functionality of the program into the board and Pieces. Back-to-the-drawing-board I would implement some form of GameManager class to handle the logistics.


# Features

### Game-types..

One can play several types of game:
* Standard 
* King and Pawn
* Minor Piece
* Major Piece

### Agents..

One can set up a game between any arrangement of two kinds of player:
* Human Agent - controlled by a human player.
* Random Agent - Selects a random piece to move, then selects a random move from among their legal moves/captures.

### Board and Pieces..
### Rules..
### Checks, Checkmates..
### Draws..

There are several types of Draw possible in Chess:
* 3-fold repition
* 50 move rule
* Insufficient material
* 

### FENs..
### Future Additions..
* Draw By Agreement
* Takebacks
* Saved Games
* Fischer Random (Chess 960)
* GUI
* Web Portal


## Conclusion




## How to run



