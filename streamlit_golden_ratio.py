# Golden Ratio Calculator - SIMPLE & DIRECT: Click to Confirm Selection
# No complex state tracking - just drag, preview, click button, get coordinates

import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import math
import plotly.graph_objects as go

st.set_page_config(
    page_title="Golden Ratio Calculator",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

GOLDEN_RATIO = (1 + math.sqrt(5)) / 2

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
        margin: 15px 0;
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
        margin: 6px 0;
        font-family: 'Courier New', monospace;
        color: #13343b;
        font-weight: 500;
    }
    .step-box {
        background-color: #fff9e6;
        border-left: 4px solid #f59e0b;
        padding: 12px;
        margin: 10px 0;
        border-radius: 5px;
        font-size: 13px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title-main'>🌀 Golden Ratio Calculator</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Measure the divine proportion (φ ≈ 1.618) in your images</p>", unsafe_allow_html=True)

# Initialize session state
if 'image' not in st.session_state:
    st.session_state.image = None
if 'img_array' not in st.session_state:
    st.session_state.img_array = None
if 'measurements' not in st.session_state:
    st.session_state.measurements = None
if 'confirmed_selection' not in st.session_state:
    st.session_state.confirmed_selection = None

# Sidebar
st.sidebar.header("📸 Image Source")
image_source = st.sidebar.radio("Choose image source:", ["Upload Image", "Use Camera"])

if image_source == "Upload Image":
    uploaded_file = st.sidebar.file_uploader("Choose an image file", type=["jpg", "jpeg", "png", "bmp", "gif"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.session_state.image = image
        st.session_state.img_array = np.array(image)
        st.session_state.confirmed_selection = None
        st.session_state.measurements = None
else:
    camera_image = st.sidebar.camera_input("Take a photo")
    if camera_image is not None:
        image = Image.open(camera_image)
        st.session_state.image = image
        st.session_state.img_array = np.array(image)
        st.session_state.confirmed_selection = None
        st.session_state.measurements = None

def calculate_score(ratio):
    difference = abs(ratio - GOLDEN_RATIO)
    k = 3
    return round(100 * math.exp(-k * difference))

def get_status(difference):
    if difference < 0.05:
        return "✨ Excellent! Very close to φ", "#21808d"
    elif difference < 0.15:
        return "👍 Good! Moderately close to φ", "#32b8c6"
    elif difference < 0.3:
        return "📐 Fair approximation", "#a84b2f"
    else:
        return "📏 Not close to φ", "#c0152f"

def draw_selection_on_image(img, x1, y1, x2, y2):
    """Draw selection box on image"""
    img_copy = img.copy()
    draw = ImageDraw.Draw(img_copy, 'RGBA')
    draw.rectangle([x1, y1, x2, y2], fill=(50, 184, 198, 50), outline=(50, 184, 198, 255), width=3)
    return img_copy

# Main app
if st.session_state.image is not None:
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("📷 Step 1: Select Area on Image")
        
        st.markdown("""
            <div class='instruction-box'>
            <strong>🎯 Steps:</strong><br>
            1. <strong>Drag on image below</strong> to create selection box<br>
            2. <strong>Enter exact coordinates</strong> below (or use sliders)<br>
            3. <strong>Preview will show</strong> selected area<br>
            4. <strong>Click "✅ Confirm Selection"</strong> button<br>
            5. <strong>Click "📊 Calculate Golden Ratio"</strong>
            </div>
        """, unsafe_allow_html=True)
        
        img_width, img_height = st.session_state.image.size
        img_array = st.session_state.img_array
        
        st.write(f"**Image Size:** {img_width}×{img_height} pixels")
        
        # Plotly chart
        fig = go.Figure()
        fig.add_trace(go.Image(z=img_array, name="Image"))
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
        
        st.plotly_chart(fig, use_container_width=True, key="chart")
        
        st.write("---")
        st.write("**Step 2: Enter Coordinates**")
        
        # Sliders for coordinate selection
        col_coords = st.columns(4)
        
        default_x_start = 0
        default_y_start = 0
        default_x_end = min(150, img_width)
        default_y_end = min(150, img_height)
        
        with col_coords[0]:
            x_start = st.slider("X Start", 0, img_width, default_x_start, 10, key="x_s")
        with col_coords[1]:
            y_start = st.slider("Y Start", 0, img_height, default_y_start, 10, key="y_s")
        with col_coords[2]:
            x_end = st.slider("X End", 0, img_width, default_x_end, 10, key="x_e")
        with col_coords[3]:
            y_end = st.slider("Y End", 0, img_height, default_y_end, 10, key="y_e")
        
        # Validate
        if x_start >= x_end or y_start >= y_end:
            st.error("❌ Invalid coordinates: X and Y ranges must be positive")
        else:
            width = x_end - x_start
            height = y_end - y_start
            
            st.markdown(f"""
                <div class='coordinates-box'>
                <strong>📍 Current Selection:</strong>
                <div class='coord-item'>X: {int(x_start)} → {int(x_end)} pixels</div>
                <div class='coord-item'>Y: {int(y_start)} → {int(y_end)} pixels</div>
                <div class='coord-item'>Size: {int(width)} × {int(height)} pixels</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Show preview with selection box
            st.write("**Step 3: Preview**")
            
            x_s = max(0, min(int(x_start), img_width - 1))
            y_s = max(0, min(int(y_start), img_height - 1))
            x_e = max(x_s + 1, min(int(x_end), img_width))
            y_e = max(y_s + 1, min(int(y_end), img_height))
            
            # Full image with box
            preview_full = draw_selection_on_image(st.session_state.image, x_s, y_s, x_e, y_e)
            col_prev = st.columns(2)
            
            with col_prev[0]:
                st.image(preview_full, caption="Full Image with Selection", use_column_width=True)
            
            # Cropped area
            with col_prev[1]:
                cropped = st.session_state.image.crop((x_s, y_s, x_e, y_e))
                if cropped.size[0] > 0 and cropped.size[1] > 0:
                    st.image(cropped, caption="Selected Area (Cropped)", use_column_width=True)
            
            # Confirm button
            st.write("**Step 4: Confirm Selection**")
            if st.button("✅ Confirm Selection", type="primary", use_container_width=True):
                st.session_state.confirmed_selection = {
                    'x_start': int(x_start),
                    'y_start': int(y_start),
                    'x_end': int(x_end),
                    'y_end': int(y_end),
                    'width': width,
                    'height': height
                }
                st.success("✅ Selection confirmed! Now click Calculate →")
    
    with col2:
        st.subheader("📈 Results")
        
        # Show confirmed coordinates
        if st.session_state.confirmed_selection:
            sel = st.session_state.confirmed_selection
            st.markdown(f"""
                <div class='coordinates-box'>
                <strong>📍 Confirmed Selection:</strong>
                <div class='coord-item'>X: {sel['x_start']} → {sel['x_end']}</div>
                <div class='coord-item'>Y: {sel['y_start']} → {sel['y_end']}</div>
                <div class='coord-item'>Size: {int(sel['width'])} × {int(sel['height'])}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Calculate button
            if st.button("📊 Calculate Golden Ratio", type="primary", use_container_width=True):
                sel = st.session_state.confirmed_selection
                w = sel['width']
                h = sel['height']
                
                if w < 10 or h < 10:
                    st.error("❌ Selection too small")
                else:
                    long_side = max(w, h)
                    short_side = min(w, h)
                    ratio = long_side / short_side
                    difference = abs(ratio - GOLDEN_RATIO)
                    score = calculate_score(ratio)
                    status, color = get_status(difference)
                    
                    st.session_state.measurements = {
                        'ratio': ratio,
                        'width': w,
                        'height': h,
                        'long_side': long_side,
                        'short_side': short_side,
                        'difference': difference,
                        'score': score,
                        'status': status,
                        'x_start': sel['x_start'],
                        'y_start': sel['y_start'],
                        'x_end': sel['x_end'],
                        'y_end': sel['y_end']
                    }
        
        # Display results
        if st.session_state.measurements:
            m = st.session_state.measurements
            
            st.markdown(f"""
                <div class='score-box'>
                    <div>Golden Ratio Score</div>
                    <div class='score-value'>{m['score']}</div>
                    <div class='score-status'>{m['status']}</div>
                </div>
            """, unsafe_allow_html=True)
            
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
                    <strong>φ:</strong><br>
                    {GOLDEN_RATIO:.4f}
                </div>
            """, unsafe_allow_html=True)
            
            # Download
            results_text = f"""
Golden Ratio Results
===================

Ratio: {m['ratio']:.4f}
φ: {GOLDEN_RATIO:.4f}
Difference: {m['difference']:.4f}
Score: {m['score']}/100
Size: {int(m['long_side'])} × {int(m['short_side'])} px
Selection: ({m['x_start']}, {m['y_start']}) to ({m['x_end']}, {m['y_end']})
"""
            st.download_button(
                label="⬇️ Download Results",
                data=results_text,
                file_name="golden_ratio_results.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.info("📊 Confirm selection and\nclick Calculate")
    
    st.write("---")
    if st.button("🔄 Reset & New Image", use_container_width=True):
        st.session_state.image = None
        st.session_state.img_array = None
        st.session_state.confirmed_selection = None
        st.session_state.measurements = None
        st.rerun()

else:
    st.info("👈 Upload an image or take a photo")

with st.expander("ℹ️ About Golden Ratio"):
    st.write("""
    The **Golden Ratio** (φ ≈ 1.618):
    - Found in nature and art
    - Perfect mathematical proportion
    - Used in design and photography
    """)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #626c71; font-size: 12px;'>Golden Ratio Calculator</p>", unsafe_allow_html=True)
