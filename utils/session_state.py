import streamlit as st
from datetime import datetime

class SessionManager:
    @staticmethod
    def init():
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        if 'username' not in st.session_state:
            st.session_state.username = ""
        if 'show_splash' not in st.session_state:
            st.session_state.show_splash = True
        if 'history' not in st.session_state:
            st.session_state.history = []
        if 'clinical_result' not in st.session_state:
            st.session_state.clinical_result = None
        if 'xray_result' not in st.session_state:
            st.session_state.xray_result = None
        if 'ensemble_result' not in st.session_state:
            st.session_state.ensemble_result = None
    
    @staticmethod
    def add_history(assessment_type, result):
        st.session_state.history.append({
            "type": assessment_type,
            "result": result,
            "time": datetime.now()
        })
    
    @staticmethod
    def clear_history():
        st.session_state.history = []
        st.session_state.clinical_result = None
        st.session_state.xray_result = None
        st.session_state.ensemble_result = None
