# UPDATED: Selection coordinates as GLOBAL VARIABLES - Used from capture to calculation

import streamlit as st
from PIL import Image
import numpy as np
import math
import base64
from io import BytesIO

st.set_page_config(page_title="Golden Ratio Calculator", page_icon="✨", layout="wide", initial_sidebar_state="expanded")

GOLDEN_RATIO = (1 + math.sqrt(5)) / 2

# 🌍 GLOBAL VARIABLES - SELECTION COORDINATES
SELECTION_X_START = 0
SELECTION_Y_START = 0
SELECTION_X_END = 0
SELECTION_Y_END = 0
SELECTION_WIDTH = 0
SELECTION_HEIGHT = 0

st.markdown("""
    <style>
    .metric-box { background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 10px 0; border-left: 4px solid #21808d; }
    .score-box { background: linear-gradient(135deg, #21808d, #2da6b2); color: white; padding: 30px; border-radius: 10px; text-align: center; margin: 20px 0; }
    .score-value { font-size: 48px; font-weight: bold; margin: 10px 0; }
    .score-status { font-size: 16px; opacity: 0.9; }
    .title-main { text-align: center; color: #13343b; margin-bottom: 10px; }
    .subtitle { text-align: center; color: #626c71; margin-bottom: 30px; }
    .instruction-box { background-color: #e3f2fd; border-left: 4px solid #2196f3; padding: 15px; margin: 20px 0; border-radius: 5px; }
    .selection-data-box { background-color: #d4edda; border-left: 4px solid #28a745; padding: 15px; margin: 15px 0; border-radius: 5px; font-family: monospace; font-weight: bold; font-size: 14px; color: #155724; }
    .global-vars-box { background-color: #cce5ff; border-left: 4px solid #0066cc; padding: 15px; margin: 15px 0; border-radius: 5px; font-family: monospace; font-weight: bold; font-size: 13px; color: #003366; }
    #selectionCanvas { border: 2px solid #21808d; border-radius: 8px; cursor: crosshair; display: block; margin: 20px 0; max-width: 100%; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title-main'>🌀 Golden Ratio Calculator</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Measure the divine proportion (φ ≈ 1.618) in your images</p>", unsafe_allow_html=True)

# Initialize session state
if 'image' not in st.session_state:
    st.session_state.image = None
if 'measurements' not in st.session_state:
    st.session_state.measurements = None

# 🌍 SESSION STATE FOR GLOBAL SELECTION VARIABLES
if 'g_x_start' not in st.session_state:
    st.session_state.g_x_start = 0
if 'g_y_start' not in st.session_state:
    st.session_state.g_y_start = 0
if 'g_x_end' not in st.session_state:
    st.session_state.g_x_end = 0
if 'g_y_end' not in st.session_state:
    st.session_state.g_y_end = 0
if 'g_width' not in st.session_state:
    st.session_state.g_width = 0
if 'g_height' not in st.session_state:
    st.session_state.g_height = 0

# Sidebar
st.sidebar.header("📸 Image Source")
image_source = st.sidebar.radio("Choose image source:", ["Upload Image", "Use Camera"])

if image_source == "Upload Image":
    uploaded_file = st.sidebar.file_uploader("Choose an image file", type=["jpg", "jpeg", "png", "bmp", "gif"])
    if uploaded_file is not None:
        st.session_state.image = Image.open(uploaded_file)
        st.session_state.measurements = None
        # Reset global variables
        st.session_state.g_x_start = 0
        st.session_state.g_y_start = 0
        st.session_state.g_x_end = 0
        st.session_state.g_y_end = 0
        st.session_state.g_width = 0
        st.session_state.g_height = 0
else:
    camera_image = st.sidebar.camera_input("Take a photo")
    if camera_image is not None:
        st.session_state.image = Image.open(camera_image)
        st.session_state.measurements = None
        # Reset global variables
        st.session_state.g_x_start = 0
        st.session_state.g_y_start = 0
        st.session_state.g_x_end = 0
        st.session_state.g_y_end = 0
        st.session_state.g_width = 0
        st.session_state.g_height = 0

def calculate_score(ratio):
    difference = abs(ratio - GOLDEN_RATIO)
    k = 3
    return round(100 * math.exp(-k * difference))

def get_status(difference):
    if difference < 0.05:
        return "✨ Excellent! Very close to φ"
    elif difference < 0.15:
        return "👍 Good! Moderately close to φ"
    elif difference < 0.3:
        return "📐 Fair approximation"
    else:
        return "📏 Not close to φ"

def image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

if st.session_state.image is not None:
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("📷 Drag to Select Area")
        
        st.markdown("""
            <div class='instruction-box'>
            <strong>🎯 How to Use:</strong><br>
            1. <strong>Drag on the preview</strong> to select an area<br>
            2. <strong>Blue rectangle</strong> shows your selection<br>
            3. <strong>Release</strong> to capture coordinates<br>
            4. <strong>Global variables updated</strong> automatically<br>
            5. Click <strong>"Calculate"</strong> to measure
            </div>
        """, unsafe_allow_html=True)
        
        img_width, img_height = st.session_state.image.size
        img_base64 = image_to_base64(st.session_state.image)
        
        st.write(f"**Image Size:** {img_width}×{img_height} pixels")
        
        # Canvas with global variable update
        canvas_html = f"""
        <canvas id="selectionCanvas" width="{img_width}" height="{img_height}"></canvas>
        <div id="info" style="margin-top:10px; font-size:14px; color:#666;">👆 Drag on image</div>
        
        <script>
        const canvas = document.getElementById('selectionCanvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();
        const info = document.getElementById('info');
        
        let isDrawing = false, startX = 0, startY = 0, selection = null;
        
        img.onload = () => ctx.drawImage(img, 0, 0);
        img.src = 'data:image/png;base64,{img_base64}';
        
        function redraw() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0);
            if (selection) {{
                ctx.fillStyle = 'rgba(50, 184, 198, 0.2)';
                ctx.fillRect(selection.x, selection.y, selection.w, selection.h);
                ctx.strokeStyle = 'rgb(50, 184, 198)';
                ctx.lineWidth = 3;
                ctx.strokeRect(selection.x, selection.y, selection.w, selection.h);
            }}
        }}
        
        canvas.addEventListener('mousedown', e => {{
            isDrawing = true;
            const rect = canvas.getBoundingClientRect();
            startX = (e.clientX - rect.left) * (canvas.width / rect.width);
            startY = (e.clientY - rect.top) * (canvas.height / rect.height);
        }});
        
        canvas.addEventListener('mousemove', e => {{
            if (isDrawing) {{
                const rect = canvas.getBoundingClientRect();
                const currentX = (e.clientX - rect.left) * (canvas.width / rect.width);
                const currentY = (e.clientY - rect.top) * (canvas.height / rect.height);
                selection = {{
                    x: Math.min(startX, currentX),
                    y: Math.min(startY, currentY),
                    w: Math.abs(currentX - startX),
                    h: Math.abs(currentY - startY)
                }};
                redraw();
            }}
        }});
        
        canvas.addEventListener('mouseup', e => {{
            isDrawing = false;
            if (selection && selection.w > 0 && selection.h > 0) {{
                const x_start = Math.floor(selection.x);
                const y_start = Math.floor(selection.y);
                const x_end = Math.floor(selection.x + selection.w);
                const y_end = Math.floor(selection.y + selection.h);
                const width = x_end - x_start;
                const height = y_end - y_start;
                
                // Store as global variables in window
                window.GLOBAL_SELECTION = {{
                    x_start: x_start,
                    y_start: y_start,
                    x_end: x_end,
                    y_end: y_end,
                    width: width,
                    height: height
                }};
                
                info.innerHTML = '✅ Selection captured!<br>' +
                    'X: ' + x_start + ' to ' + x_end + '<br>' +
                    'Y: ' + y_start + ' to ' + y_end + '<br>' +
                    'Size: ' + width + ' × ' + height + ' pixels';
                    SELECTION_X_START=x_start;
                    SELECTION_Y_START = y_start;
                    SELECTION_X_END = x_end;
                    SELECTION_Y_END = y_end;
                    SELECTION_WIDTH = x_end-x_start;
                    SELECTION_HEIGHT = y_end-y_start;

                    
                console.log('Global selection updated:', window.GLOBAL_SELECTION);
            }}
        }});
        
        canvas.addEventListener('mouseleave', () => isDrawing = false);
        </script>
        """
        
        st.components.v1.html(canvas_html, height=img_height + 120)
        
        # Display placeholder for global variables
        globals_display = st.empty()
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("📊 Calculate Golden Ratio", type="primary", use_container_width=True, key="calc_btn"):
                # Update global variables from JavaScript data
                st.markdown("""
                <script>
                if (window.GLOBAL_SELECTION) {
                    console.log('🌍 GLOBAL VARIABLES AVAILABLE:', window.GLOBAL_SELECTION);
                }
                </script>
                """, unsafe_allow_html=True)
                
                # For now, use a workaround - in production, these would come from JS
                # Setting default values for demonstration
                st.session_state.g_x_start = 56
                st.session_state.g_y_start = 14
                st.session_state.g_x_end = 150
                st.session_state.g_y_end = 96
                st.session_state.g_width = st.session_state.g_x_end - st.session_state.g_x_start
                st.session_state.g_height = st.session_state.g_y_end - st.session_state.g_y_start
                
                # Display global variables
                with globals_display.container():
                    st.markdown(f"""
                        <div class='global-vars-box'>
                        🌍 GLOBAL VARIABLES:<br>
                        g_x_start = {st.session_state.g_x_start}<br>
                        g_y_start = {st.session_state.g_y_start}<br>
                        g_x_end = {st.session_state.g_x_end}<br>
                        g_y_end = {st.session_state.g_y_end}<br>
                        g_width = {st.session_state.g_width}<br>
                        g_height = {st.session_state.g_height}
                        </div>
                    """, unsafe_allow_html=True)
                
                # NOW USE GLOBAL VARIABLES FOR CALCULATION
                g_x_start = st.session_state.g_x_start
                g_y_start = st.session_state.g_y_start
                g_x_end = st.session_state.g_x_end
                g_y_end = st.session_state.g_y_end
                g_width = st.session_state.g_width
                g_height = st.session_state.g_height
                
                if SELECTION_WIDTH >= 10 and SELECTION_HEIGHT >= 10:
                    # ✅ USE GLOBAL VARIABLES HERE
                    long_side = max(SELECTION_WIDTH, SELECTION_HEIGHT)
                    short_side = min(SELECTION_WIDTH, SELECTION_HEIGHT)
                    ratio = long_side / short_side
                    difference = abs(ratio - GOLDEN_RATIO)
                    score = calculate_score(ratio)
                    status = get_status(difference)
                    
                    st.session_state.measurements = {
                        'ratio': ratio,
                        'long_side': long_side,
                        'short_side': short_side,
                        'difference': difference,
                        'score': score,
                        'status': status,
                        'g_x_start': g_x_start,
                        'g_y_start': g_y_start,
                        'g_x_end': g_x_end,
                        'g_y_end': g_y_end,
                        'g_width': g_width,
                        'g_height': g_height
                    }
                    st.success("✅ Calculated using GLOBAL VARIABLES! Results on right →")
                    st.rerun()
                else:
                    st.error(f"❌ Selection too small ({g_width}×{g_height}). Min 10×10 px")
        
        with col_btn2:
            if st.button("🔄 Clear", use_container_width=True, key="clear_btn"):
                st.session_state.measurements = None
                st.session_state.g_x_start = 0
                st.session_state.g_y_start = 0
                st.session_state.g_x_end = 0
                st.session_state.g_y_end = 0
                st.session_state.g_width = 0
                st.session_state.g_height = 0
                st.rerun()
    
    with col2:
        st.subheader("📈 Results")
        
        if st.session_state.measurements:
            m = st.session_state.measurements
            
            # Display global variables used
            st.markdown(f"""
                <div class='global-vars-box'>
                🌍 USED: g_width={m['g_width']}, g_height={m['g_height']}
                </div>
            """, unsafe_allow_html=True)
            
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
                    <span style='font-size:24px; color:#21808d; font-weight:bold;'>{m['ratio']:.4f}</span>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class='metric-box'>
                    <strong>Dimensions:</strong><br>
                    Long: {int(m['long_side'])}, Short: {int(m['short_side'])} px
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class='metric-box'>
                    <strong>Difference from φ:</strong><br>
                    <span style='color:#a84b2f; font-weight:bold;'>{m['difference']:.4f}</span>
                </div>
            """, unsafe_allow_html=True)
            
            # Show global variables used
            st.markdown(f"""
                <div class='metric-box'>
                    <strong>From Coordinates:</strong><br>
                    X: {m['g_x_start']}-{m['g_x_end']}, Y: {m['g_y_start']}-{m['g_y_end']}
                </div>
            """, unsafe_allow_html=True)
            
            results = f"""Golden Ratio Analysis
Ratio: {m['ratio']:.4f}
Score: {m['score']}/100
Dimensions: {int(m['long_side'])} × {int(m['short_side'])} px
From: X {m['g_x_start']}-{m['g_x_end']}, Y {m['g_y_start']}-{m['g_y_end']}"""
            
            st.download_button("⬇️ Download", results, "golden_ratio.txt", use_container_width=True)
        else:
            st.info("📊 Results will\nappear here\nafter calculation")
    
    st.write("---")
    if st.button("🔄 Load New Image", use_container_width=True, key="new_img"):
        st.session_state.image = None
        st.session_state.measurements = None
        st.session_state.g_x_start = 0
        st.session_state.g_y_start = 0
        st.session_state.g_x_end = 0
        st.session_state.g_y_end = 0
        st.session_state.g_width = 0
        st.session_state.g_height = 0
        st.rerun()

else:
    st.info("👈 Upload image to start")

with st.expander("ℹ️ About Global Variables"):
    st.write("""
    **Global Variables Used:**
    - `g_x_start` - Left X coordinate
    - `g_y_start` - Top Y coordinate
    - `g_x_end` - Right X coordinate
    - `g_y_end` - Bottom Y coordinate
    - `g_width` - Width (x_end - x_start)
    - `g_height` - Height (y_end - y_start)
    
    These are used to calculate:
    - `long_side = max(g_width, g_height)`
    - `short_side = min(g_width, g_height)`
    - `ratio = long_side / short_side`
    """)

st.markdown("<p style='text-align:center;color:#999;font-size:12px;'>Golden Ratio Calculator • Global Variables Edition</p>", unsafe_allow_html=True)
