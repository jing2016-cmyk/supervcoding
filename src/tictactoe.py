import os

class TicTacToe:
    def __init__(self):
        self.board = [" "] * 9
        self.current_player = "X"

    def display_board(self):
        os.system("cls" if os.name == "nt" else "clear")
        print("Tic Tac Toe")
        print("-------------")
        for row in range(3):
            row_cells = self.board[row * 3:(row + 1) * 3]
            print(f"| {' | '.join(row_cells)} |")
            print("-------------")

    def make_move(self, position: int) -> bool:
        if position < 1 or position > 9:
            return False
        index = position - 1
        if self.board[index] != " ":
            return False
        self.board[index] = self.current_player
        return True

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def winning_combinations(self):
        return [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6),
        ]

    def check_winner(self):
        for a, b, c in self.winning_combinations():
            if self.board[a] != " " and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        return None

    def is_draw(self):
        return all(cell != " " for cell in self.board) and self.check_winner() is None

    def play_game(self):
        while True:
            self.display_board()
            winner = self.check_winner()
            if winner:
                print(f"Player {winner} wins!\n")
                break
            if self.is_draw():
                print("It's a draw!\n")
                break

            try:
                position = int(input(f"Player {self.current_player}, choose a position (1-9): "))
            except ValueError:
                print("Please enter a valid number between 1 and 9.")
                input("Press Enter to continue...")
                continue

            if not self.make_move(position):
                print("That move is not valid. Choose an empty cell between 1 and 9.")
                input("Press Enter to continue...")
                continue

            self.switch_player()

        self.display_board()
        print("Thanks for playing!")


if __name__ == "__main__":
    TicTacToe().play_game()
