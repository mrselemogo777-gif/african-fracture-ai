import streamlit as st
from utils.session_state import SessionManager

def show():
    st.markdown("### 📋 Assessment History")
    
    if st.session_state.history:
        for h in st.session_state.history[-10:]:
            st.caption(f"{h['time'].strftime('%H:%M:%S')} - {h['type']}: {h['result']}")
        
        if st.button("Clear History"):
            SessionManager.clear_history()
            st.rerun()
    else:
        st.info("No assessments yet")
