import streamlit as st
import numpy as np
from PIL import Image
from tensorflow.keras.applications.efficientnet import preprocess_input
from utils.session_state import SessionManager

def show(model_manager):
    st.markdown("### 📷 X-ray Analysis")
    st.caption("EfficientNetB0 + Random Forest | 68.6% Accuracy")
    
    uploaded = st.file_uploader("Upload X-ray image", type=["jpg", "png", "jpeg"])
    
    if uploaded:
        image = Image.open(uploaded)
        st.image(image, width=250)
        
        if st.button("Analyze", type="primary"):
            with st.spinner("Analyzing..."):
                pred, prob = model_manager.predict_xray(image)
                
                if pred == 1:
                    st.error(f"🔴 COMPLEX FRACTURE - {prob:.1%} confidence")
                    result = "COMPLEX"
                else:
                    st.success(f"🟢 SIMPLE FRACTURE - {(1-prob):.1%} confidence")
                    result = "SIMPLE"
                
                st.session_state.xray_result = {"prediction": result, "confidence": prob}
                SessionManager.add_history("X-ray", result)
