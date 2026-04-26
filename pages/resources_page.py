import streamlit as st

def show():
    st.markdown("### 📚 Clinical Resources")
    
    with st.expander("For Clinicians"):
        st.markdown("""
        - WHO Fracture Management Guidelines
        - AAOS Clinical Practice Guidelines
        - African Federation of Emergency Medicine
        """)
    
    with st.expander("For Patients"):
        st.markdown("""
        - Understanding Bone Fractures
        - Fracture Recovery Timeline
        """)
    
    with st.expander("About This AI"):
        st.markdown("""
        **Model Performance:**
        - Clinical Model: 84.1% accuracy
        - X-ray Model: 68.6% accuracy
        - Ensemble: 84.8% accuracy
        
        **Training Data:**
        - 1,129 patients from 18 African countries
        - 10 fracture types (5 Simple, 5 Complex)
        """)
    
    with st.expander("Send Feedback"):
        rating = st.select_slider("Rate this tool:", options=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"])
        feedback = st.text_area("Your feedback:")
        if st.button("Submit"):
            st.success("Thank you for your feedback!")
