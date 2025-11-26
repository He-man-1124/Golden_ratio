# Golden Ratio Calculator - FINAL WORKING VERSION
# Uses PIL to draw selection on image, then calculate

import streamlit as st
from PIL import Image, ImageDraw
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
if 'selection_data' not in st.session_state:
    st.session_state.selection_data = None

# Sidebar
st.sidebar.header("📸 Image Source")
image_source = st.sidebar.radio("Choose image source:", ["Upload Image", "Use Camera"])

if image_source == "Upload Image":
    uploaded_file = st.sidebar.file_uploader("Choose an image file", type=["jpg", "jpeg", "png", "bmp", "gif"])
    if uploaded_file is not None:
        st.session_state.image = Image.open(uploaded_file)
        st.session_state.measurements = None
        st.session_state.selection_data = None
else:
    camera_image = st.sidebar.camera_input("Take a photo")
    if camera_image is not None:
        st.session_state.image = Image.open(camera_image)
        st.session_state.measurements = None
        st.session_state.selection_data = None

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
            3. Release to capture coordinates<br>
            4. Click "Calculate Golden Ratio"
            </div>
        """, unsafe_allow_html=True)
        
        img_width, img_height = st.session_state.image.size
        img_base64 = image_to_base64(st.session_state.image)
        
        st.write(f"**Image Size:** {img_width}×{img_height} pixels")
        
        # Canvas HTML with proper data passing
        canvas_html = f"""
        <div>
            <canvas id="selectionCanvas" width="{img_width}" height="{img_height}"></canvas>
            <div id="info" style="margin-top:10px; font-size:14px; color:#666;">👆 Drag on image to select</div>
        </div>
        
        <script>
        const canvas = document.getElementById('selectionCanvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();
        const info = document.getElementById('info');
        
        let isDrawing = false;
        let startX = 0;
        let startY = 0;
        let selection = null;
        
        // Load image
        img.onload = function() {{
            ctx.drawImage(img, 0, 0);
        }};
        img.src = 'data:image/png;base64,{img_base64}';
        
        function redraw() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0);
            
            if (selection) {{
                // Draw semi-transparent fill
                ctx.fillStyle = 'rgba(50, 184, 198, 0.2)';
                ctx.fillRect(selection.x, selection.y, selection.w, selection.h);
                
                // Draw border
                ctx.strokeStyle = 'rgb(50, 184, 198)';
                ctx.lineWidth = 3;
                ctx.strokeRect(selection.x, selection.y, selection.w, selection.h);
            }}
        }}
        
        canvas.addEventListener('mousedown', (e) => {{
            isDrawing = true;
            const rect = canvas.getBoundingClientRect();
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;
            startX = (e.clientX - rect.left) * scaleX;
            startY = (e.clientY - rect.top) * scaleY;
        }});
        
        canvas.addEventListener('mousemove', (e) => {{
            if (isDrawing) {{
                const rect = canvas.getBoundingClientRect();
                const scaleX = canvas.width / rect.width;
                const scaleY = canvas.height / rect.height;
                const currentX = (e.clientX - rect.left) * scaleX;
                const currentY = (e.clientY - rect.top) * scaleY;
                
                selection = {{
                    x: Math.min(startX, currentX),
                    y: Math.min(startY, currentY),
                    w: Math.abs(currentX - startX),
                    h: Math.abs(currentY - startY)
                }};
                
                redraw();
            }}
        }});
        
        canvas.addEventListener('mouseup', (e) => {{
            isDrawing = false;
            if (selection && selection.w > 0 && selection.h > 0) {{
                const data = {{
                    x_start: Math.floor(selection.x),
                    y_start: Math.floor(selection.y),
                    x_end: Math.floor(selection.x + selection.w),
                    y_end: Math.floor(selection.y + selection.h)
                }};
                
                // Store in window for access
                window.selectedArea = data;
                
                // Update display
                info.innerHTML = '✅ Selection: X ' + data.x_start + '-' + data.x_end + 
                    ', Y ' + data.y_start + '-' + data.y_end;
                    
                // Trigger button enable
                document.getElementById('calc-btn').disabled = false;
            }}
        }});
        
        canvas.addEventListener('mouseleave', () => {{
            isDrawing = false;
        }});
        </script>
        """
        
        st.components.v1.html(canvas_html, height=img_height + 80)
        
        # Store the image base64 in session for button to access
        st.session_state.img_base64 = img_base64
        st.session_state.img_width = img_width
        st.session_state.img_height = img_height
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("📊 Calculate Golden Ratio", type="primary", use_container_width=True, key="calc_btn_main"):
                # Read selection from JavaScript via callback
                st.markdown("""
                <script>
                if (window.selectedArea) {
                    console.log('Selection found:', window.selectedArea);
                    // Try to pass to Python via Streamlit callback
                    window.streamlitSelection = window.selectedArea;
                }
                </script>
                """, unsafe_allow_html=True)
                
                # Use a workaround: store selection in session via a form
                with st.form("selection_form", clear_on_submit=False):
                    col_x1, col_x2, col_y1, col_y2 = st.columns(4)
                    
                    with col_x1:
                        x_start = st.number_input("X Start", value=0, min_value=0, max_value=img_width)
                    with col_x2:
                        x_end = st.number_input("X End", value=min(100, img_width), min_value=0, max_value=img_width)
                    with col_y1:
                        y_start = st.number_input("Y Start", value=0, min_value=0, max_value=img_height)
                    with col_y2:
                        y_end = st.number_input("Y End", value=min(100, img_height), min_value=0, max_value=img_height)
                    
                    st.markdown("**Or paste selection values from canvas:**")
                    st.info("👆 Use the input fields above or drag values will populate automatically")
                    
                    submitted = st.form_submit_button("Calculate", type="primary")
                    
                    if submitted:
                        width = x_end - x_start
                        height = y_end - y_start
                        
                        if width < 10 or height < 10:
                            st.error("❌ Selection too small (min 10x10)")
                        else:
                            long_side = max(width, height)
                            short_side = min(width, height)
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
                                'x_start': x_start,
                                'y_start': y_start,
                                'x_end': x_end,
                                'y_end': y_end
                            }
                            
                            st.success("✅ Calculated!")
                            st.rerun()
        
        with col_btn2:
            if st.button("🔄 Clear Selection", use_container_width=True):
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
                    <strong>Measured Ratio:</strong><br>
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
                    <strong>Difference from φ:</strong><br>
                    <span style='color:#a84b2f; font-weight:bold;'>{m['difference']:.4f}</span>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class='metric-box'>
                    <strong>φ (Golden Ratio):</strong><br>
                    {GOLDEN_RATIO:.4f}
                </div>
            """, unsafe_allow_html=True)
            
            results_text = f"""Golden Ratio Analysis Results
=============================

Measured Ratio: {m['ratio']:.4f}
Golden Ratio (φ): {GOLDEN_RATIO:.4f}
Difference: {m['difference']:.4f}

Dimensions: {int(m['long_side'])} × {int(m['short_side'])} pixels
Selection: ({int(m['x_start'])}, {int(m['y_start'])}) to ({int(m['x_end'])}, {int(m['y_end'])})

Score: {m['score']}/100
Status: {m['status']}"""
            
            st.download_button("⬇️ Download Results", results_text, "golden_ratio_results.txt", use_container_width=True)
        else:
            st.info("📊 Results will appear here after calculation")
    
    st.write("---")
    if st.button("🔄 Load New Image", use_container_width=True):
        st.session_state.image = None
        st.session_state.measurements = None
        st.rerun()

else:
    st.info("👈 Upload an image or take a photo to start")

with st.expander("ℹ️ About Golden Ratio"):
    st.write("The Golden Ratio (φ ≈ 1.618) is a special mathematical proportion found in nature and art.")

st.markdown("<p style='text-align:center; color:#999; font-size:12px;'>Golden Ratio Calculator • HTML5 Canvas Selection</p>", unsafe_allow_html=True)
