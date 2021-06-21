import streamlit as st
import SessionState
import random
import operator
import time



def random_problem():
    st.markdown("<h1 style = 'text-align:center; color:green;'>Simple Math</h1>", unsafe_allow_html=True)
    
    session_state = SessionState.get(name = "", button_start = False)
    
    session_state.name = st.text_input("Enter Your Name")
    
    button_start = st.button('Start Game')
    if button_start:
        session_state.button_start = True
    if session_state.button_start:
        st.write("Welcome ", session_state.name)
        session_state.operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            }
        session_state.num1 = random.randint(1,10)
        
        session_state.num2 = random.randint(1,10)
        
        session_state.operation = random.choice(list(session_state.operators.keys()))
        session_state.answer = session_state.operators.get(session_state.operation)(session_state.num1,session_state.num2)
        st.write('What is:', session_state.num1, session_state.operation, session_state.num2,'?')
        session_state.ans = st.text_input('Answer: ')
        session_state.button_submit = st.button('Answer')
        if session_state.button_submit:
            if session_state.answer == session_state.ans:
                st.write('Correct')
            else:
                st.write('Incorrect')
    
random_problem()
