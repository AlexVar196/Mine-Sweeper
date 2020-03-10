import random
import time
import datetime
import constants as c

from termcolor import cprint, colored

stillPlaying = True
correctFlagCounter = 0
flagsLeft = 0
timerStart = 0

def getTotalTime(endTime):
    """
    Calculates the total play time.
    returns a string.
    """
    global timerStart
    totalTime = endTime - timerStart
    conversion = datetime.timedelta(seconds=int(totalTime))
    converted_time = str(conversion)
    return converted_time


def restart():
    """
    Restarts the program and gets back to the main menu.
    All data reset.
    Menu options are P for play
                     I for instructions
                     Q for quit
    Option to choose difficulty e (easy)
                                m (medium)
                                h (hell)
    """

    global correctFlagCounter, timerStart, flagsLeft, stillPlaying
    correctFlagCounter, timerStart, flagsLeft, stillPlaying = 0, 0, 0, True
    cprint('''
     M e n u
===================
Type P to play
Type I to get instructions
Type Q to quit''', 'magenta')

    command = input('>>>')

    if command == 'P':
        cprint("choose difficulty", 'magenta')
        difficulty = input(colored('''
difficulty: "e" - easy(10 mines) 
            "m" - medium(20 mines)
            "h" - hell(20 mines)\n>>>''', 'magenta'))
        if difficulty == 'e':
            startGame(c.easyMode)
        elif difficulty == 'm':
            startGame(c.mediumMode)
        elif difficulty == 'h':
            startGame(c.hellMode)
        else:
            restart()
    elif command == 'I':
        printInfo()
    elif command == 'Q':
        cprint('Thanks for playing!', 'blue')
        exit()
    else:
        restart()


def startGame(mode):
    """
    Starts game with the chosen mode.
    Creates two boards, actual one with answers and a blank one that player sees.
    Starts timer.
    While in game mode, keeps taking input command:
    --> f (flag)
    --> s (Step)
    --> q (Quit)
    and then Row and Column input.
    :param mode: integer 10 or 20 or 30
    :return: None
    """
    global timerStart, stillPlaying, flagsLeft
    actualBoard = createBoard(mode)
    # Uncomment next line to see the actual board.
    # displayBoard(actualBoard)
    playerBoard = createPlayerBoard()
    displayBoard(playerBoard)
    timerStart = time.time()
    flagsLeft = mode

    while stillPlaying:
        if correctFlagCounter == mode:
            stillPlaying = False
            endTime = time.time()
            st = 'YOU WON!!! Time: ' + getTotalTime(endTime) + ' seconds'
            cprint(st, color='cyan')
            # Uncomment next line to see the actual board.
            # displayBoard(actualBoard)
            restart()

        s_row = colored('Pick Row(0-9): ', 'blue')
        s_column = colored('Pick Column(A-J): ', 'cyan')
        s_command = colored('''
What to do? 
--> f (flag) 
--> s (Step) 
--> q (Quit)
>>>''', 'green')
        command = input(s_command).lower()
        if command == 'q':
            cprint('Thanks for playing!', 'blue')
            exit()
        row = input(s_row)
        if row == 'q':
            cprint('Thanks for playing!', 'blue')
            exit()
        column = input(s_column).lower()
        if column == 'q':
            cprint('Thanks for playing!', 'blue')
            exit()

        if command == 'f':
            flag(row, column, playerBoard, actualBoard)
        elif command == 's':
            step(row, column, playerBoard, actualBoard)


