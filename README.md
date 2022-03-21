# Geri'sGame
First project - Creating a chess program

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
`Knight`, `Bishop`, etc. inherrit from `Piece` and all appart from `King` and `Pawn` are almost entirely generic. 

I would come to see this for the error it was as it would bring about a circular dependency between the Kings (among other predictable problems).
Navigating these issuee when they arose was fidly and my eventual solutions were inneficient and unnecessarily delicate for what seems a very generic set of problems.

This is a very common problem with poorly thougtht out OO architectures and I now see that I placed far too much raw functionality of the program into the Board and Pieces. Back-to-the-drawing-board I would implement some form of GameManager class to handle the logistics.

### Validation

The user input for making moves is handled in SAN (Standard Algebraic Notation) This is the most common notation and, in my opinion, the most intuitive.

I decided to validate a given move in several stages. 
1. All pieces know their movement rules and can be called uppon to "look" at the board, populating lists of their curerntly legal moves.
2. Ensure the input is in the correct format and that it will convert into Chess language to make an actual "sentence" (eg. "Bishop to e4", "Queen takes e6")
3. Check the content of this "sentence" against the board state to verrify the pieces and squares involved actually exist and can see each other.
4. Execute the move in a temporary copy of the Board to ensure legality of edge cases w.r.t Checks and Checkmates.

Following the Python idiom ["Better to ask forgiveness than permission"](https://devblogs.microsoft.com/python/idiomatic-python-eafp-versus-lbyl/#:~:text=One%20idiomatic%20practice%20in%20Python,ask%20for%20forgiveness%20than%20permission%E2%80%9D.) I built the validation layers assuming the phrase *would* parse and the move *would* be legal, catching any errors should the step fail and re-prompting the user for another move.

# Features

### Board and Pieces..

![](https://github.com/AlexHFrench/GerrysGame/blob/master/Img/standard_board.png)
(depending on the font size of your terminal the file labels do or do not align)

### Game-types..

One can play several types of game:

![](https://github.com/AlexHFrench/GerrysGame/blob/master/Img/game_mode_menu.png)

### Agents..

One can set up a game between any arrangement of two kinds of player:

* Human Agent - controlled by a human player.
* Random Agent - Selects a random piece to move, then selects a random move from among their legal moves/captures.

![](https://github.com/AlexHFrench/GerrysGame/blob/master/Img/agent_creation_wizard.png)


### Checks, Checkmates..

The engine will catch Checks and Checkmates and, along with Draws, return the results of the game out of the game loop into the higher level of the menu system. (Though there is no implementation of any handling of that information.)

This is a typical Checkmate:

![](https://github.com/AlexHFrench/GerrysGame/blob/master/Img/checkmate.png)

Kings know which squares they cannot move into in nearly all cases. As a result these squares do not populate their lists of available moves/captures.

There is one case that is missed though, where they can move in the same direction as the attack of a Checking piece. Because the King obstructs the view of the target square the King believes it is not guarded. An Agent may then tell the King to move there and the game will try to do so.

During step 4 of the validation process indicated above, on the test board, a search for on-board Checks is made. It is then noticed that this move would leave the King in check and the test board is discarded. The Agent prompted for another move and the attempted move is removeds from the King's lists of vissible squares. 

This process can eb seen happening in the figure below.

![](https://github.com/AlexHFrench/GerrysGame/blob/master/Img/move_into_check_edge_case.png)

### Draws..

There are several types of Draw possible in Chess:
* 3-fold repition

![](https://github.com/AlexHFrench/GerrysGame/blob/master/Img/3-fold-repetition.png)

Note the [rules](https://en.wikipedia.org/wiki/Threefold_repetition#:~:text=In%20chess%2C%20the%20threefold%20repetition,as%20triple%20occurrence%20of%20position.) of 3-fold-repetition. The castling rights and en-passant statuses must also be conserved for two positions to be considered equivalent.

* 50 move rule

![](https://github.com/AlexHFrench/GerrysGame/blob/master/Img/50_move_rule.png)
* Insufficient material

![](https://github.com/AlexHFrench/GerrysGame/blob/master/Img/draw_by_insufficient_material.png)

### [FEN](https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation)..

Compressed format of board-state information storage.

Used to load games into the engine from external sources (books, online games, historical games, etc.)

A truncated form is used to store recent board states for Draw conditions (see above).

Would be used to store Save Game files in the event of implementation.


### Additional Features..
* Disambiguation of active piece in such cases where it my be ambiguous.

![](https://github.com/AlexHFrench/GerrysGame/blob/master/Img/disambiguation.png)

* Captures en-passant.
* Castling.

King side.
![](https://github.com/AlexHFrench/GerrysGame/blob/master/Img/king_side_castling.png)

Queen side.
![](https://github.com/AlexHFrench/GerrysGame/blob/master/Img/queen_side_castling.png)

Notice the different input characters used, both 0 and O are recognised.
* Promotion.

![](https://github.com/AlexHFrench/GerrysGame/blob/master/Img/promotion.png)

### Future Additions..
* Draw By Agreement
* Takebacks
* Saved Games
* Fischer Random (Chess 960)
* GUI
* Web Portal
* Game statistics and analysis (win:loss, average time per move, etc.)


## Conclusion




## How to run



