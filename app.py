import streamlit as st
import chess
import chess.svg
import cairosvg
from PIL import Image
import io

# Initialize the chess board
if "board" not in st.session_state:
    st.session_state.board = chess.Board()

# Display the board as a PNG in Streamlit
def display_board():
    svg_data = chess.svg.board(st.session_state.board)
    png_data = cairosvg.svg2png(bytestring=svg_data.encode("utf-8"))
    image = Image.open(io.BytesIO(png_data))
    st.image(image)

# Make a move by clicking squares
st.title("Interactive Chess with Streamlit")
st.write("Click on a piece to select it, then click on a target square to move.")

# Keep track of selected square
if "selected_square" not in st.session_state:
    st.session_state.selected_square = None

# Display the board
display_board()

# Capture the clicked square
for row in range(8, 0, -1):
    cols = []
    for col in range(8):
        square = chess.square(col, row - 1)
        square_name = chess.square_name(square)
        if st.button(square_name, key=square_name):
            # If a piece is already selected, try to move it
            if st.session_state.selected_square:
                move = chess.Move.from_uci(st.session_state.selected_square + square_name)
                if move in st.session_state.board.legal_moves:
                    st.session_state.board.push(move)
                    st.session_state.selected_square = None
                    st.experimental_rerun()
                else:
                    st.warning("Illegal move!")
                    st.session_state.selected_square = None
            else:
                st.session_state.selected_square = square_name
    st.write(" ")  # Line break after each row

# Display the game status
if st.session_state.board.is_checkmate():
    st.write("Checkmate!")
elif st.session_state.board.is_stalemate():
    st.write("Stalemate!")
elif st.session_state.board.is_insufficient_material():
    st.write("Draw due to insufficient material.")
