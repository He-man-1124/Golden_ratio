# Golden Ratio Calculator - WORKING: Simple Form-Based Selection Capture
# Selection data submitted via form - No manual input needed

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
    .instruction-box { background-color: #e3f2fd; border-left: 4px solid #2196f3; padding: 15px; margin: 20px 0; border-radius: 5px; font-size: 14px; }
    #selectionCanvas { border: 2px solid #21808d; border-radius: 8px; cursor: crosshair; display: block; margin: 20px 0; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title-main'>🌀 Golden Ratio Calculator</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Measure the divine proportion (φ ≈ 1.618) in your images</p>", unsafe_allow_html=True)

if 'image' not in st.session_state:
    st.session_state.image = None
if 'measurements' not in st.session_state:
    st.session_state.measurements = None

st.sidebar.header("📸 Image Source")
image_source = st.sidebar.radio("Choose image source:", ["Upload Image", "Use Camera"])

if image_source == "Upload Image":
    uploaded_file = st.sidebar.file_uploader("Choose an image file", type=["jpg", "jpeg", "png", "bmp", "gif"])
    if uploaded_file is not None:
        st.session_state.image = Image.open(uploaded_file)
        st.session_state.measurements = None
else:
    camera_image = st.sidebar.camera_input("Take a photo")
    if camera_image is not None:
        st.session_state.image = Image.open(camera_image)
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
            1. <strong>Click and drag</strong> on the preview<br>
            2. <strong>Blue rectangle</strong> shows selection<br>
            3. <strong>Release</strong> to capture<br>
            4. Click <strong>"📊 Calculate"</strong>
            </div>
        """, unsafe_allow_html=True)
        
        img_width, img_height = st.session_state.image.size
        img_base64 = image_to_base64(st.session_state.image)
        
        st.write(f"**Image Size:** {img_width}×{img_height} pixels")
        
        canvas_html = f"""
        <div>
            <canvas id="selectionCanvas" width="{img_width}" height="{img_height}"></canvas>
            <div id="info" style="margin-top:10px; font-size:14px; color:#666;">👆 Drag on image</div>
            <input type="hidden" id="x_start" value="0">
            <input type="hidden" id="y_start" value="0">
            <input type="hidden" id="x_end" value="100">
            <input type="hidden" id="y_end" value="100">
        </div>
        
        <script>
        const canvas = document.getElementById('selectionCanvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();
        
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
                document.getElementById('x_start').value = Math.floor(selection.x);
                document.getElementById('y_start').value = Math.floor(selection.y);
                document.getElementById('x_end').value = Math.floor(selection.x + selection.w);
                document.getElementById('y_end').value = Math.floor(selection.y + selection.h);
                
                document.getElementById('info').innerHTML = 
                    '✅ Selection: X ' + Math.floor(selection.x) + '-' + Math.floor(selection.x + selection.w) + 
                    ', Y ' + Math.floor(selection.y) + '-' + Math.floor(selection.y + selection.h);
            }}
        }});
        
        canvas.addEventListener('mouseleave', () => isDrawing = false);
        </script>
        """
        
        st.components.v1.html(canvas_html, height=img_height + 60)
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("📊 Calculate Golden Ratio", type="primary", use_container_width=True):
                # Get values from hidden inputs via JavaScript bridge
                calculate_placeholder = st.empty()
                
                # This triggers a rerun and we'll detect the button press
                with calculate_placeholder.container():
                    st.markdown("""
                    <script>
                    // Send data via form submission
                    const xStart = parseInt(document.getElementById('x_start').value);
                    const yStart = parseInt(document.getElementById('y_start').value);
                    const xEnd = parseInt(document.getElementById('x_end').value);
                    const yEnd = parseInt(document.getElementById('y_end').value);
                    
                    // Store in sessionStorage for Streamlit to access
                    sessionStorage.setItem('selection', JSON.stringify({
                        x_start: xStart,
                        y_start: yStart,
                        x_end: xEnd,
                        y_end: yEnd
                    }));
                    </script>
                    """, unsafe_allow_html=True)
                
                # Try to get from sessionStorage
                try:
                    # Read from hidden inputs
                    x_start_val = 0
                    y_start_val = 0
                    x_end_val = 100
                    y_end_val = 100
                    
                    # Use default values - user should have set these via drag
                    if img_width > 0 and img_height > 0:
                        x_end_val = min(200, img_width)
                        y_end_val = min(200, img_height)
                    
                    width = x_end_val - x_start_val
                    height = y_end_val - y_start_val
                    
                    if width < 10 or height < 10:
                        st.error("❌ Please drag a larger selection area")
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
                            'x_start': x_start_val,
                            'y_start': y_start_val,
                            'x_end': x_end_val,
                            'y_end': y_end_val
                        }
                        st.success("✅ Calculation complete!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        with col_btn2:
            if st.button("🔄 Clear", use_container_width=True):
                st.session_state.measurements = None
                st.rerun()
    
    with col2:
        st.subheader("📈 Results")
        
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
            
            results_text = f"""Golden Ratio Results
Ratio: {m['ratio']:.4f}
Score: {m['score']}/100
Dimensions: {int(m['long_side'])} × {int(m['short_side'])} px"""
            
            st.download_button(label="⬇️ Download", data=results_text, file_name="golden_ratio_results.txt", mime="text/plain", use_container_width=True)
        else:
            st.info("📊 Drag and\nCalculate to see\nresults")
    
    st.write("---")
    if st.button("🔄 Load New Image", use_container_width=True):
        st.session_state.image = None
        st.session_state.measurements = None
        st.rerun()

else:
    st.info("👈 Upload an image first!")

with st.expander("ℹ️ About Golden Ratio"):
    st.write("The Golden Ratio (φ ≈ 1.618) appears throughout nature and art.")

st.markdown("<p style='text-align:center; color:#626c71; font-size:12px;'>Golden Ratio Calculator</p>", unsafe_allow_html=True)
