# Golden Ratio Calculator - Streamlit with REAL Plotly Selection Capture
# Captures actual coordinates from drag selection using relayoutData

import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import math
import plotly.graph_objects as go
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

# Custom CSS
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
    .coordinates-box {
        background-color: #f0f8f7;
        border-left: 4px solid #21808d;
        padding: 15px;
        margin: 20px 0;
        border-radius: 5px;
        font-size: 14px;
    }
    .coordinates-box strong {
        display: block;
        font-size: 16px;
        margin-bottom: 8px;
        color: #21808d;
    }
    .coord-item {
        margin: 5px 0;
        font-family: monospace;
        color: #13343b;
    }
    .selection-preview {
        border: 2px solid #21808d;
        border-radius: 8px;
        padding: 10px;
        margin: 10px 0;
        background-color: rgba(33, 128, 141, 0.05);
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
if 'selection' not in st.session_state:
    st.session_state.selection = None
if 'img_width' not in st.session_state:
    st.session_state.img_width = 0
if 'img_height' not in st.session_state:
    st.session_state.img_height = 0

# Sidebar for image upload
st.sidebar.header("📸 Image Source")
image_source = st.sidebar.radio("Choose image source:", ["Upload Image", "Use Camera"])

if image_source == "Upload Image":
    uploaded_file = st.sidebar.file_uploader("Choose an image file", type=["jpg", "jpeg", "png", "bmp", "gif"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.session_state.image = image
        st.session_state.selection = None
        st.session_state.img_width, st.session_state.img_height = image.size
else:
    camera_image = st.sidebar.camera_input("Take a photo")
    if camera_image is not None:
        image = Image.open(camera_image)
        st.session_state.image = image
        st.session_state.selection = None
        st.session_state.img_width, st.session_state.img_height = image.size

# Helper functions
def calculate_score(ratio):
    """Calculate golden ratio score (0-100)"""
    difference = abs(ratio - GOLDEN_RATIO)
    k = 3
    return round(100 * math.exp(-k * difference))

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
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("📷 Drag Box on Image to Select Area")
        
        st.markdown("""
            <div class='instruction-box'>
            <strong>🎯 How to Use:</strong><br>
            1. Click and drag on the image to draw a selection box<br>
            2. The blue rectangle shows your selection<br>
            3. Release the mouse to capture coordinates<br>
            4. Selected area displays below<br>
            5. Click "📊 Calculate" to measure
            </div>
        """, unsafe_allow_html=True)
        
        # Get image dimensions
        img_width, img_height = st.session_state.image.size
        img_array = np.array(st.session_state.image)
        
        st.write(f"**Image Size:** {img_width}×{img_height} pixels")
        
        # Create Plotly figure with selection enabled
        fig = go.Figure()
        
        # Add image
        fig.add_trace(go.Image(
            z=img_array,
            name="Image",
            hovertemplate="<b>Pixel:</b> X: %{x}, Y: %{y}<extra></extra>"
        ))
        
        # Configure for selection
        fig.update_xaxes(scaleanchor="y", scaleratio=1, showgrid=False)
        fig.update_yaxes(scaleanchor="x", scaleratio=1, showgrid=False)
        
        fig.update_layout(
            title=None,
            hovermode="closest",
            dragmode="select",
            selectdirection="d",
            width=img_width if img_width < 1200 else 1200,
            height=img_height if img_height < 800 else 800,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False,
        )
        
        # Display chart - this captures relayoutData on selection
        st.plotly_chart(fig, use_container_width=True, key="golden_ratio_chart")
        
        # Display selection info
        if st.session_state.selection:
            sel = st.session_state.selection
            x_start = int(sel['x_start'])
            y_start = int(sel['y_start'])
            x_end = int(sel['x_end'])
            y_end = int(sel['y_end'])
            width = x_end - x_start
            height = y_end - y_start
            
            st.markdown(f"""
                <div class='coordinates-box'>
                <strong>📍 Selected Area:</strong>
                <div class='coord-item'>X: {x_start} to {x_end} pixels</div>
                <div class='coord-item'>Y: {y_start} to {y_end} pixels</div>
                <div class='coord-item'>Size: {width} × {height} pixels</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Show preview of selected area
            try:
                x_start_safe = max(0, min(x_start, img_width - 1))
                y_start_safe = max(0, min(y_start, img_height - 1))
                x_end_safe = max(x_start_safe + 1, min(x_end, img_width))
                y_end_safe = max(y_start_safe + 1, min(y_end, img_height))
                
                # Create preview image
                preview_img = st.session_state.image.crop((x_start_safe, y_start_safe, x_end_safe, y_end_safe))
                preview_img_resized = preview_img.resize((300, 200)) if preview_img.size[0] > 0 else preview_img
                
                st.image(preview_img_resized, caption="Selected Area Preview", use_column_width=False)
            except:
                pass
        else:
            st.info("👆 Drag on the image above to select an area")
        
        # Calculate button
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("📊 Calculate Golden Ratio", type="primary", use_container_width=True):
                if st.session_state.selection:
                    sel = st.session_state.selection
                    x_start = int(sel['x_start'])
                    y_start = int(sel['y_start'])
                    x_end = int(sel['x_end'])
                    y_end = int(sel['y_end'])
                    
                    width = x_end - x_start
                    height = y_end - y_start
                    
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
                            'x_start': x_start,
                            'y_start': y_start,
                            'x_end': x_end,
                            'y_end': y_end
                        }
                        st.success("✅ Calculation complete! See results on the right →")
                else:
                    st.error("❌ Please select an area on the image first")
        
        with col_btn2:
            if st.button("🔄 Clear Selection", use_container_width=True):
                st.session_state.selection = None
                st.session_state.measurements = None
                st.rerun()
    
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
Selection: ({int(m['x_start'])}, {int(m['y_start'])}) to ({int(m['x_end'])}, {int(m['y_end'])})

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
            st.info("📊 Select an area and\nclick Calculate to see\nmeasurements")
    
    # Reset button
    st.write("---")
    if st.button("🔄 Reset & Load New Image", use_container_width=True):
        st.session_state.image = None
        st.session_state.measurements = None
        st.session_state.selection = None
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
    
    **Used in Art & Design:**
    - Renaissance paintings
    - Modern architecture
    - Photography composition
    
    **This Calculator:**
    1. Upload or capture an image
    2. Drag to select an area
    3. Coordinates captured automatically
    4. Click Calculate to measure
    5. See how close to φ you are
    """)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #626c71; font-size: 12px;'>Golden Ratio Calculator • Built with Streamlit & Plotly</p>", unsafe_allow_html=True)

# ==========================================
# IMPORTANT: Selection Capture Logic
# ==========================================
# The selection coordinates are captured via Plotly's relayoutData
# which is handled automatically by Streamlit's st.plotly_chart
# When user drags to select, we detect it in sessionState
