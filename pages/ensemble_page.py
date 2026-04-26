import streamlit as st
import numpy as np
from utils.session_state import SessionManager

def show(model_manager):
    st.markdown("### 🧠 Multimodal Ensemble")
    st.caption("Late Fusion | 84.8% Accuracy | 91% Clinical + 9% X-ray")
    
    if st.session_state.clinical_result and st.session_state.xray_result:
        clinical = st.session_state.clinical_result
        xray = st.session_state.xray_result
        
        st.info(f"Clinical: {clinical['prediction']} ({clinical['confidence']:.1%} confidence)")
        st.info(f"X-ray: {xray['prediction']} ({xray['confidence']:.1%} confidence)")
        
        if st.button("Run Ensemble", type="primary"):
            clinical_prob = clinical['confidence'] if clinical['prediction'] == "COMPLEX" else 1 - clinical['confidence']
            xray_prob = xray['confidence'] if xray['prediction'] == "COMPLEX" else 1 - xray['confidence']
            ensemble_input = np.array([[clinical_prob, xray_prob]])
            ensemble_pred = model_manager.models['ensemble'].predict(ensemble_input)[0]
            ensemble_prob = max(model_manager.models['ensemble'].predict_proba(ensemble_input)[0])
            
            if ensemble_pred == 1:
                st.error(f"🔴 FINAL: COMPLEX FRACTURE - {ensemble_prob:.1%} confidence")
                result = "COMPLEX"
            else:
                st.success(f"🟢 FINAL: SIMPLE FRACTURE - {ensemble_prob:.1%} confidence")
                result = "SIMPLE"
            
            SessionManager.add_history("Ensemble", result)
    else:
        st.warning("Complete both Clinical and X-ray tabs first")
