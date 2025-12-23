import os
from helpers import draw_board, check_side, check_win, get_column, format_player, ROW_COUNT, COLUMN_COUNT, BOARD_SIZE, PLAYERS, terminal_colors
import pprint

class Game:
    def __init__(self) -> None:
        self.board: list[str] = list(map(str, range(0, BOARD_SIZE)))
        self.playing: bool = True
        # List to track all moves
        self.moves: list[int] = []
        self.won: bool = False
        # Half moves
        self.ply: int = 0
        self.message: str = ""

    # Check if a spot is available
    def is_available(self, move: int) -> bool:
        if move > BOARD_SIZE - 1: return False
        return True if not self.board[move] in PLAYERS.values() else False
    
    # Get a list of all the possible moves on the current board
    def get_available_moves(self) -> list[int]:
        moves: list[int] = []
        for spot in enumerate(self.board):
            if self.is_available(spot[0]): moves.append(spot[0])
        moves.sort()
        return moves

    # Make a move in a given column
    def make_move(self, move: int, player: str) -> int:
        # Go down in the column until a spot occupied is found and make the move on the spot above
        while self.is_available(move):
            move += COLUMN_COUNT
        move -= COLUMN_COUNT
        self.board[move] = player
        self.moves.append(move)
        self.won = check_win(self.board, move, player)
        self.ply += 1
        return move
    
    # Remove the move in a given spot
    def revert_move(self, move: int) -> int:
        self.board[move] = str(move)
        self.won = False
        self.ply -= 1
        return self.moves.pop(move)

    # Remove the last move made in a column
    def revert_last_move(self, move: int) -> int:
        while self.is_available(move):
            move += COLUMN_COUNT
        self.board[move] = str(move)
        self.moves.pop()
        self.won = False
        self.ply -= 1
        return move

    # Print the board and end game message
    def print_end_game(self):
        draw_board(self.board, self.moves.pop())
        # Print winner if applicable
        if self.won: print(f"Player '{format_player(check_side(self.ply-1))}' {terminal_colors.OK_GREEN}Wins!{terminal_colors.END_C}")
        else: print(f"{terminal_colors.OK_CYAN}{terminal_colors.BOLD}GAME OVER - Tie!{terminal_colors.END_C}")

# Play game with two human players
def human_human():
    game = Game()
    while game.playing:
        # Reset the screen
        player = check_side(game.ply)
        draw_board(game.board)
        print(game.message + f"\nTurn {game.ply + 1} for player {format_player(player)} or press 'q' to quit")
        t0e = Kibitzer()
        t0e.best_move(game)
        # Get input from player
        move = input()
        move_int = -1
        if move == 'q':
            game.playing = False
            draw_board(game.board)
            print(f"{terminal_colors.OK_CYAN}{terminal_colors.BOLD}GAME TERMINATED{terminal_colors.END_C}")
        elif str.isdigit(move):
            move_int = int(move)
            if 0 <= move_int <= ROW_COUNT:
                # Check if spot is taken
                if game.is_available(move_int):
                    # Update board
                    move_int = game.make_move(move_int, player)
                    game.message = ""
                    if game.won: game.playing = False
                    if game.ply > BOARD_SIZE - 1: game.playing = False
                else: game.message = f"{terminal_colors.WARNING}Warning: Spot already taken{terminal_colors.END_C}"
            else: game.message = f"{terminal_colors.FAIL}Invalid move{terminal_colors.END_C}"
        else: game.message = f"{terminal_colors.FAIL}Invalid input{terminal_colors.END_C}"

    game.print_end_game()

