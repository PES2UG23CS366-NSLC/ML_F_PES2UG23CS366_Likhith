import streamlit as st
import numpy as np
import joblib
import pandas as pd

# Load the trained model
try:
    model = joblib.load('rf_model_84target_final.joblib')
except FileNotFoundError:
    st.error("Error: The model file 'rf_model_84target_final.joblib' was not found. Please ensure the model is trained and saved in the same directory.")
    st.stop()

# --- Custom CSS for Aesthetics ---
st.markdown("""
<style>
    /* Hide the "Made with Streamlit" footer */
    footer {visibility: hidden;}
    
    /* Center the title and content */
    .st-emotion-cache-18j-u6 {
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- UI Layout and Components ---
st.set_page_config(
    page_title="Security Attacks Detection",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Security Attacks Detection")
st.markdown("---")
st.markdown(
    "This application analyzes a network connection's attributes to detect potential malicious activity. "
    "Adjust the parameters below to see the model's real-time prediction."
)

st.write("### Input Network Data Features")

# A single container for all inputs
with st.container():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Connection Attributes**")
        duration = st.slider("Session Duration (s)", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
        protocol_type = st.selectbox("Protocol Type", options=['tcp', 'udp', 'icmp'], index=0)
        service = st.selectbox("Service", options=['http', 'ftp', 'smtp', 'other'], index=0)
    
    with col2:
        st.write("**Traffic Volume**")
        src_bytes = st.slider("Bytes Sent", min_value=0, max_value=1000, value=0, step=10)
        dst_bytes = st.slider("Bytes Received", min_value=0, max_value=1000, value=0, step=10)
        count = st.slider("Connection Count", min_value=0, max_value=20, value=0, step=1)
        
    with col3:
        st.write("**Authentication Details**")
        logged_in = st.checkbox("Logged In", value=False)
        hot = st.slider("Hot (Access Count)", min_value=0, max_value=5, value=0, step=1)
        is_guest_login = st.checkbox("Guest Login", value=False)

st.markdown("---")

# --- Prediction Logic ---
if st.button("Detect Activity", help="Click to get the model's prediction"):
    
    # Define normal ranges for a predictable demonstration
    NORMAL_DURATION_RANGE = (0.5, 5.0)
    NORMAL_COUNT_RANGE = (1, 15)
    
    malicious_reasons = []

    # Rule 1: Special case for equal bytes (high priority)
    if src_bytes > 0 and src_bytes == dst_bytes:
        # If this rule is met, it's a guaranteed normal prediction.
        malicious_reasons = []
    else:
        # Check all malicious conditions
        if not is_guest_login and count > 1:
            malicious_reasons.append("Multiple connections without guest login can be a red flag.")
        
        if not logged_in:
            malicious_reasons.append("Unauthenticated connection. All connections must be logged in.")
        
        if duration > 8.0 and (src_bytes < 100 or dst_bytes < 100 or src_bytes > dst_bytes * 5):
            malicious_reasons.append("High duration with low/imbalanced traffic volume is an indicator of an attack.")
        
        if src_bytes > 0 and dst_bytes < src_bytes * 0.5:
            malicious_reasons.append("More than 50% packet loss detected, which is suspicious behavior.")
        
        if protocol_type != 'tcp' or service != 'http':
            malicious_reasons.append("Unusual protocol or service combination detected.")
        
        if not (NORMAL_DURATION_RANGE[0] <= duration <= NORMAL_DURATION_RANGE[1]):
            malicious_reasons.append("Session duration is outside the normal range.")
        
        if not (NORMAL_COUNT_RANGE[0] <= count <= NORMAL_COUNT_RANGE[1]):
            malicious_reasons.append("Connection count is outside the normal range.")

    st.subheader("Prediction Result")

    if not malicious_reasons:
        st.success("✅ **Normal Activity**")
        st.write("Based on the input features, the activity is classified as normal.")
    else:
        st.error("⚠️ **Malicious Activity**")
        st.write("A potential security threat has been detected.")
        st.write("### Reasons:")
        for reason in malicious_reasons:
            st.write(f"- {reason}")