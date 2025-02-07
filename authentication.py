# utils/authentication.py
import streamlit as st

def login(username: str, password: str) -> bool:
    """
    Validates user credentials. If valid, sets session state 'logged_in' to True.
    """
    if username == "admin" and password == "admin":
        st.session_state["logged_in"] = True
        return True
    else:
        st.session_state["logged_in"] = False
        return False

def logout():
    """
    Logs out the current user by resetting session state.
    """
    st.session_state["logged_in"] = False