def flag(row, column, playerBoard, actualBoard):
    """
    Puts a flag.
    If flag is put on a location where there is actually a mine,
    correctFlagCounter goes up. If reaches the number of actual mines, player won.
    Number of flags equals the number of mines and player can get flags back
    by unflagging an existing flag.
    :param row: String
    :param column: Int
    :param playerBoard: 2d Array filled with all data
    :param actualBoard: 2d array filled with '_'
    :return: None
    """
    r = int(row)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    rows = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    global correctFlagCounter, flagsLeft

    if column in letters:
        if r in rows:
            column = getColumn(column)
            if flagsLeft > 0:
                if actualBoard[r][column] == '*':
                    correctFlagCounter += 1
                if playerBoard[r][column] == '_':
                    playerBoard[r][column] = colored(str(c.flagChar), 'green')
                    flagsLeft -= 1
                    print('\n>>> flags left:', flagsLeft)
            elif playerBoard[r][column] == colored(str(c.flagChar), 'green'):
                playerBoard[r][column] = '_'
                flagsLeft += 1
                print('\n>>> flags left: ', flagsLeft)
            else:
                cprint('Sorry, you ran out of flags. Unflag some by flagging same coordinates', color='red')
        else:
            cprint("row not in range B", color='red')
    else:
        cprint("column nor in range C", color='red')

    displayBoard(playerBoard)


def getColumn(column):
    """
    :arg column: string
    :return i: integer value of the letter index
    """
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    for i in range(len(letters)):
        if letters[i] == column:
            return i


def step(row, column, playerBoard, actualBoard):
    """
    Steps on coordinate. If stepped on a mine, player looses.
    Else, if it's a zero - opens all surrounding slots.
    If its any other digit, just reveals the digit.
    :param row: integer
    :param column: string
    :param playerBoard: 2d Array filled with all data
    :param actualBoard: 2d array filled with '_'
    :return: None
    """
    print('stepping on [', row, 'x', column, ']')
    r = int(row)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    rows = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    if column in letters:
        if r in rows:
            column = getColumn(column)
            if checkSquare(r, column, actualBoard):
                cprint('''

##############################
###   !!!   BOOOOM   !!!   ###
### you stepped on a mine! ###
##############################'''
                       , color='red')
                displayBoard(actualBoard)
                global stillPlaying
                stillPlaying = False
                endTime = time.time()
                st = 'Thank you for playing! Time: ' + getTotalTime(endTime) + ' seconds'
                cprint(st, color='cyan')
                restart()

            else:
                cprint('we are still alive', color='green')
                playerBoard[r][column] = actualBoard[r][column]
                if playerBoard[r][column] == 0:
                    openTiles(r, column, playerBoard, actualBoard)
        else:
            cprint("row not in range", color='red')
    else:
        cprint("column nor in range", color='red')

    displayBoard(playerBoard)


def openTiles(r, column, playerBoard, actualBoard):
    """
    Opens the surrounding tiles around the chosen step.
    :param r: row - integer
    :param column: integer
    :param playerBoard: 2d Array filled with all data
    :param actualBoard: 2d array filled with '_'
    :return: playerBoard
    """
    if r - 1 > -1:
        row = playerBoard[r - 1]
        if column - 1 > -1:
            row[column - 1] = actualBoard[r - 1][column - 1]
        row[column] = playerBoard[r - 1][column]
        if 10 > column + 1:
            row[column + 1] = actualBoard[r - 1][column + 1]
        row[column] = actualBoard[r - 1][column]
    displayBoard(actualBoard)

    row = playerBoard[r]
    if column - 1 > -1:
        row[column - 1] = actualBoard[r][column - 1]
    if 10 > column + 1:
        row[column + 1] = actualBoard[r][column + 1]

    if 10 > r + 1:
        row = playerBoard[r + 1]
        if column - 1 > -1:
            row[column - 1] = actualBoard[r + 1][column - 1]
        row[column] = playerBoard[r - 1][column]
        if 10 > column + 1:
            row[column + 1] = actualBoard[r + 1][column + 1]
        row[column] = actualBoard[r - 1][column]

    return playerBoard


def checkSquare(row, column, board):
    """
    Checks if chosen spot has a mine
    :param row: int
    :param column: int
    :param board: actual board
    :return: boolean true if has mine, false otherwise.
    """
    if board[row][column] == '*':
        return True
    else:
        return False


