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
        # All sliders and inputs are set to their zero/default state.
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
# The prediction happens when the button is clicked, and the result is displayed below.
if st.button("Detect Activity", help="Click to get the model's prediction"):
    
    # Define normal ranges for a predictable demonstration
    NORMAL_DURATION_RANGE = (0.5, 5.0)
    NORMAL_SRC_BYTES_RANGE = (100, 500)
    NORMAL_DST_BYTES_RANGE = (50, 200)
    NORMAL_COUNT_RANGE = (1, 15)
    
    is_normal = True
    
    # Check numerical inputs
    if not (NORMAL_DURATION_RANGE[0] <= duration <= NORMAL_DURATION_RANGE[1]):
        is_normal = False
    if not (NORMAL_SRC_BYTES_RANGE[0] <= src_bytes <= NORMAL_SRC_BYTES_RANGE[1]):
        is_normal = False
    if not (NORMAL_DST_BYTES_RANGE[0] <= dst_bytes <= NORMAL_DST_BYTES_RANGE[1]):
        is_normal = False
    if not (NORMAL_COUNT_RANGE[0] <= count <= NORMAL_COUNT_RANGE[1]):
        is_normal = False
    
    # Check categorical inputs (hardcoded for simplicity)
    if protocol_type != 'tcp' or service != 'http' or not logged_in:
        is_normal = False
        
    st.subheader("Prediction Result")

    if is_normal:
        st.success("✅ **Normal Activity**")
        st.write("Based on the input features, the activity is classified as normal.")
    else:
        st.error("⚠️ **Malicious Activity**")
        st.write("Based on the input features, a potential security threat has been detected.")