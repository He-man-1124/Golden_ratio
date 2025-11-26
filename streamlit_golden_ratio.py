# Golden Ratio Calculator - DEBUG VERSION: See exactly what's happening

import streamlit as st
from PIL import Image
import numpy as np
import math
import base64
from io import BytesIO

st.set_page_config(page_title="Golden Ratio Calculator", page_icon="✨", layout="wide", initial_sidebar_state="expanded")

GOLDEN_RATIO = (1 + math.sqrt(5)) / 2

st.markdown("""
    <style>
    .metric-box { background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 10px 0; border-left: 4px solid #21808d; }
    .score-box { background: linear-gradient(135deg, #21808d, #2da6b2); color: white; padding: 30px; border-radius: 10px; text-align: center; margin: 20px 0; }
    .score-value { font-size: 48px; font-weight: bold; margin: 10px 0; }
    .score-status { font-size: 16px; opacity: 0.9; }
    .title-main { text-align: center; color: #13343b; margin-bottom: 10px; }
    .subtitle { text-align: center; color: #626c71; margin-bottom: 30px; }
    .instruction-box { background-color: #e3f2fd; border-left: 4px solid #2196f3; padding: 15px; margin: 20px 0; border-radius: 5px; }
    .debug-box { background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 10px 0; border-radius: 5px; font-family: monospace; font-size: 12px; }
    #selectionCanvas { border: 2px solid #21808d; border-radius: 8px; cursor: crosshair; display: block; margin: 20px 0; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title-main'>🌀 Golden Ratio Calculator [DEBUG]</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Measure the divine proportion (φ ≈ 1.618) in your images</p>", unsafe_allow_html=True)

# Initialize session state
if 'image' not in st.session_state:
    st.session_state.image = None
if 'measurements' not in st.session_state:
    st.session_state.measurements = None
if 'selection_data' not in st.session_state:
    st.session_state.selection_data = None
if 'debug_log' not in st.session_state:
    st.session_state.debug_log = []

def add_debug(msg):
    """Add message to debug log"""
    st.session_state.debug_log.append(f"[{len(st.session_state.debug_log)+1}] {msg}")

# Sidebar
st.sidebar.header("📸 Image Source")
image_source = st.sidebar.radio("Choose image source:", ["Upload Image", "Use Camera"])

if image_source == "Upload Image":
    uploaded_file = st.sidebar.file_uploader("Choose an image file", type=["jpg", "jpeg", "png", "bmp", "gif"])
    if uploaded_file is not None:
        st.session_state.image = Image.open(uploaded_file)
        st.session_state.measurements = None
        st.session_state.debug_log = []
        add_debug("Image uploaded")
else:
    camera_image = st.sidebar.camera_input("Take a photo")
    if camera_image is not None:
        st.session_state.image = Image.open(camera_image)
        st.session_state.measurements = None
        st.session_state.debug_log = []
        add_debug("Image captured from camera")

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
            1. Drag on the preview to select an area<br>
            2. Blue rectangle shows your selection<br>
            3. Release to capture<br>
            4. Click "Calculate Golden Ratio"
            </div>
        """, unsafe_allow_html=True)
        
        img_width, img_height = st.session_state.image.size
        img_base64 = image_to_base64(st.session_state.image)
        
        st.write(f"**Image Size:** {img_width}×{img_height} pixels")
        
        # Canvas with debug data passing
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
                const data = {{
                    x_start: Math.floor(selection.x),
                    y_start: Math.floor(selection.y),
                    x_end: Math.floor(selection.x + selection.w),
                    y_end: Math.floor(selection.y + selection.h)
                }};
                
                window.selectedData = data;
                console.log('Selection captured:', data);
                
                info.innerHTML = '✅ Selection: X ' + data.x_start + '-' + data.x_end + 
                    ', Y ' + data.y_start + '-' + data.y_end;
            }}
        }});
        
        canvas.addEventListener('mouseleave', () => isDrawing = false);
        </script>
        """
        
        st.components.v1.html(canvas_html, height=img_height + 60)
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("📊 Calculate Golden Ratio", type="primary", use_container_width=True, key="calc_btn"):
                add_debug("Calculate button CLICKED")
                
                # Check if we can access window.selectedData
                st.markdown("""
                <script>
                console.log('Window selected data:', window.selectedData);
                if (window.selectedData) {
                    console.log('Data exists:', window.selectedData);
                } else {
                    console.log('No selection data found');
                }
                </script>
                """, unsafe_allow_html=True)
                
                # For now, use default test values to demonstrate calculation works
                add_debug("Using test values for demonstration")
                
                x_start = 50
                y_start = 50
                x_end = 350
                y_end = 250
                
                add_debug(f"X: {x_start} to {x_end}")
                add_debug(f"Y: {y_start} to {y_end}")
                
                width = x_end - x_start
                height = y_end - y_start
                
                add_debug(f"Width: {width}, Height: {height}")
                
                if width > 0 and height > 0:
                    long_side = max(width, height)
                    short_side = min(width, height)
                    ratio = long_side / short_side
                    difference = abs(ratio - GOLDEN_RATIO)
                    score = calculate_score(ratio)
                    status = get_status(difference)
                    
                    add_debug(f"Long side: {long_side}, Short side: {short_side}")
                    add_debug(f"Ratio calculated: {ratio:.4f}")
                    add_debug(f"Score calculated: {score}")
                    
                    st.session_state.measurements = {
                        'ratio': ratio,
                        'long_side': long_side,
                        'short_side': short_side,
                        'difference': difference,
                        'score': score,
                        'status': status,
                        'x_start': x_start,
                        'y_start': y_start,
                        'x_end': x_end,
                        'y_end': y_end
                    }
                    
                    add_debug("✅ Measurements stored in session state")
                    st.rerun()
                else:
                    add_debug("❌ Invalid dimensions")
        
        with col_btn2:
            if st.button("🔄 Clear", use_container_width=True, key="clear_btn"):
                st.session_state.measurements = None
                st.session_state.debug_log.append("Clear button clicked")
                st.rerun()
    
    with col2:
        st.subheader("📈 Results")
        
        add_debug(f"Checking measurements: {st.session_state.measurements is not None}")
        
        if st.session_state.measurements:
            add_debug("✅ MEASUREMENTS EXIST - ABOUT TO DISPLAY")
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
                    <strong>Ratio:</strong><br>
                    <span style='font-size:24px; color:#21808d; font-weight:bold;'>{m['ratio']:.4f}</span>
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
                    <strong>Difference:</strong><br>
                    <span style='color:#a84b2f; font-weight:bold;'>{m['difference']:.4f}</span>
                </div>
            """, unsafe_allow_html=True)
            
            results = f"Ratio: {m['ratio']:.4f}\nScore: {m['score']}/100"
            st.download_button("⬇️ Download", results, "golden_ratio.txt", use_container_width=True)
        else:
            add_debug("❌ NO MEASUREMENTS TO DISPLAY")
            st.info("📊 Results will appear here")
    
    st.write("---")
    
    # DEBUG SECTION
    st.subheader("🐛 DEBUG LOG")
    
    if st.session_state.debug_log:
        debug_text = "\n".join(st.session_state.debug_log[-20:])  # Last 20 entries
        st.markdown(f"""
            <div class='debug-box'>
            {debug_text}
            </div>
        """, unsafe_allow_html=True)
        
        st.write(f"**Total debug entries:** {len(st.session_state.debug_log)}")
    else:
        st.write("No debug logs yet")
    
    if st.button("🗑️ Clear Debug Log"):
        st.session_state.debug_log = []
        st.rerun()

else:
    st.info("👈 Upload image to start")

st.markdown("<p style='text-align:center;color:#999;font-size:12px;'>Golden Ratio Calculator [DEBUG MODE]</p>", unsafe_allow_html=True)
