# Golden Ratio Calculator - Streamlit App (Simple & Reliable)
# Uses HTML5 Canvas via JavaScript - Works perfectly with Streamlit!

import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import math
import json

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
    .instruction-box {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 15px;
        margin: 20px 0;
        border-radius: 5px;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# App Title
st.markdown("<h1 class='title-main'>🌀 Golden Ratio Calculator</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Measure the divine proportion (φ ≈ 1.618) in your images</p>", unsafe_allow_html=True)

# Initialize session state
if 'image' not in st.session_state:
    st.session_state.image = None
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
    k = 3
    return round(100 * math.exp(-k * difference))

# Helper function to get status
def get_status(difference):
    """Get status message and color"""
    if difference < 0.05:
        return "✨ Excellent! Very close to φ", "#21808d"
    elif difference < 0.15:
        return "👍 Good! Moderately close to φ", "#32b8c6"
    elif difference < 0.3:
        return "📐 Fair approximation", "#a84b2f"
    else:
        return "📏 Not close to φ", "#c0152f"

# Main app logic
if st.session_state.image is not None:
    col1, col2 = st.columns([2.5, 1])
    
    with col1:
        st.subheader("📷 Tap & Drag to Select Area")
        
        st.markdown("""
            <div class='instruction-box'>
            <strong>🎯 How to Use:</strong><br>
            1. Use the input fields below to specify coordinates<br>
            2. OR use the simple slider approach<br>
            3. Set X and Y start/end positions<br>
            4. Click "📊 Calculate Golden Ratio" to measure
            </div>
        """, unsafe_allow_html=True)
        
        # Get image dimensions
        img_width, img_height = st.session_state.image.size
        
        # Display image
        st.image(st.session_state.image, use_column_width=True, caption=f"Image: {img_width}×{img_height} px")
        
        st.write("---")
        st.write("**📊 Select Area Using Coordinates:**")
        
        # Use 4 columns for easier input
        col_a, col_b, col_c, col_d = st.columns(4)
        
        with col_a:
            x_start = st.number_input("X Start", value=0, min_value=0, max_value=img_width, step=10)
        
        with col_b:
            y_start = st.number_input("Y Start", value=0, min_value=0, max_value=img_height, step=10)
        
        with col_c:
            x_end = st.number_input("X End", value=min(100, img_width), min_value=0, max_value=img_width, step=10)
        
        with col_d:
            y_end = st.number_input("Y End", value=min(100, img_height), min_value=0, max_value=img_height, step=10)
        
        # Show preview with selection
        if x_start < x_end and y_start < y_end:
            img_preview = st.session_state.image.copy()
            draw = ImageDraw.Draw(img_preview, 'RGBA')
            
            # Draw selection rectangle
            draw.rectangle(
                [x_start, y_start, x_end, y_end],
                outline=(50, 184, 198),
                width=3,
                fill=(50, 184, 198, 50)
            )
            
            st.image(img_preview, use_column_width=True, caption="Preview with selection")
            st.success(f"✅ Selection: ({int(x_start)}, {int(y_start)}) to ({int(x_end)}, {int(y_end)})")
        
        # Calculate button
        if st.button("📊 Calculate Golden Ratio", type="primary", use_container_width=True):
            width = abs(x_end - x_start)
            height = abs(y_end - y_start)
            
            if width < 10 or height < 10:
                st.error("❌ Selection too small. Please select an area larger than 10×10 pixels.")
            else:
                long_side = max(width, height)
                short_side = min(width, height)
                ratio = long_side / short_side
                difference = abs(ratio - GOLDEN_RATIO)
                score = calculate_score(ratio)
                status, color = get_status(difference)
                
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
                    'x_start': int(x_start),
                    'y_start': int(y_start),
                    'x_end': int(x_end),
                    'y_end': int(y_end)
                }
                st.success("✅ Calculation complete! See results on the right.")
    
    with col2:
        st.subheader("📈 Results")
        
        if st.session_state.measurements:
            m = st.session_state.measurements
            
            # Score display
            st.markdown(f"""
                <div class='score-box'>
                    <div>Golden Ratio Score</div>
                    <div class='score-value'>{m['score']}</div>
                    <div class='score-status'>{m['status']}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Measurements
            st.markdown(f"""
                <div class='metric-box'>
                    <strong>Measured Ratio:</strong><br>
                    <span style='font-size: 24px; color: #21808d; font-weight: bold;'>{m['ratio']:.4f}</span>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class='metric-box'>
                    <strong>Dimensions:</strong><br>
                    {int(m['long_side'])} × {int(m['short_side'])} px
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class='metric-box'>
                    <strong>Difference from φ:</strong><br>
                    <span style='color: #a84b2f; font-weight: bold;'>{m['difference']:.4f}</span>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class='metric-box'>
                    <strong>φ (Golden Ratio):</strong><br>
                    {GOLDEN_RATIO:.4f}
                </div>
            """, unsafe_allow_html=True)
            
            # Download results
            results_text = f"""
Golden Ratio Analysis Results
=============================

Measured Ratio: {m['ratio']:.4f}
Golden Ratio (φ): {GOLDEN_RATIO:.4f}
Difference: {m['difference']:.4f}

Dimensions: {int(m['long_side'])} × {int(m['short_side'])} pixels
Selection: ({m['x_start']}, {m['y_start']}) to ({m['x_end']}, {m['y_end']})

Score: {m['score']}/100
Status: {m['status']}
"""
            st.download_button(
                label="⬇️ Download Results",
                data=results_text,
                file_name="golden_ratio_results.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.info("📊 Enter coordinates and click Calculate to see results")
    
    # Reset button
    st.write("---")
    if st.button("🔄 Reset & Load New Image", use_container_width=True):
        st.session_state.image = None
        st.session_state.measurements = None
        st.rerun()

else:
    st.info("👈 Upload an image or take a photo from the sidebar to get started!")

# About section
with st.expander("ℹ️ About Golden Ratio"):
    st.write("""
    The **Golden Ratio** (φ ≈ 1.618) is a special mathematical number:
    
    **Formula:** φ = (1 + √5) / 2
    
    **Found in Nature:**
    - Flower petals and seeds
    - Seashells and spiral galaxies
    - Human body proportions
    - Snail shells
    
    **Used in Art & Design:**
    - Renaissance paintings (Leonardo da Vinci)
    - Modern architecture (Le Corbusier)
    - Photography composition
    - Web design layouts
    
    **This Calculator:**
    1. Upload or capture an image
    2. Specify an area using coordinates
    3. See how close it is to φ
    4. Score: 0-100 (100 = perfect golden ratio)
    """)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #626c71; font-size: 12px;'>Golden Ratio Calculator • Built with Streamlit</p>", unsafe_allow_html=True)

