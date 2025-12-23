import os

ROW_COUNT = 6
COLUMN_COUNT = 7
BOARD_SIZE = ROW_COUNT * COLUMN_COUNT
WINNING_STREAK = 4
PLAYERS = {0:"X", 1:"O"}

class terminal_colors:
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_CYAN = '\033[96m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END_C = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Print the current board to the terminal
def draw_board(board: list[str], last_move: int=-1):
    os.system('cls' if os.name == 'nt' else 'clear')
    for i in range(COLUMN_COUNT):
        print(f"  {i}", end="")
    print(" ")
    for i, spot in enumerate(board):
        spot = format_player(spot)
        if (i+1) % COLUMN_COUNT == 0: print("|" + spot + "|")
        else: print("|" + spot, end="")
    if last_move >= 0: print(f"Last move: {last_move}")

# Check what player has the turn
def check_side(ply: int) -> str:
    return PLAYERS[ply % 2]

def check_win(board: list[str], pos: int, player:str) -> bool:
    # Horizontal
    # Make a loop in the horizontal sides relative to the position (last move)
    match_count = 0
    low = (pos // COLUMN_COUNT) * COLUMN_COUNT
    high = low + COLUMN_COUNT

    for i in range(low, high):
        if board[i] == player:
            match_count += 1
            if match_count == WINNING_STREAK: return True
        else: match_count = 0
        if match_count + (high - 1 + i) < WINNING_STREAK: break

    # Vertical
    # Make a loop in the vertical sides relative to the position (last move)
    match_count = 0
    i = pos
    while i >= COLUMN_COUNT:
        i -= COLUMN_COUNT

    while i < BOARD_SIZE:
        if board[i] == player:
            match_count += 1
            if match_count == WINNING_STREAK: return True
        else: match_count = 0
        # misses optimization that calculates if the remaining spots in the column + match_count < WINNING_STREAK
        i += COLUMN_COUNT

    # DIAGONALs - we can move around the array using addition and subtraction ex:
    """
    | 0| 1| 2| 3| 4| 5| 6|
    | 7| 8| 9|10|11|12|13|
    |14|15|16|17|18|19|20|
    |21|22|23|24|25|26|27|
    |28|29|30|31|32|33|34|
    |35|36|37|38|39|40|41|
    """
    # Easy to see that adding 8 to index goes diagonally down right
    # Diagonal Up Down
    match_count = 0
    i = pos
    while i % COLUMN_COUNT != 0 and i > COLUMN_COUNT:
        i = diagonal_up_left(i)
    # Check for short diagonals
    if (4 <= i <= ROW_COUNT) or i == 21 or i == 28 or i == 35:
        i = BOARD_SIZE

    while i < 38:
        if board[i] == player:
            match_count += 1
            if match_count == WINNING_STREAK: return True
        else: match_count = 0
        # misses optimization that calculates if the remaining spots in the column + match_count < WINNING_STREAK
        if i == 27 or i == 34 or i == (BOARD_SIZE - 1 ):
            i = BOARD_SIZE
        i = diagonal_down_right(i)

    # Diagonal Down Up
    match_count = 0
    i = pos
    while i % COLUMN_COUNT != 0 and i < 35:
        i = diagonal_down_left(i)

    # Check for short diagonals
    if (39 <= i <= (BOARD_SIZE - 1 )) or i == 0 or i == COLUMN_COUNT or i == 14:
        i = - BOARD_SIZE

    while i >= 3:
        if board[i] == player:
            match_count += 1
            if match_count == WINNING_STREAK: return True
        else: match_count = 0
        # misses optimization that calculates if the remaining spots in the column + match_count < WINNING_STREAK
        if i == 20 or i == 13 or i == ROW_COUNT:
            i = - BOARD_SIZE
        i = diagonal_up_right(i)
    
    return False

# Get the corresponding column for the given spot
def get_column(move: int):
    while move >= COLUMN_COUNT:
        move -= COLUMN_COUNT
    return move


def diagonal_up_left(position: int) -> int:
    return position - COLUMN_COUNT + 1

def diagonal_down_right(position: int) -> int:
    return position + COLUMN_COUNT + 1

def diagonal_up_right(position: int) -> int:
    return position - ROW_COUNT

def diagonal_down_left(position: int) -> int:
    return position + ROW_COUNT

# Give colors and format to the player character
def format_player(player: str) -> str:
    if str.isdigit(player) and int(player) < 10: player =  " " + player
    if player == PLAYERS[0]: player = f" {terminal_colors.OK_BLUE}{player}{terminal_colors.END_C}"
    elif player == PLAYERS[1]: player = f" {terminal_colors.FAIL}{player}{terminal_colors.END_C}"
    return player
