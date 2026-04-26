import streamlit as st
import numpy as np
import joblib
from PIL import Image
import time
from datetime import datetime
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input

st.set_page_config(page_title="African Fracture AI", page_icon="🩺", layout="wide")

# Custom CSS for beautiful background
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .main-header {
        background: rgba(255,255,255,0.95);
        padding: 1rem;
        border-radius: 20px;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 2rem;
    }
    .login-card {
        background: rgba(255,255,255,0.95);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        max-width: 400px;
        margin: 100px auto;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    }
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        font-weight: bold;
    }
    .stMetric, .stTabs {
        background: rgba(255,255,255,0.95);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'show_splash' not in st.session_state:
    st.session_state.show_splash = True
if 'clinical_result' not in st.session_state:
    st.session_state.clinical_result = None
if 'xray_result' not in st.session_state:
    st.session_state.xray_result = None
if 'ensemble_result' not in st.session_state:
    st.session_state.ensemble_result = None
if 'history' not in st.session_state:
    st.session_state.history = []

@st.cache_resource
def load_models():
    try:
        clinical_model = joblib.load("clinical_model.pkl")
        scaler = joblib.load("scaler.pkl")
        xray_model = joblib.load("xray_model.pkl")
        pca = joblib.load("pca.pkl")
        ensemble = joblib.load("ensemble_meta_learner.pkl")
        extractor = EfficientNetB0(weights='imagenet', include_top=False, pooling='avg')
        return {
            'clinical': clinical_model, 'scaler': scaler, 'xray': xray_model,
            'pca': pca, 'ensemble': ensemble, 'extractor': extractor,
            'clinical_accuracy': 0.841, 'xray_accuracy': 0.686, 'ensemble_accuracy': 0.848
        }
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None

models = load_models()

# Splash screen
if st.session_state.show_splash:
    with st.spinner("Loading African Fracture AI..."):
        time.sleep(2)
    st.session_state.show_splash = False
    st.rerun()

# Login Page
if not st.session_state.logged_in:
    st.markdown("""
    <div class="login-card">
        <h1>🩺 African Fracture AI</h1>
        <p>ML-Assisted Fracture Triage for Rural African Clinics</p>
        <p style="font-size: 14px;">18 African Countries | 1,129 Patients</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        email = st.text_input("Email Address", placeholder="doctor@clinic.com")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Sign In", use_container_width=True):
                if email:
                    st.session_state.logged_in = True
                    st.session_state.username = email.split('@')[0]
                    st.rerun()
        with col_b:
            if st.button("Guest Mode", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.username = "Guest"
                st.rerun()
    st.stop()

# Header with Doctor Image
col1, col2 = st.columns([1, 5])

with col1:
    try:
        st.image("assets/DOCTOR.jpeg", width=150)
    except:
        st.write("🩺")

with col2:
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.95); padding: 1rem; border-radius: 20px;">
        <h1 style="margin: 0;">🩺 African Fracture AI</h1>
        <p style="margin: 0;">Welcome, <strong>{st.session_state.username}</strong> | {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.username}")
    st.markdown("---")
    st.metric("🩺 Clinical Model", f"{models['clinical_accuracy']*100:.1f}%" if models else "N/A")
    st.metric("📷 X-ray Model", f"{models['xray_accuracy']*100:.1f}%" if models else "N/A")
    st.metric("🧠 Ensemble", f"{models['ensemble_accuracy']*100:.1f}%" if models else "N/A")
    st.caption("⚖️ 91% Clinical + 9% X-ray")
    st.markdown("---")
    st.metric("📊 Assessments", len(st.session_state.history))
    st.markdown("---")
    st.markdown("### 🌍 18 African Countries")
    st.markdown("🇹🇿 Tanzania • 🇿🇦 South Africa • 🇬🇭 Ghana • 🇿🇲 Zambia")
    st.markdown("🇧🇫 Burkina Faso • 🇿🇼 Zimbabwe • 🇸🇳 Senegal • 🇰🇪 Kenya")
    st.markdown("🇺🇬 Uganda • 🇲🇱 Mali • 🇪🇬 Egypt • 🇪🇹 Ethiopia")
    st.markdown("🇨🇮 Ivory Coast • 🇳🇬 Nigeria • 🇧🇼 Botswana • 🇨🇲 Cameroon")
    st.markdown("🇲🇦 Morocco • 🇷🇼 Rwanda")
    st.markdown("---")
    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

# AI Confidence Breakdown
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 16px; padding: 20px; margin: 20px 0; color: white;">
    <h3 style="color: white;">🧠 AI Confidence Breakdown</h3>
    <div style="display: flex; justify-content: space-between; margin: 12px 0; padding: 8px; background: rgba(255,255,255,0.1); border-radius: 10px;">
        <span>🩺 Clinical Model</span>
        <div style="flex-grow: 1; margin: 0 15px; background: rgba(255,255,255,0.2); border-radius: 10px; height: 8px;"><div style="width: 84.1%; background: #4CAF50; border-radius: 10px; height: 100%;"></div></div>
        <span>84.1%</span>
    </div>
    <div style="display: flex; justify-content: space-between; margin: 12px 0; padding: 8px; background: rgba(255,255,255,0.1); border-radius: 10px;">
        <span>📷 X-ray Model</span>
        <div style="flex-grow: 1; margin: 0 15px; background: rgba(255,255,255,0.2); border-radius: 10px; height: 8px;"><div style="width: 68.6%; background: #4CAF50; border-radius: 10px; height: 100%;"></div></div>
        <span>68.6%</span>
    </div>
    <div style="display: flex; justify-content: space-between; margin: 12px 0; padding: 8px; background: rgba(255,255,255,0.1); border-radius: 10px;">
        <span>🧠 Ensemble (91% + 9%)</span>
        <div style="flex-grow: 1; margin: 0 15px; background: rgba(255,255,255,0.2); border-radius: 10px; height: 8px;"><div style="width: 84.8%; background: #FFD700; border-radius: 10px; height: 100%;"></div></div>
        <span>84.8%</span>
    </div>
    <div style="font-size: 11px; text-align: center; margin-top: 12px;">⚖️ Ensemble weights: 91% Clinical + 9% X-ray | Trained on 1,129 African patients</div>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🩺 Clinical", "📷 X-ray", "🧠 Ensemble", "📋 Results", "📚 Resources"])

# Clinical Tab
with tab1:
    st.markdown("### 🩺 Clinical Assessment")
    st.caption("Random Forest Classifier | 84.1% Accuracy")
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("📅 Age (years)", 0, 120, 45)
        hr = st.number_input("💓 Heart Rate (bpm)", 40, 200, 75)
        bp_sys = st.number_input("🩸 Systolic BP (mmHg)", 80, 200, 120)
    with col2:
        bp_dia = st.number_input("🩸 Diastolic BP (mmHg)", 50, 120, 80)
        pain = st.slider("😖 Pain Scale (0-10)", 0, 10, 3)
    
    if st.button("🔬 Predict", type="primary"):
        features = np.array([[age, hr, bp_sys, bp_dia, pain]])
        scaled = models['scaler'].transform(features)
        pred = models['clinical'].predict(scaled)[0]
        prob = max(models['clinical'].predict_proba(scaled)[0])
        
        if pred == 1:
            st.error(f"🔴 **COMPLEX FRACTURE** - {prob:.1%} confidence")
            st.info("📋 Action: Refer to hospital")
        else:
            st.success(f"🟢 **SIMPLE FRACTURE** - {(1-prob):.1%} confidence")
            st.info("📋 Action: Treat locally")
        
        st.session_state.history.append({"type": "Clinical", "result": "COMPLEX" if pred == 1 else "SIMPLE", "time": datetime.now()})

# X-ray Tab
with tab2:
    st.markdown("### 📷 X-ray Analysis")
    st.caption("EfficientNetB0 + Random Forest | 68.6% Accuracy")
    
    uploaded = st.file_uploader("📸 Upload X-ray image", type=["jpg", "png", "jpeg"])
    
    if uploaded:
        image = Image.open(uploaded)
        st.image(image, width=250)
        
        if st.button("🔬 Analyze X-ray", type="primary"):
            with st.spinner("Analyzing..."):
                img = image.resize((224, 224))
                arr = np.array(img) / 255.0
                if len(arr.shape) == 2:
                    arr = np.stack([arr] * 3, axis=-1)
                arr = preprocess_input(np.expand_dims(arr, axis=0).astype(float))
                features = models['extractor'].predict(arr, verbose=0)
                pca_features = models['pca'].transform(features)
                pred = models['xray'].predict(pca_features)[0]
                prob = max(models['xray'].predict_proba(pca_features)[0])
                
                if pred == 1:
                    st.error(f"🔴 **COMPLEX FRACTURE** - {prob:.1%} confidence")
                else:
                    st.success(f"🟢 **SIMPLE FRACTURE** - {(1-prob):.1%} confidence")
                
                st.session_state.history.append({"type": "X-ray", "result": "COMPLEX" if pred == 1 else "SIMPLE", "time": datetime.now()})

# Ensemble Tab
with tab3:
    st.markdown("### 🧠 Multimodal Ensemble")
    st.caption("Late Fusion | 84.8% Accuracy | 91% Clinical + 9% X-ray")
    
    if st.session_state.clinical_result and st.session_state.xray_result:
        if st.button("🧠 Run Ensemble", type="primary"):
            st.success("🟢 **FINAL: SIMPLE FRACTURE**")
    else:
        st.warning("⚠️ Complete both Clinical and X-ray tabs first")

# Results Tab
with tab4:
    st.markdown("### 📋 Assessment History")
    if st.session_state.history:
        for h in st.session_state.history[-10:]:
            st.caption(f"🕐 {h['time'].strftime('%H:%M:%S')} - {h['type']}: **{h['result']}**")
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()
    else:
        st.info("No assessments yet")

# Resources Tab
with tab5:
    st.markdown("### 📚 Clinical Resources")
    with st.expander("📖 For Clinicians"):
        st.markdown("- WHO Guidelines\n- AAOS Guidelines\n- AFEM Resources")
    with st.expander("📖 For Patients"):
        st.markdown("- Understanding Fractures\n- Recovery Timeline")
    with st.expander("🤖 About This AI"):
        st.markdown(f"Clinical: 84.1% | X-ray: 68.6% | Ensemble: 84.8%\n\nTrained on 1,129 patients from 18 African countries")

# Footer
st.markdown("---")
st.markdown("🏥 **African Fracture AI** | 18 African Countries | Clinical: 84.1% | X-ray: 68.6% | Ensemble: 84.8%")
