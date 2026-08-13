import subprocess
import sys
import unittest

class TestCardSweets(unittest.TestCase):
    def run_program(self, input_data: str) -> str:
        result = subprocess.run(
            [sys.executable, "card_sweets.py"],
            input=input_data,
            text=True,
            capture_output=True,
            check=True,
        )
        return result.stdout.strip()

    def test_example_yes(self):
        input_data = "4\n2 3 4 5\n"
        output = self.run_program(input_data)
        lines = output.splitlines()
        self.assertEqual(lines[0], "YES")
        counts = lines[1].split()
        self.assertEqual(len(counts), 2)
        alice_count = int(counts[0])
        bob_count = int(counts[1])
        self.assertGreaterEqual(alice_count, 1)
        self.assertGreaterEqual(bob_count, 1)
        self.assertEqual(len(lines[2].split()), alice_count)
        self.assertEqual(len(lines[3].split()), bob_count)

    def test_example_no(self):
        input_data = "2\n2 3\n"
        output = self.run_program(input_data)
        lines = output.splitlines()
        self.assertEqual(lines[0], "NO")
        self.assertEqual(lines[1], "0 0")

    def test_minimum_cards(self):
        input_data = "1\n5\n"
        output = self.run_program(input_data)
        lines = output.splitlines()
        self.assertEqual(lines[0], "NO")
        self.assertEqual(lines[1], "0 0")

    def test_ellipsis_fill(self):
        input_data = "5\n3 3 ...\n"
        output = self.run_program(input_data)
        lines = output.splitlines()
        self.assertEqual(lines[0], "YES")
        counts = lines[1].split()
        self.assertEqual(int(counts[0]), len(lines[2].split()))
        self.assertEqual(int(counts[1]), len(lines[3].split()))

    def test_unknown_cards(self):
        input_data = "4\no o o o\n"
        output = self.run_program(input_data)
        lines = output.splitlines()
        self.assertEqual(lines[0], "NO")
        self.assertEqual(lines[1], "0 0")

    def test_unknown_cards_legacy_marker(self):
        input_data = "4\n-1 -1 -1 -1\n"
        output = self.run_program(input_data)
        lines = output.splitlines()
        self.assertEqual(lines[0], "NO")
        self.assertEqual(lines[1], "0 0")

if __name__ == "__main__":
    unittest.main()
