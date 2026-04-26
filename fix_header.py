import streamlit as st

# Read current app.py
with open('app.py', 'r') as f:
    content = f.read()

# Find the header section and replace it
old_header = '''col_left, col_mid, col_right = st.columns([1, 4, 1])

with col_mid:
    st.markdown('<h1 style="color: #1e3c72; margin-bottom: 0;">🦴 African Fracture AI</h1>', unsafe_allow_html=True)
    st.markdown(f"Welcome, **{st.session_state.username}** | {datetime.now().strftime('%Y-%m-%d %H:%M')}")'''

new_header = '''col_left, col_mid, col_right = st.columns([1, 3, 1])

with col_left:
    try:
        st.image("assets/DOCTOR.jpeg", width=150)
    except:
        st.markdown("🩺", fontsize=40)

with col_mid:
    st.markdown('<h1 style="color: #1e3c72; margin-bottom: 0;">🦴 African Fracture AI</h1>', unsafe_allow_html=True)
    st.markdown(f"Welcome, **{st.session_state.username}** | {datetime.now().strftime('%Y-%m-%d %H:%M')}")'''

if old_header in content:
    content = content.replace(old_header, new_header)
    with open('app.py', 'w') as f:
        f.write(content)
    print("✅ Header fixed - Doctor image added to left column")
else:
    print("⚠️ Pattern not found, manual edit needed")
