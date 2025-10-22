# --------------------------------------------------------
# Connect6 Game Engine
# Creator: Jenna Helttula
# --------------------------------------------------------

from __future__ import annotations
import sys
from protocol import parse_squares
from board import Board, BLACK, WHITE
from engine import Engine

# --------------------------------------------------------
# HELP_TEXT: This text is printed when you type "help"
# --------------------------------------------------------
HELP_TEXT = """\
Commands:
  name          -> print engine name
  print         -> show the current board
  exit | quit   -> terminate the program
  black XXXX    -> place black stones (first move: one stone, e.g. 'JJJJ')
  white XXXX    -> place white stones
  next          -> engine plays next move
  move XXXX     -> opponent moved; engine responds
  new black     -> start a new game as black
  new white     -> start a new game as white
  depth d       -> set time limit per move (milliseconds)
  vcf | unvcf   -> ignored (compatibility)
  help          -> show this help message
"""

def eprint(msg: str) -> None:
    print(msg, file=sys.stderr)

# --------------------------------------------------------
# MAIN FUNCTION
# This runs the loop that reads commands from standard input
# and sends responses to standard output.
# --------------------------------------------------------
def main() -> None:
    
    board = Board()
    engine = Engine()

    def place_move(color: int, move_str: str):
        # Convert compact notation (e.g., "ASBS") into list of coordinates
        stones = parse_squares(move_str.upper())

        # Special case: first black move might be duplicated, e.g. "JJJJ"
        if color == BLACK and board.num_moves == 0 and len(stones) == 2 and stones[0] == stones[1]:
            stones = [stones[0]]

        # First move (black) -> 1 stone, otherwise 2 stones
        expected = 1 if (color == BLACK and board.num_moves == 0) else 2
        if len(stones) != expected:
            raise ValueError(f"Expected {expected} stones, got {len(stones)}")

        if not board.place(stones, color):
            raise ValueError("Illegal move: occupied or invalid position")
        
        board.to_move = BLACK if color == WHITE else WHITE


    print(flush=True)  # Ensure the first output is clean

    for line in sys.stdin:
        cmd = line.strip()
        if not cmd:
            continue

        parts = cmd.split(maxsplit=1)
        keyword = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        try:

            if keyword == "name":
               
                print("Connect6 Student Engine", flush=True)

            elif keyword == "print":
                
                print(board.print_ascii(), flush=True)

            elif keyword in ("exit", "quit"):
                
                break

            # --- GAMEPLAY COMMANDS ---

            elif keyword == "black":
                
                place_move(BLACK, arg)

            elif keyword == "white":
                
                place_move(WHITE, arg)

            elif keyword == "move":
                
                place_move(board.to_move, arg)
                mv = engine.select_move(board)
                if mv:
                    
                    board.place(mv, board.to_move)
                    board.to_move = BLACK if board.to_move == WHITE else WHITE
                    print(engine.format_move_for_stdout(mv), flush=True)

            elif keyword == "next":
                
                mv = engine.select_move(board)
                if mv:
                    board.place(mv, board.to_move)
                    board.to_move = BLACK if board.to_move == WHITE else WHITE
                    print(engine.format_move_for_stdout(mv), flush=True)

            elif keyword == "new":
                
                board = Board()
                if arg.lower() == "black":
                    engine.set_side(BLACK)
                elif arg.lower() == "white":
                    engine.set_side(WHITE)
                    board.to_move = WHITE
                else:
                    raise ValueError("Use: new black | new white")

            elif keyword == "depth":
                
                engine.set_time_ms(int(arg))

            elif keyword in ("vcf", "unvcf"):
                
                print("", flush=True)

            elif keyword == "help":
                
                print(HELP_TEXT, flush=True)

            else:
                # Unknown command
                print(HELP_TEXT, flush=True)

        except Exception as ex:
            # Any error goes to stderr (not stdout)
            eprint(f"[error] {ex} for command: {cmd}")


if __name__ == "__main__":
    main()
