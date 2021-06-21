import streamlit as st
import SessionState
import random
import operator



def random_problem():
    st.markdown("<h1 style = 'text-align:center; color:green;'>Simple Math</h1>", unsafe_allow_html=True)
    
    session_state = SessionState.get(name = "", button_start = False)
    
    session_state.name = st.text_input("Enter Your Name")
    
    button_start = st.button('Start Game')
    
    if button_start:
        session_state.button_start = True
        
    if session_state.button_start:
        st.write("Welcome ", session_state.name)
        operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            }
        num1 = random.randint(1,10)
        
        num2 = random.randint(1,10)
        
        operation = random.choice(list(operators.keys()))
        answer = operators.get(operation)(num1,num2)
        session_state.qus = str(num1)+' '+str(operation)+' '+str(num2)
        st.write('What is: ', session_state.qus)
        #st.write('What is:', num1, operation, num2,'?')
        session_state.ans = st.text_input('Answer: ')
        
        button_submit = st.button('Answer')   
        if button_submit:
            ans = int(session_state.ans)
            if answer == ans:
                st.write('Correct')
            else:
                st.write('Incorrect')
    
random_problem()