def placeBombs(board, mines):
    """
    Places bombs randomly on the board while creation.
    :param board: actual board
    :param mines: number of mines to put
    :return: board
    """
    while mines != 0:
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        # print('x: ', x, 'y: ', y)
        if board[x][y] == '*':
            continue
        else:
            board[x][y] = '*'
            # analyzeBoard(x, y, board)
            mines -= 1

    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] == '*':
                updateValues(row, column, board)

    return board


def updateValues(r, column, board):
    """
    Updates the values on the actual board. Svery non-mine spot will have a
    number indicating how many bombs are next to it.
    :param r: row - integer
    :param column: - integer
    :param board: 2d array actual board
    :return: board
    """
    if r - 1 > -1:
        row = board[r - 1]
        if column - 1 > -1:
            if row[column - 1] != '*':
                row[column - 1] += 1
        if row[column] != '*':
            row[column] += 1
        if 10 > column + 1:
            if row[column + 1] != '*':
                row[column + 1] += 1

    row = board[r]
    if column - 1 > -1:
        if row[column - 1] != '*':
            row[column - 1] += 1
    if 10 > column + 1:
        if row[column + 1] != '*':
            row[column + 1] += 1

    if r + 1 < 10:
        row = board[r + 1]
        if column - 1 > -1:
            if row[column - 1] != '*':
                row[column - 1] += 1
        if row[column] != '*':
            row[column] += 1
        if 10 > column + 1:
            if row[column + 1] != '*':
                row[column + 1] += 1

    return board


def displayBoard(board):
    """
    Displays the board in terminal
    :param board:
    :return: None
    """
    print(colored('##############################', 'magenta'))
    rows = [colored('##   ', 'magenta'), 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', colored('  ##', 'magenta')]
    for i in range(len(rows)):
        st = colored(rows[i], 'blue')
        print(st, end=' ', sep=' ')
    print()
    cprint('##                          ##', color='magenta')
    for row in range(len(board)):
        st1 = colored('## ', 'magenta')
        st2 = colored(str(row), 'cyan')
        st3 = colored('  ', 'blue')
        st4 = st1 + st2 + st3
        print(st4, end='')
        for column in range(len(board[row])):
            val = board[row][column]
            if isinstance(val, int):
                print(val, end=' ')
            elif isinstance(val, str):
                if val == '_':
                    print(val, end=' ')
                elif val == '*':
                    cprint(val, color='red', end=' ')
                else:
                    cprint(val, color='green', end=' ')
            else:
                cprint(val, color='green', end=' ')

        print('  ##')
    print()


def createBoard(mines):
    """
    Creates a 10x10 board (2d array) and fills with value 0
    :param mines: number of bombs
    :return: board
    """
    board = [[0 for r in range(10)]
             for c in range(10)]

    board = placeBombs(board, mines)
    return board


def createPlayerBoard():
    """
    Creates a 10x10 board (2d array) and fills with string '_'
    :return: board
    """
    board = [['_' for r in range(10)]
             for c in range(10)]
    return board


def printInfo():
    """
    Prints Instructions in terminal
    :return: None
    """
    cprint('''
    Instructions
    ============     
 >  Type P to play
        - Pick action:
          flag - put flag
          step - step on field and risk getting a boom!
        - Pick row coodrinate (0 - 9)
        - Pick Column coordinate (A - J)  
 >  Type I to get instructions
 >  Basically don't blow yourself up
 >  Easy mode has 10 mines, medium has 20 and hell mode has 30 mines.
 >  The number of flags you get is equal to number of mines.
 >  You can get a flag back if you unflag an existing flag by flagging same coordinates
 >  If you put all flags on all the mines, you win!
 >  If you step on a mine, you lose!  
 >  Good luck!!!
 
 ''', 'red')
    restart()


restart()
