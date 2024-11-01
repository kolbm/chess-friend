import streamlit as st
import chess
import chess.svg
import matplotlib.pyplot as plt
from PIL import Image
import io

# Initialize the chess board
if "board" not in st.session_state:
    st.session_state.board = chess.Board()

# Display the chess board using matplotlib and Pillow
def display_board():
    # Create a matplotlib figure
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.axis("off")

    # Generate SVG image and display it using Pillow
    svg_data = chess.svg.board(st.session_state.board).encode("utf-8")
    image = Image.open(io.BytesIO(svg_data))

    # Display the image in Streamlit
    st.image(image, use_column_width=True)

# Function to handle moves
def handle_move(move):
    try:
        st.session_state.board.push_san(move)
    except ValueError:
        st.warning("Invalid move. Please try again.")

# Main app
st.title("Interactive Chess with Streamlit")
st.write("Use standard algebraic notation (e.g., 'e2 e4') to move pieces.")

# Display the board
display_board()

# Input for moves
move = st.text_input("Enter your move in algebraic notation (e.g., e2 e4):")
if st.button("Make Move"):
    handle_move(move)
    st.experimental_rerun()  # Refresh board after move

# Check for game status
if st.session_state.board.is_checkmate():
    st.write("Checkmate! Game over.")
elif st.session_state.board.is_stalemate():
    st.write("Stalemate! Game over.")
elif st.session_state.board.is_insufficient_material():
    st.write("Draw due to insufficient material.")
