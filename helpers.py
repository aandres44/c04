import os

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

def draw_board(board: list[str], last_move: int=-1):
    #board = "|1|2|3|\n|4|5|6|\n|7|8|9|"
    os.system('cls' if os.name == 'nt' else 'clear')
    for i in range(7):
        print(f"  {i}", end="")
    print(" ")
    for i, spot in enumerate(board):
        spot = format_player(spot)
        if (i+1) % 7 == 0: print("|" + spot + "|")
        else: print("|" + spot, end="")
    if last_move >= 0: print(f"Last move: {last_move}")

def check_side(ply: int) -> str:
    if ply % 2 == 0: return 'O'
    else: return 'X'

def check_win(board: list[str], pos: int, player:str) -> bool:
    # Horizontal
    # Make a loop in the horizontal sides relative to the position (last move)
    match_count = 0
    #pos = position[0]
    low = (pos // 7) * 7
    high = low + 7

    for i in range(low, high):
        if board[i] == player:
            match_count += 1
            if match_count == 4: return True
        else: match_count = 0
        if match_count + (high - 1 + i) < 4: break

    # Vertical
    # Make a loop in the vertical sides relative to the position (last move)
    match_count = 0
    i = pos
    while i >= 7:
        i -= 7

    while i < 42:
        if board[i] == player:
            match_count += 1
            if match_count == 4: return True
        else: match_count = 0
        # misses optimization that calculates if the remaining spots in the column + match_count < 4
        i += 7

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
    while i % 7 != 0 and i > 7:
        i = diagonal_up_left(i)
    # Check for short diagonals
    if (4 <= i <= 6) or i == 21 or i == 28 or i == 35:
        i = 42

    #print(i)

    while i < 38:
        #print(board[i], match_count, i)
        if board[i] == player:
            match_count += 1
            if match_count == 4: return True
        else: match_count = 0
        # misses optimization that calculates if the remaining spots in the column + match_count < 4
        if i == 27 or i == 34 or i == 41:
            i = 42
        i = diagonal_down_right(i)

    # Diagonal Down Up
    match_count = 0
    i = pos
    while i % 7 != 0 and i < 35:
        i = diagonal_down_left(i)

    # Check for short diagonals
    if (39 <= i <= 41) or i == 0 or i == 7 or i == 14:
        i = -42

    while i >= 3:
        if board[i] == player:
            match_count += 1
            if match_count == 4: return True
        else: match_count = 0
        # misses optimization that calculates if the remaining spots in the column + match_count < 4
        if i == 20 or i == 13 or i == 6:
            i = -42
        i = diagonal_up_right(i)
    
    return False

def diagonal_up_left(position: int) -> int:
    return position - 8

def diagonal_down_right(position: int) -> int:
    return position + 8

def diagonal_up_right(position: int) -> int:
    return position - 6

def diagonal_down_left(position: int) -> int:
    return position + 6


def format_player(player: str) -> str:
    if str.isdigit(player) and int(player) < 10: player =  " " + player
    if player == 'X': player = f" {terminal_colors.OK_BLUE}{player}{terminal_colors.END_C}"
    elif player == 'O': player = f" {terminal_colors.FAIL}{player}{terminal_colors.END_C}"
    return player
