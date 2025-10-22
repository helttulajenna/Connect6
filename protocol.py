# --------------------------------------------------------
# protocol.py
# Converts between coordinate strings and (x, y) positions
# Used by the Connect6 engine to read and print moves.
# --------------------------------------------------------

from typing import List, Tuple

# Letters used on the board (A–S = 19 positions)
LETTERS = "ABCDEFGHIJKLMNOPQRS"

def is_valid_sq(token: str) -> bool:
    """
    Check if a coordinate like 'JJ' is valid.
    Both characters must be between A and S.
    """
    return len(token) == 2 and all(c in LETTERS for c in token)

def parse_squares(compact: str) -> List[Tuple[int, int]]:
    """
    Convert a compact string (like 'ASBS' or 'JJJJ')
    into a list of coordinates [(x1, y1), (x2, y2), ...].

    Each position = 2 letters:
      - first = column (A–S)
      - second = row (A–S)

    Example:
      'ASBS' -> [(0, 18), (1, 18)]
      'JJJJ' -> [(9, 9), (9, 9)]
    """
    compact = compact.strip().upper()

    
    if len(compact) % 2 != 0:
        raise ValueError(f"Invalid coordinate length: {compact}")

    squares: List[Tuple[int, int]] = []

    # Process every 2-letter pair
    for i in range(0, len(compact), 2):
        token = compact[i:i + 2]

        # Validate that both letters are within A–S
        if not is_valid_sq(token):
            raise ValueError(f"Invalid square: {token}")

        col, row = token[0], token[1]
        x = LETTERS.index(col)  # Convert letter to 0-based index
        y = LETTERS.index(row)
        squares.append((x, y))

    return squares

def squares_to_compact(squares: List[Tuple[int, int]]) -> str:
    """Convert coordinates back to compact format, e.g. [(0,18),(1,18)] -> 'ASBS'."""

    return "".join(LETTERS[x] + LETTERS[y] for (x, y) in squares)
