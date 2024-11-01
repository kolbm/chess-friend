import streamlit as st
import chess
import chess.svg

# Set up the chess board
board = chess.Board()

# Function to display the chess board as HTML
def display_board():
    svg = chess.svg.board(board)  # Generate the board as an SVG
    st.write(f'<div>{svg}</div>', unsafe_allow_html=True)

# Extended list of chess openings
openings = {
    "Ruy Lopez": ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5"],
    "Italian Game": ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4"],
    "Sicilian Defense": ["e2e4", "c7c5"],
    "French Defense": ["e2e4", "e7e6"],
    "Caro-Kann Defense": ["e2e4", "c7c6"],
    "Pirc Defense": ["e2e4", "d7d6"],
    "Scandinavian Defense": ["e2e4", "d7d5"],
    "Alekhine's Defense": ["e2e4", "g8f6"],
    "Queen's Gambit": ["d2d4", "d7d5", "c2c4"],
    "King's Gambit": ["e2e4", "e7e5", "f2f4"],
    "English Opening": ["c2c4"],
    "Nimzo-Indian Defense": ["d2d4", "g8f6", "c2c4", "e7e6", "b1c3", "f8b4"],
    "King's Indian Defense": ["d2d4", "g8f6", "c2c4", "g7g6"],
    "Grünfeld Defense": ["d2d4", "g8f6", "c2c4", "g7g6", "b1c3", "d7d5"],
    "Dutch Defense": ["d2d4", "f7f5"],
    "Benoni Defense": ["d2d4", "c7c5"],
    "Catalan Opening": ["d2d4", "d7d5", "g2g3"],
    "London System": ["d2d4", "d7d5", "g1f3", "e7e6", "c2c3"],
    "Trompowsky Attack": ["d2d4", "g8f6", "g1f3"],
    "Vienna Game": ["e2e4", "e7e5", "g1f3", "d7d6"],
    "Scotch Game": ["e2e4", "e7e5", "g1f3", "d7d6", "d2d4"],
    "Four Knights Game": ["e2e4", "e7e5", "g1f3", "b8c6", "b1c3"],
}

# Function to identify the opening
def identify_opening():
    moves = [board.san(move) for move in board.move_stack]
    for opening_name, opening_moves in openings.items():
        if moves[:len(opening_moves)] == opening_moves:
            return opening_name
    return "Unknown Opening"

# Main Streamlit app
def main():
    st.title("Streamlit Chess Game")
    st.write("Play chess and see if you recognize the opening!")

    # Display current board
    display_board()

    # Show the current opening if recognizable
    opening_name = identify_opening()
    st.write(f"Opening: {opening_name}")

    # Input for moves
    move = st.text_input("Enter your move in algebraic notation (e.g., e2e4):").strip()

    if st.button("Make Move"):
        try:
            # Try to push move if it's valid
            board.push_san(move)
            display_board()  # Update board
        except ValueError:
            st.write("Invalid move! Try again.")

    # Check if game is over
    if board.is_checkmate():
        st.write("Checkmate!")
    elif board.is_stalemate():
        st.write("Stalemate!")
    elif board.is_insufficient_material():
        st.write("Draw due to insufficient material.")
    
    # Option for AI opponent
    if st.button("Play against AI"):
        ai_move = random.choice([move for move in board.legal_moves])
        board.push(ai_move)
        display_board()

if __name__ == "__main__":
    main()
