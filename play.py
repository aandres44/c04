#import os
from helpers import draw_board, check_side, check_win, format_player, terminal_colors

class Game:
    def __init__(self) -> None:
        #rows, cols = (6, 7)
        #self.board: list[str] = ["."]*cols*rows
        self.board: list[str] = list(map(str, range(0, 41 + 1)))
        self.playing = True
        # add list to track all moves
        self.last_move = -1
        self.won = False
        # Half moves
        self.ply = 0
        self.message = ""

    def is_available(self, move: int) -> bool:
        print(move)
        if move > 41: return False
        return True if not self.board[move] in {"X", "O"} else False

    def make_move(self, move: int, player: str):
        #go down in the column until a spot occupied is found and make the move on the spot above
        while self.is_available(move):
            move += 7
        move -= 7
        print(move, " make")
        self.board[move] = player
        self.last_move = move
        return move
    
    def revert_move(self, move: int):
        self.board[move] = str(move)

    def revert_last_move(self) -> None:
        if 0 <= self.last_move <= 41:
            self.board[self.last_move] = str(self.last_move)
        # When the list to track all moves is implemented pop the previous last move to store it here
        self.last_move = -1

    def print_end_game(self):
        draw_board(self.board, self.last_move)
        # Print winner if applicable
        if self.won: print(f"Player '{format_player(check_side(self.ply-1))}' {terminal_colors.OK_GREEN}Wins!{terminal_colors.END_C}")
        else: print(f"{terminal_colors.OK_CYAN}{terminal_colors.BOLD}GAME OVER - Tie!{terminal_colors.END_C}")

def human_human():
    game = Game()

    while game.playing:
        # Reset the screen
        player = check_side(game.ply)
        draw_board(game.board)
        print(game.message + f"\nTurn {game.ply + 1} for player {format_player(player)} or press 'q' to quit")
        #t0e = Kibitzer()
        #t0e.best_move(game, game.ply)
        # Get input from player
        move = input()
        move_int = -1
        if move == 'q':
            game.playing = False
            draw_board(game.board)
            print(f"{terminal_colors.OK_CYAN}{terminal_colors.BOLD}GAME TERMINATED{terminal_colors.END_C}")
        elif str.isdigit(move):
            move_int = int(move)
            if 0 <= move_int <= 6:
                # Check if spot is taken
                if game.is_available(move_int):
                    # Update board
                    move_int = game.make_move(move_int, player)
                    game.ply += 1
                    game.message = ""
                    if check_win(game.board, move_int, player): game.playing, game.won = False, True
                    if game.ply > 41: game.playing = False
                else: game.message = f"{terminal_colors.WARNING}Warning: Spot already taken{terminal_colors.END_C}"
            else: game.message = f"{terminal_colors.FAIL}Invalid move{terminal_colors.END_C}"
        else: game.message = f"{terminal_colors.FAIL}Invalid input{terminal_colors.END_C}"

    game.print_end_game()

def AI_AI():
    game = Game()

    while game.playing:
        c04 = Kibitzer()
        player = check_side(game.ply)
        move = c04.best_move(game, game.ply)[0].position
        move_int = int(move) - 1
        if 0 <= move_int < len(game.board):
            if game.is_available(move_int):
                # Update board
                game.make_move(move_int, player)
                game.ply += 1
                game.message = ""

        if check_win(game.board, move, player): game.playing, game.won = False, True
        if game.ply > 8: game.playing = False

    game.print_end_game()

from helpers import check_side, check_win
import pprint

class Move:
    def __init__(self, score:float, position:int, player:str) -> None:
        self.score = score
        self.position = position
        self.player = player

    def __repr__(self):
        return f"score: {100 - self.score}' position: {self.position}) player: {self.player}"

class Kibitzer:
    def __init__(self, p1:str='O', p2:str='X') -> None:
        self.p1 = p1
        self.p2 = p2
        self.moves:dict[int, Move] = {}
        # Max values are bigger than 100 to search for the fastest win or slowest loss using depth
        self.scores:dict[str, float] = {p1: -100, p2: 100, 'tie': 0}

    def minimax(self, game: Game, depth: int, is_maximizing: bool, ply: int)->float:
        curr_side = check_side(ply)
        if check_win(game.board, game.last_move, curr_side):
            score = self.scores[curr_side] - depth
            if is_maximizing:
                score = self.scores[curr_side] + depth
            return score
        elif ply > 8: return self.scores['tie']

        limit_eval = float('inf')
        player = self.p2
        if is_maximizing: 
            limit_eval = float('-inf')
            player = self.p1
        for i in range(7):
            # Check if the spot is available
            if not game.board[i] in {'X', 'O'}:
                last = game.make_move(i, player)
                eval = self.minimax(game, depth + 1, not is_maximizing, ply + 1)
                game.revert_move(last)
                #max_eval = max(max_eval, eval)
                if (is_maximizing and eval > limit_eval) or ((not is_maximizing) and eval < limit_eval):
                    limit_eval = eval
                    self.moves[depth] = Move(eval, i+1, curr_side)
        self.moves = dict(sorted(self.moves.items()))
        return limit_eval

    def best_move(self, game: Game, ply: int):
        self.moves = {}
        # p1 to make its turn
        max = False
        if check_side(ply) == 'O': max = True
        pprint.pprint(f"minimax: {self.minimax(game, 0, max, ply)}, best move: {self.moves}")
        return self.moves




def main_menu() -> None:
    """test = Game()
    test.board[4] = "X"
    test.board[9] = "X"
    test.board[16] = "X"
    #test.board[23] = "X"
    #test.board[3] = "X"
    #test.board[4] = "X"
    #test.board[5] = "X"
    test.board[10] = "X"
    test.board[18] = "X"
    test.board[22] = "X"
    draw_board(test.board)
    print(check_win(test.board, 16, "X"))"""
    human_human()