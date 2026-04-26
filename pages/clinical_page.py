import streamlit as st
import numpy as np
from utils.session_state import SessionManager

def show(model_manager):
    st.markdown("### 🩺 Clinical Assessment")
    st.caption("Random Forest Classifier | 84.1% Accuracy")
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age (years)", 0, 120, 45)
        hr = st.number_input("Heart Rate (bpm)", 40, 200, 75)
        bp_sys = st.number_input("Systolic BP (mmHg)", 80, 200, 120)
    with col2:
        bp_dia = st.number_input("Diastolic BP (mmHg)", 50, 120, 80)
        pain = st.slider("Pain Scale (0-10)", 0, 10, 3)
    
    if st.button("Predict", type="primary"):
        pred, prob = model_manager.predict_clinical(age, hr, bp_sys, bp_dia, pain)
        
        if pred == 1:
            st.error(f"🔴 COMPLEX FRACTURE - {prob:.1%} confidence")
            st.info("Action: Refer to hospital")
            result = "COMPLEX"
        else:
            st.success(f"🟢 SIMPLE FRACTURE - {(1-prob):.1%} confidence")
            st.info("Action: Treat locally")
            result = "SIMPLE"
        
        st.session_state.clinical_result = {"prediction": result, "confidence": prob}
        SessionManager.add_history("Clinical", result)
