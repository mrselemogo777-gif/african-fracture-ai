import streamlit as st
import time
from datetime import datetime
from models.model_manager import ModelManager
from utils.session_state import SessionManager
from pages import clinical_page, xray_page, ensemble_page, results_page, resources_page

st.set_page_config(page_title="African Fracture AI", page_icon="🩺", layout="wide")

SessionManager.init()
model_manager = ModelManager()

# Splash screen
if st.session_state.show_splash:
    with st.spinner("Loading African Fracture AI..."):
        time.sleep(2)
    st.session_state.show_splash = False
    st.rerun()

# Login
if not st.session_state.logged_in:
    st.markdown("""
    <div style="background: rgba(0,0,0,0.75); padding: 2rem; border-radius: 20px; text-align: center; max-width: 400px; margin: 100px auto;">
        <h1 style="color: white;">🩺 African Fracture AI</h1>
        <p style="color: #ccc;">ML-Assisted Fracture Triage for Rural Africa</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Enter as Guest", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.username = "Guest"
            st.rerun()
    st.stop()

# Header
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    try:
        st.image("assets/DOCTOR.jpeg", width=150)
    except:
        st.write("🩺")
with col2:
    st.title("African Fracture AI")
    st.write(f"Welcome, {st.session_state.username} | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
with col3:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

st.markdown("---")

# Sidebar
with st.sidebar:
    st.metric("Clinical Model", "84.1%")
    st.metric("X-ray Model", "68.6%")
    st.metric("Ensemble", "84.8%")
    st.markdown("---")
    st.markdown("### 18 African Countries")
    st.markdown("Tanzania • South Africa • Ghana • Zambia • Burkina Faso • Zimbabwe • Senegal • Kenya • Uganda • Mali • Egypt • Ethiopia • Ivory Coast • Nigeria • Botswana • Cameroon • Morocco • Rwanda")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Clinical", "X-ray", "Ensemble", "Results", "Resources"])

with tab1:
    clinical_page.show(model_manager)
with tab2:
    xray_page.show(model_manager)
with tab3:
    ensemble_page.show(model_manager)
with tab4:
    results_page.show()
with tab5:
    resources_page.show()

st.markdown("---")
st.markdown("🏥 African Fracture AI | 18 Countries | Clinical: 84.1% | X-ray: 68.6% | Ensemble: 84.8%")
