import streamlit as st
import chess
import chess.svg
import json

# Initialize a new chess board if not already in session state
if 'board' not in st.session_state:
    st.session_state.board = chess.Board()

# HTML and JavaScript for interactive chessboard
html_code = f"""
<div id="board" style="width: 400px"></div>
<button id="getPositionBtn">Get Position</button>
<p id="status"></p>
<script src="https://cdnjs.cloudflare.com/ajax/libs/chessboard-js/1.0.0/chessboard-1.0.0.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/chess.js/0.10.2/chess.min.js"></script>
<script>
    var board = Chessboard('board', {{
      draggable: true,
      position: '{st.session_state.board.fen()}',
      onDrop: onDrop
    }});

    var game = new Chess();

    function onDrop(source, target) {{
        var move = game.move({{
            from: source,
            to: target,
            promotion: 'q' // Promote to a queen for simplicity
        }});

        if (move === null) return 'snapback';
        
        // Send move to Streamlit backend
        fetch('/?move=' + JSON.stringify({{from: source, to: target}}))
          .then(response => response.json())
          .then(data => {{
              if (data.error) {{
                  alert(data.error);
              }} else {{
                  board.position(data.position);
                  document.getElementById("status").innerHTML = data.status;
              }}
          }});
    }}
</script>
"""

# Handle move submission and board update
def handle_move(move):
    from_square = move["from"]
    to_square = move["to"]
    uci_move = from_square + to_square
    try:
        st.session_state.board.push_uci(uci_move)
        return {"position": st.session_state.board.fen(), "status": "Move accepted"}
    except ValueError:
        return {"error": "Invalid move!", "position": st.session_state.board.fen(), "status": "Try again"}

# Check for move query parameters
if st.experimental_get_query_params():
    move_data = json.loads(st.experimental_get_query_params()["move"][0])
    result = handle_move(move_data)
    st.json(result)  # Return JSON response for the frontend

# Display the chessboard and instructions
st.markdown("### Interactive Chess Game")
st.markdown("Move the pieces by dragging and dropping them on the board!")
st.components.v1.html(html_code, height=500)
