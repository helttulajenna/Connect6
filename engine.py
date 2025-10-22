# --------------------------------------------------------
# engine.py
# Connect6 engine for the tournament
# Chooses reasonable moves: center first, then near existing stones
# --------------------------------------------------------

import time, random
from typing import List, Tuple
from board import Board, BLACK, WHITE, EMPTY
from protocol import squares_to_compact

class Engine:
    def __init__(self) -> None:
        # Default time limit: 3000 ms (3 seconds per move)
        self.time_ms = 3000
        self.side = None  

    def set_time_ms(self, ms: int) -> None:
        """Set the time per move (milliseconds)."""
        self.time_ms = max(100, ms)

    def set_side(self, side: int) -> None:
        """Set which color this engine plays (BLACK or WHITE)."""
        self.side = side

    
    # The core move-selection function
    
    def select_move(self, board: Board) -> List[Tuple[int, int]]:
        """Selects the next move. Black starts in the center; 
        later moves are placed near existing stones."""

       
        # Start measuring time (for future improvements)
        start_time = time.time()

        # First move: Black plays the center (J, J) 
        if board.num_moves == 0 and board.to_move == BLACK:
            return [(9, 9)]  # 0-based index for J (the 10th letter)

        # Collect all empty squares and those near existing stones 
        empty_squares = []
        nearby_squares = set()

        for y in range(19):
            for x in range(19):
                if board.get(x, y) != EMPTY:
                    # For every stone on the board, mark adjacent empty squares
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < 19 and 0 <= ny < 19:
                                if board.get(nx, ny) == EMPTY:
                                    nearby_squares.add((nx, ny))
                else:
                    empty_squares.append((x, y))

     
        candidates = list(nearby_squares) if nearby_squares else empty_squares

        def distance_from_center(move: Tuple[int, int]) -> int:
            x, y = move
            cx, cy = 9, 9  # center coordinates
            return (x - cx) ** 2 + (y - cy) ** 2

        # Sort by distance (closest to center first)
        candidates.sort(key=distance_from_center)

        # How many stones to place this turn 
        stones_needed = 2 if board.num_moves > 0 else 1

        # Pick first N candidate moves
        chosen_moves = candidates[:stones_needed]

        return chosen_moves

  
    def format_move_for_stdout(self, stones: List[Tuple[int, int]]) -> str:
        """Return move in text format (e.g. 'move JJJJ' or 'move ASBS')."""
        return "move " + squares_to_compact(stones)
