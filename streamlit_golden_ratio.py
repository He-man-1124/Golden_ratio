# Golden Ratio Calculator - Streamlit App
# Install required packages: pip install streamlit pillow opencv-python numpy

import streamlit as st
from PIL import Image, ImageDraw
import cv2
import numpy as np
from io import BytesIO
import math
To update, run: pip install --upgrade pip

# Set page configuration
st.set_page_config(
    page_title="Golden Ratio Calculator",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define golden ratio constant
GOLDEN_RATIO = (1 + math.sqrt(5)) / 2  # ≈ 1.618

# Custom CSS styling
st.markdown("""
    <style>
    .metric-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #21808d;
    }
    .score-box {
        background: linear-gradient(135deg, #21808d, #2da6b2);
        color: white;
        padding: 30px;
        border-radius: 10px;
        text-align: center;
        margin: 20px 0;
    }
    .score-value {
        font-size: 48px;
        font-weight: bold;
        margin: 10px 0;
    }
    .score-status {
        font-size: 16px;
        opacity: 0.9;
    }
    .title-main {
        text-align: center;
        color: #13343b;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #626c71;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# App Title
st.markdown("<h1 class='title-main'>🌀 Golden Ratio Calculator</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Measure the divine proportion (φ ≈ 1.618) in your images</p>", unsafe_allow_html=True)

# Initialize session state for image
if 'image' not in st.session_state:
    st.session_state.image = None
if 'image_with_selection' not in st.session_state:
    st.session_state.image_with_selection = None
if 'measurements' not in st.session_state:
    st.session_state.measurements = None

# Sidebar for image upload
st.sidebar.header("📸 Image Source")
image_source = st.sidebar.radio("Choose image source:", ["Upload Image", "Use Camera"])

if image_source == "Upload Image":
    uploaded_file = st.sidebar.file_uploader("Choose an image file", type=["jpg", "jpeg", "png", "bmp", "gif"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.session_state.image = image
else:
    camera_image = st.sidebar.camera_input("Take a photo")
    if camera_image is not None:
        image = Image.open(camera_image)
        st.session_state.image = image

# Helper function to calculate score
def calculate_score(ratio):
    """Calculate golden ratio score (0-100)"""
    difference = abs(ratio - GOLDEN_RATIO)
    k = 3  # Decay constant
    return round(100 * math.exp(-k * difference))

# Helper function to get status message and color
def get_status(difference):
    """Get status message and color based on difference"""
    if difference < 0.05:
        status = "✨ Excellent! Very close to φ"
        color = "#21808d"
    elif difference < 0.15:
        status = "👍 Good! Moderately close to φ"
        color = "#32b8c6"
    elif difference < 0.3:
        status = "📐 Fair approximation"
        color = "#a84b2f"
    else:
        status = "📏 Not close to φ"
        color = "#c0152f"
    return status, color

# Main app logic
if st.session_state.image is not None:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📷 Image Preview")
        
        # Convert PIL to numpy for display
        img_np = np.array(st.session_state.image)
        
        # Create interactive area for selection
        st.write("**Instructions:** Click and drag on the image to select an area to measure the golden ratio.")
        
        # Display image with streamlit
        st.image(st.session_state.image, use_column_width=True)
        
        # Input fields for manual selection
        st.write("---")
        st.write("**Manual Selection (in pixels):**")
        col_a, col_b, col_c, col_d = st.columns(4)
        
        with col_a:
            x_start = st.number_input("X Start", value=0, min_value=0)
        with col_b:
            y_start = st.number_input("Y Start", value=0, min_value=0)
        with col_c:
            x_end = st.number_input("X End", value=100, min_value=0)
        with col_d:
            y_end = st.number_input("Y End", value=100, min_value=0)
        
        # Calculate button
        if st.button("📊 Calculate Golden Ratio", type="primary"):
            width = abs(x_end - x_start)
            height = abs(y_end - y_start)
            
            if width < 10 or height < 10:
                st.error("❌ Selection too small. Please draw a larger selection (minimum 10 pixels).")
            else:
                long_side = max(width, height)
                short_side = min(width, height)
                ratio = long_side / short_side
                difference = abs(ratio - GOLDEN_RATIO)
                score = calculate_score(ratio)
                status, color = get_status(difference)
                
                # Store measurements in session state
                st.session_state.measurements = {
                    'ratio': ratio,
                    'width': width,
                    'height': height,
                    'long_side': long_side,
                    'short_side': short_side,
                    'difference': difference,
                    'score': score,
                    'status': status,
                    'color': color,
                    'x_start': x_start,
                    'y_start': y_start,
                    'x_end': x_end,
                    'y_end': y_end
                }
                
                st.success("✅ Calculation complete! See results on the right.")
    
    with col2:
        st.subheader("📈 Measurements")
        
        if st.session_state.measurements:
            m = st.session_state.measurements
            
            # Score display with custom HTML
            st.markdown(f"""
                <div class='score-box'>
                    <div class='score-label'>Golden Ratio Score</div>
                    <div class='score-value'>{m['score']}</div>
                    <div class='score-status'>{m['status']}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Metrics
            st.markdown(f"""
                <div class='metric-box'>
                    <strong>Measured Ratio:</strong><br>
                    <span style='font-size: 24px; font-weight: bold; color: #21808d;'>{m['ratio']:.4f}</span>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class='metric-box'>
                    <strong>Dimensions:</strong><br>
                    <span style='font-size: 20px; font-weight: bold;'>{int(m['long_side'])} × {int(m['short_side'])} px</span>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class='metric-box'>
                    <strong>Difference from φ:</strong><br>
                    <span style='font-size: 24px; font-weight: bold; color: #a84b2f;'>{m['difference']:.4f}</span>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class='metric-box'>
                    <strong>φ (Golden Ratio):</strong><br>
                    <span style='font-size: 20px;'>{GOLDEN_RATIO:.4f}</span>
                </div>
            """, unsafe_allow_html=True)
            
            # Download results button
            results_text = f"""
Golden Ratio Analysis Results
=============================

Measured Ratio: {m['ratio']:.4f}
Golden Ratio (φ): {GOLDEN_RATIO:.4f}
Difference: {m['difference']:.4f}

Dimensions: {int(m['long_side'])} × {int(m['short_side'])} pixels
Selection: ({int(m['x_start'])}, {int(m['y_start'])}) to ({int(m['x_end'])}, {int(m['y_end'])})

Score: {m['score']}/100
Status: {m['status']}
"""
            st.download_button(
                label="⬇️ Download Results",
                data=results_text,
                file_name="golden_ratio_results.txt",
                mime="text/plain"
            )
        else:
            st.info("👈 Select an area and click 'Calculate Golden Ratio' to see measurements.")
    
    # Reset button
    if st.button("🔄 Reset", use_container_width=True):
        st.session_state.image = None
        st.session_state.measurements = None
        st.rerun()

else:
    st.info("👈 Upload an image or take a photo from the sidebar to get started!")

# Information section
with st.expander("ℹ️ About Golden Ratio"):
    st.write("""
    The **Golden Ratio** (φ ≈ 1.618) is a mathematical ratio found frequently in nature and art.
    
    **Formula:** φ = (1 + √5) / 2 ≈ 1.618033988749...
    
    **Characteristics:**
    - When a rectangle has a length-to-width ratio of φ, it's considered aesthetically pleasing
    - Found in architecture, design, nature (flower petals, seashells, spiral galaxies)
    - Used extensively in graphic design, web design, and photography
    
    **How to use this calculator:**
    1. Upload an image or take a photo
    2. Specify the coordinates of the area you want to measure
    3. Click "Calculate Golden Ratio" to see how close your selection is to φ
    4. Score ranges from 0-100, where 100 is perfect alignment with φ
    """)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #626c71; font-size: 12px;'>Golden Ratio Calculator • Built with Streamlit</p>", unsafe_allow_html=True)
