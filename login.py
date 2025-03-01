import streamlit as st
from  streamlit_option_menu import option_menu
from backend import database
import doctor
import nurse
               
                

    

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


if "page" not in st.session_state:
    st.session_state.page = "login"



def login():
    
    st.title(" login ")
    
   

    username = st.text_input("username")
    password = st.text_input("password" , type = "password")
    col1 , col2 , col3 = st.columns([1,2,3])
    with col2:  
        # Style the button using Markdown
        st.markdown(
            """
            <style>
            div.stButton > button {
                width: 300px;
                height: 70px;
                font-size: 20px;
                background-color: green;
                color: white;
                border-radius: 30px;
                border: none;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        login_button = st.button("login")  
    
    
    
    if login_button:
        if username and password:
            result = database.verify_user(username, password)
            if result == "Doctor":
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.page = "doctor"  # Redirect to Doctor page
                st.rerun()
            elif result == "Nurse":
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.page = "nurse"  # Redirect to Doctor page
                st.rerun()
            else:
                st.error(result) 
        else:
            st.error("Error please fill your username or password")


          
if st.session_state.page == "login":
    login()
elif st.session_state.page == "doctor" and st.session_state.logged_in:
    doctor.show()
elif st.session_state.page == "nurse" and st.session_state.logged_in:
    nurse.show()  
else:
    st.session_state.page = "login"
    st.rerun()


            #LOG OUT

def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.page == "login"
    st.rerun()    

if st.session_state.logged_in:
    st.sidebar.write(f"👤 Logged in as: **{st.session_state.username}**")
    if st.sidebar.button("log out"):
        logout()           

def show():
        st.write("this is the nurses page")        