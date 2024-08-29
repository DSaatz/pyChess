import chess
from stockfish import Stockfish

# ASCII representation of chess pieces
PIECE_UNICODE = {
    'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
    'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙',
    '.': '·'
}

def print_ascii_board(board):
    board_str = str(board)
    print("\n    a b c d e f g h")
    print("  +-----------------+")

    rows = board_str.split('\n')
    for i, row in enumerate(rows):
        print(f"{8 - i} |", end=" ")
        for square in row:
            print(PIECE_UNICODE.get(square, square), end=" ")
        print(f"| {8 - i}")

    print("  +-----------------+")
    print("    a b c d e f g h\n")

def main():
    # Initialize the board and Stockfish engine
    board = chess.Board()
    stockfish = Stockfish(path="stockfish\stockfish-windows-x86-64-avx2.exe")

    print("Welcome to the CLI Chess Game!")
    print("You are playing as white. Enter your moves in UCI format (e.g., e2e4).")

    while not board.is_game_over():
        # Display the board with ASCII art
        print_ascii_board(board)

        # Get the player's move
        player_move = input("Your move: ")

        # Validate the move
        try:
            move = chess.Move.from_uci(player_move)
            if move in board.legal_moves:
                board.push(move)
            else:
                print("Invalid move. Please try again.")
                continue
        except:
            print("Invalid format. Please enter your move in UCI format (e.g., e2e4).")
            continue

        # Check if the game is over after the player's move
        if board.is_game_over():
            break

        # Set the position for Stockfish
        stockfish.set_fen_position(board.fen())

        # Get the best move from Stockfish
        engine_move = stockfish.get_best_move()

        # Make Stockfish's move
        board.push(chess.Move.from_uci(engine_move))
        print(f"Stockfish's move: {engine_move}")

    # Final board state
    print_ascii_board(board)
    
    # Game over message
    if board.is_checkmate():
        print("Checkmate! You lost.")
    elif board.is_stalemate():
        print("Stalemate!")
    elif board.is_insufficient_material():
        print("Draw due to insufficient material!")
    else:
        print("Game over!")

if __name__ == "__main__":
    main()
