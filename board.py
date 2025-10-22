# --------------------------------------------------------
# board.py
# 19x19 board for Connect6
# Handles stone placement and win checking.
# --------------------------------------------------------

from typing import List, Tuple, Optional
from protocol import LETTERS

# Constants for readability
EMPTY = 0
BLACK = 1
WHITE = 2
SIZE = 19 


DIRS = [(1, 0), (0, 1), (1, 1), (1, -1)]

class Board:
    def __init__(self):
        # Create empty 19x19 grid
        self.grid = [[EMPTY] * SIZE for _ in range(SIZE)]
        self.to_move = BLACK  # Black starts
        self.num_moves = 0

    def inside(self, x: int, y: int) -> bool:
        """Check if position is on the board."""
        return 0 <= x < SIZE and 0 <= y < SIZE

    def get(self, x: int, y: int) -> int:
        """Get content of a cell (0=empty, 1=black, 2=white)."""
        return self.grid[y][x]

    def place(self, stones: List[Tuple[int, int]], color: int) -> bool:
        """Place stones on the board. Returns True if the move is valid."""
        for (x, y) in stones:
            if not self.inside(x, y) or self.get(x, y) != EMPTY:
                return False  # invalid move
        for (x, y) in stones:
            self.grid[y][x] = color
        self.num_moves += len(stones)
        return True

    def has_winner(self) -> Optional[int]:
        """Checks if any player has six or more stones in a row."""
        for y in range(SIZE):
            for x in range(SIZE):
                color = self.get(x, y)
                if color == EMPTY:
                    continue
                for dx, dy in DIRS:
                    count = 1
                    nx, ny = x + dx, y + dy
                    while self.inside(nx, ny) and self.get(nx, ny) == color:
                        count += 1
                        nx += dx
                        ny += dy
                    if count >= 6:
                        return color
        return None

    def print_ascii(self) -> str:
        """Return a ASCII version of the board."""
        lines = ["   " + " ".join(LETTERS)]  # top letters
        for y in range(SIZE - 1, -1, -1):
            row = []
            for x in range(SIZE):
                cell = self.get(x, y)
                if cell == EMPTY:
                    row.append(".")
                elif cell == BLACK:
                    row.append("X")
                else:
                    row.append("O")
            lines.append(f"{LETTERS[y]:>2} " + " ".join(row))
        return "\n".join(lines)
