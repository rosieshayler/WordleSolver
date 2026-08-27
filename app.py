import streamlit as st
from solver_logic import load_words, filter_wordle_words
import time

# page set up
st.set_page_config(page_title="Wordle Solver", page_icon="🟩")
st.title("🟩🟨⬜️ Wordle Solver")
st.write("Enter your guess and the colour score to filter the remaining possible words.")

# session state management 
if 'possible_words' not in st.session_state:
    st.session_state.possible_words = load_words("wordlewords.txt")

# user interface
col1, col2 = st.columns(2)
with col1:
    guess = st.text_input("Word Guessed (5 letters)", max_chars=5).lower()
with col2:
    score = st.text_input("Score (0=Grey, 1=Yellow, 2=Green)", max_chars=5)

# action button
if st.button("Filter Words"):
    # validation (want to make better)
    if len(guess) != 5:
        st.error("Error: Guessed word must be exactly 5 letters.")
    elif len(score) != 5 or not all(char in "012" for char in score):
        st.error("Error: Score must be exactly 5 digits using only 0, 1, or 2.")
    else:
        # 1. Start the high-resolution timer
        start_time = time.perf_counter()
        
        # 2. Run your flawlessly optimized logic
        filtered_list = filter_wordle_words(st.session_state.possible_words, guess, score)
        
        # 3. Stop the timer
        end_time = time.perf_counter()
        
        # 4. Calculate the difference
        execution_time = end_time - start_time
        
        # Display the result on your web app
        st.success(f"Filtered {len(st.session_state.possible_words)} words in {execution_time:.5f} seconds!")
        
        # Update the session state
        st.session_state.possible_words = filtered_list

# output 
st.divider()
st.subheader(f"Possible words remaining: {len(st.session_state.possible_words)}")

with st.container(height=300):
    for word in st.session_state.possible_words:
        st.write(word)

st.divider()
if st.button("Reset Game"):
    # Reload the full dictionary to start over
    st.session_state.possible_words = load_words("wordlewords.txt")
    st.rerun()


