import streamlit as st
import chess
from streamlit_chessboard import st_chessboard

# Initialize chess board
if "board" not in st.session_state:
    st.session_state.board = chess.Board()

# Function to handle moves
def handle_move(from_square, to_square):
    move = chess.Move.from_uci(from_square + to_square)
    if move in st.session_state.board.legal_moves:
        st.session_state.board.push(move)
        return True
    else:
        st.warning("Illegal move attempted.")
        return False

# Display the chessboard and capture moves
st.title("Interactive Chessboard with Streamlit")
st.write("Drag and drop pieces to make your move!")

# Display the board and get user's move
move = st_chessboard("chessboard", initial_fen=st.session_state.board.fen(), theme="blue2")
if move:
    from_square, to_square = move["from"], move["to"]
    if handle_move(from_square, to_square):
        st.experimental_rerun()

# Show the FEN notation for reference
st.write(f"Current FEN: {st.session_state.board.fen()}")

# Check for game-ending conditions
if st.session_state.board.is_checkmate():
    st.write("Checkmate! Game over.")
elif st.session_state.board.is_stalemate():
    st.write("Stalemate! Game over.")
elif st.session_state.board.is_insufficient_material():
    st.write("Draw due to insufficient material.")
