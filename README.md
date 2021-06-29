# GerrysGame
Toy project - Creating a chess program

# Introduction

This is my first actual program (outside of courses and problems, etc.)
I chose chess because I enjoy the game and wanted to work on something that matched my personal interests.

I also thought it would provide a rich place to start as a problem space and have many potential features
to itteratively add as I progress in my skills, all the way up to eventually experimenting with ML.

I did not look at any other implementations of chess boards before or during development. I made sure that all refrence materials I used (Stackoverflow etc.) were not explicitly chess related. I did this to maximise for my own learning and not the form or function of the eventual program.

As a result brace yourself. I hereby divest myself of any and all responsibility for any eye bleeding or fatal brain crashes that result from gazing uppon the following code..

# Scope

The primary purpose of the project was to develop basic skills and get my teeth into building a "real" project from scratch.

As a result the overall ethos was, "if it will run, that's good enough", with function taking precedence over space and time efficiency.

I just wanted the capacity to play a full, legal game against another human with all rules and win/draw conditions built into the program.

## Decisions

### OOP

The program running in the terminal seemed perfectly fine.
And OOP (Object Oriented Programming) was the natural choice.

I also thought it natural that the Pieces "see" the board, in that they are responsible for knowing their currently legal moves.
Further, the `Board` should handle all elements of actually moving the Pieces and resetting itself to the previous state should the move prove to be illegal.
Which meant the Board was also responsible for Checks and Mates and making the information available for Draw assessments (counting moves, storing board positions, etc.). 

Each piece has knowledge of it's currently legal moves, captures and any friendly pieces it is supporting.
`Knight`, `Bishop`, etcc. inherrit from `Piece` and all appart from `King` and `Pawn` are almost entirely generic. 

I would come to see this for the error it was as it would bring about a circular dependency between the Kings (among other predictable problems).
Navigating these issuee when they arose was fidly and my eventual solutions were inneficient and unnecessarily delicate for what seems a very generic set of problems.

This is a very common problem with poorly thougtht out OO architectures and I now see that I placed far too much raw functionality of the program into the Board and Pieces. Back-to-the-drawing-board I would implement some form of GameManager class to handle the logistics.

### Validation

The user input for making moves is handled in SAN (Standard Algebraic Notation) This is the most common notation and, in my opinion, the most intuitive.

I decided to validate a given move in several stages. 
1. All pieces know their movement rulse and can be called uppon to "look" at the board, populating all their curerntly legal moves into a list.
2. Ensure the input is in the correct format and that it will convert into Chess language to make an actual "sentence" (eg. "Bishop to e4", "Queen takes e6")
3. Check the content of this "sentence" against the board state to verrify the pieces and squares involved actually exist and can see each other.
4. Execute the move in a temporary copy of the Board to ensure legality of edge cases w.r.t Checks and Checkmates.

I followed the Python idiom ["Better to ask forgiveness than permission"](https://devblogs.microsoft.com/python/idiomatic-python-eafp-versus-lbyl/#:~:text=One%20idiomatic%20practice%20in%20Python,ask%20for%20forgiveness%20than%20permission%E2%80%9D.) and built the validation layers assuming the phrase would parse and the move would be legal, catching any errors should the step fail and re-prompting the user for another move.

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



