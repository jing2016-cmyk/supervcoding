import unittest
from src.tictactoe import TicTacToe

class TestTicTacToe(unittest.TestCase):
    def test_make_move_valid(self):
        game = TicTacToe()
        self.assertTrue(game.make_move(1))
        self.assertEqual(game.board[0], "X")

    def test_make_move_invalid_position(self):
        game = TicTacToe()
        self.assertFalse(game.make_move(0))
        self.assertFalse(game.make_move(10))

    def test_make_move_on_taken_cell(self):
        game = TicTacToe()
        game.make_move(1)
        self.assertFalse(game.make_move(1))

    def test_check_winner_rows(self):
        game = TicTacToe()
        game.board = ["X", "X", "X", " ", " ", " ", " ", " ", " "]
        self.assertEqual(game.check_winner(), "X")

    def test_check_winner_diagonal(self):
        game = TicTacToe()
        game.board = ["O", " ", " ", " ", "O", " ", " ", " ", "O"]
        self.assertEqual(game.check_winner(), "O")

    def test_is_draw(self):
        game = TicTacToe()
        game.board = ["X", "O", "X", "X", "O", "O", "O", "X", "X"]
        self.assertTrue(game.is_draw())

    def test_is_not_draw_with_winner(self):
        game = TicTacToe()
        game.board = ["X", "X", "X", "O", "O", " ", " ", " ", " "]
        self.assertFalse(game.is_draw())

if __name__ == "__main__":
    unittest.main()