# Play a game against the AI
def human_AI():
    game = Game()
    while game.playing:
        # Reset the screen
        player = check_side(game.ply)
        draw_board(game.board)
        print(game.message + f"\nTurn {game.ply + 1} for player {format_player(player)} or press 'q' to quit")
        if player == 'O':
            c04 = Kibitzer()
            move = c04.best_move(game)[1]
            move_int = get_column(move)
            if 0 <= move_int < len(game.board):
                if game.is_available(move_int):
                    # Update board
                    game.make_move(move_int, player)
                    game.message = ""
        else:
            move = input()
            move_int = -1
            if move == 'q':
                game.playing = False
                draw_board(game.board)
                print(f"{terminal_colors.OK_CYAN}{terminal_colors.BOLD}GAME TERMINATED{terminal_colors.END_C}")
            elif str.isdigit(move):
                move_int = int(move)
                if 0 <= move_int <= ROW_COUNT:
                    # Check if spot is taken
                    if game.is_available(move_int):
                        # Update board
                        move_int = game.make_move(move_int, player)
                        game.message = ""
                        if game.won: game.playing = False
                        if game.ply > BOARD_SIZE - 1: game.playing = False
                    else: game.message = f"{terminal_colors.WARNING}Warning: Spot already taken{terminal_colors.END_C}"
                else: game.message = f"{terminal_colors.FAIL}Invalid move{terminal_colors.END_C}"
            else: game.message = f"{terminal_colors.FAIL}Invalid input{terminal_colors.END_C}"
        if game.won: game.playing = False
        if game.ply > BOARD_SIZE - 1: game.playing = False
        
    game.print_end_game()



# Simulate game with two AI players
def AI_AI():
    game = Game()

    while game.playing:
        c04 = Kibitzer()
        player = check_side(game.ply)
        move = c04.best_move(game)[1]
        move_int = get_column(move)
        if 0 <= move_int < len(game.board):
            if game.is_available(move_int):
                # Update board
                game.make_move(move_int, player)
                game.message = ""
        if game.won: game.playing = False
        if game.ply > BOARD_SIZE - 1: game.playing = False
    game.print_end_game()

class Move:
    def __init__(self, score:float, position:int, player:str) -> None:
        self.score = score
        self.position = position
        self.player = player

    def __repr__(self):
        return f"score: {100 - self.score} position: {self.position} player: {self.player}"

class Kibitzer:
    def __init__(self) -> None:
        self.moves:dict[int, Move] = {}
        # Max values are bigger than 100 to search for the fastest win or slowest loss using depth
        self.scores:dict[str, float] = {PLAYERS[0]: -10000000000, PLAYERS[1]: 10000000000, 'tie': 0}

    # Simple implementation of the minimax function
    def minimax(self, game: Game, depth: int) -> tuple[float, int]:
        curr_side = check_side(game.ply)
        is_maximizing = False
        if curr_side == PLAYERS[0]: is_maximizing = True
        if game.won:
            score = self.scores[curr_side] - depth
            if is_maximizing:
                score = self.scores[curr_side] + depth
            return score, -1
        elif game.ply > BOARD_SIZE - 1 or  depth >= 3: return self.scores['tie'], -1
        moves = game.get_available_moves()
        limit_eval = float('inf')
        if is_maximizing: limit_eval = float('-inf')
        best_move = -1
        for spot in moves:
            # Check if the spot is available
            last_move = game.make_move(get_column(spot), curr_side)
            eval = self.minimax(game, depth + 1)[0]
            game.revert_last_move(spot)
            if (is_maximizing and eval > limit_eval) or ((not is_maximizing) and eval < limit_eval):
                limit_eval = eval
                best_move = last_move
        return limit_eval, best_move

    # Get the best move using the minimax function
    def best_move(self, game: Game):
        best_move = self.minimax(game, 0)
        pprint.pprint(f"best move: {best_move}")
        return best_move



# Menu to load game mode
def main_menu() -> None:
    waiting = True
    while waiting:
        print("Welcome! Please select a game mode from the menu below or press '0' to quit")
        print("     1. Human vs Human")
        print("     2. Human vs AI")
        print("     3. AI vs AI")
        print("     0. Quit game")
        selection = input()
        match selection:
            case '0':
                waiting = False
            case '1':
                human_human()
            case '2':
                human_AI()
            case '3':
                AI_AI()
            case _:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"{terminal_colors.FAIL}Invalid option{terminal_colors.END_C}")