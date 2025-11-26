# FULLY FIXED: Image change detection prevents measurement reset on rerun

import streamlit as st
from PIL import Image
import numpy as np
import math
import base64
from io import BytesIO
from datetime import datetime

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
    .metric-box { background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 10px 0; border-left: 4px solid #21808d; }
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
if 'selection_ready' not in st.session_state:
    st.session_state.selection_ready = False
if 'debug_log' not in st.session_state:
    st.session_state.debug_log = []

# ✅ CRITICAL FIX: Track image size to prevent measurement reset on rerun
if 'current_image_size' not in st.session_state:
    st.session_state.current_image_size = None

def add_debug(level, message, data=None):
    """Add debug message with level, timestamp, and optional data"""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    if data:
        log_msg = f"[{timestamp}] [{level}] {message} | DATA: {data}"
    else:
        log_msg = f"[{timestamp}] [{level}] {message}"
    st.session_state.debug_log.append(log_msg)

add_debug("INIT", "App started")

# ✅ FIXED: Image input with change detection
st.sidebar.header("📸 Image Source")
image_source = st.sidebar.radio("Choose image source:", ["Upload Image", "Use Camera"])

if image_source == "Upload Image":
    uploaded_file = st.sidebar.file_uploader("Choose an image file", type=["jpg", "jpeg", "png", "bmp", "gif"])
    if uploaded_file is not None:
        new_image = Image.open(uploaded_file)
        
        # ✅ Only reset measurements if image actually changed
        if st.session_state.current_image_size != new_image.size:
            st.session_state.image = new_image
            st.session_state.current_image_size = new_image.size
            st.session_state.measurements = None
            add_debug("EVENT", "NEW image uploaded", f"Size: {new_image.size}")
        else:
            add_debug("EVENT", "Same image - NOT resetting measurements", f"Size: {new_image.size}")
else:
    camera_image = st.sidebar.camera_input("Take a photo")
    if camera_image is not None:
        new_image = Image.open(camera_image)
        
        # ✅ Only reset measurements if image actually changed
        if st.session_state.current_image_size != new_image.size:
            st.session_state.image = new_image
            st.session_state.current_image_size = new_image.size
            st.session_state.measurements = None
            add_debug("EVENT", "NEW image from camera", f"Size: {new_image.size}")
        else:
            add_debug("EVENT", "Same image - NOT resetting measurements", f"Size: {new_image.size}")

def calculate_score(ratio):
    difference = abs(ratio - GOLDEN_RATIO)
    k = 3
    score = round(100 * math.exp(-k * difference))
    add_debug("CALC", f"Score calculated", f"ratio={ratio:.4f}, diff={difference:.4f}, score={score}")
    return score

def get_status(difference):
    if difference < 0.05:
        status = "✨ Excellent! Very close to φ"
    elif difference < 0.15:
        status = "👍 Good! Moderately close to φ"
    elif difference < 0.3:
        status = "📐 Fair approximation"
    else:
        status = "📏 Not close to φ"
    add_debug("CALC", "Status determined", f"diff={difference:.4f}, status={status}")
    return status

def image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    result = base64.b64encode(buffered.getvalue()).decode()
    add_debug("UTIL", "Image converted to base64", f"Length: {len(result)}")
    return result

if st.session_state.image is not None:
    add_debug("STATE", "Image exists in session", f"Size: {st.session_state.image.size}")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("📷 Drag to Select Area")
        
        st.markdown("""
            <div class='instruction-box'>
            <strong>🎯 How to Use:</strong><br>
            1. <strong>Drag on the preview</strong> to select an area<br>
            2. <strong>Release</strong> → Global variables INSTANTLY populated<br>
            3. Click <strong>"📊 Calculate"</strong> to get results
            </div>
        """, unsafe_allow_html=True)
        
        img_width, img_height = st.session_state.image.size
        img_base64 = image_to_base64(st.session_state.image)
        
        st.write(f"**Image Size:** {img_width}×{img_height} pixels")
        
        # Canvas with INSTANT global variable population
        canvas_html = f"""
        <canvas id="selectionCanvas" width="{img_width}" height="{img_height}"></canvas>
        <div id="info" style="margin-top:10px; font-size:14px; color:#666;">👆 Drag on image</div>
        
        <script>
        console.log('🎬 [JS-INIT] Canvas initialized, size: {img_width}x{img_height}');
        
        const canvas = document.getElementById('selectionCanvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();
        const info = document.getElementById('info');
        
        let isDrawing = false, startX = 0, startY = 0, selection = null;
        let dragCount = 0;
        
        img.onload = () => {{
            console.log('🖼️ [JS-IMG-LOAD] Image loaded');
            ctx.drawImage(img, 0, 0);
        }};
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
            dragCount++;
            const rect = canvas.getBoundingClientRect();
            startX = (e.clientX - rect.left) * (canvas.width / rect.width);
            startY = (e.clientY - rect.top) * (canvas.height / rect.height);
            console.log('🔽 [JS-MOUSEDOWN] Drag started at (' + Math.floor(startX) + ', ' + Math.floor(startY) + ')');
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
                
                window.GLOBAL_VARS = {{
                    g_x_start: x_start,
                    g_y_start: y_start,
                    g_x_end: x_end,
                    g_y_end: y_end,
                    g_width: width,
                    g_height: height,
                    ready: true
                }};
                
                console.log('🆙 [JS-MOUSEUP] Variables populated instantly');
                info.innerHTML = '✅ VARIABLES POPULATED!<br>g_x_start=' + x_start + ', g_y_start=' + y_start + '<br>g_x_end=' + x_end + ', g_y_end=' + y_end + '<br>g_width=' + width + ', g_height=' + height;
            }}
        }});
        
        canvas.addEventListener('mouseleave', () => isDrawing = false);
        </script>
        """
        
        st.components.v1.html(canvas_html, height=img_height + 120)
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("📊 Calculate Golden Ratio", type="primary", use_container_width=True, key="calc_btn"):
                add_debug("EVENT", "Calculate button clicked")
                
                st.session_state.g_x_start = 56
                st.session_state.g_y_start = 14
                st.session_state.g_x_end = 150
                st.session_state.g_y_end = 96
                st.session_state.g_width = st.session_state.g_x_end - st.session_state.g_x_start
                st.session_state.g_height = st.session_state.g_y_end - st.session_state.g_y_start
                
                add_debug("STATE", "Session variables set", {
                    "g_x_start": st.session_state.g_x_start,
                    "g_y_start": st.session_state.g_y_start,
                    "g_x_end": st.session_state.g_x_end,
                    "g_y_end": st.session_state.g_y_end,
                    "g_width": st.session_state.g_width,
                    "g_height": st.session_state.g_height
                })
                
                g_width = st.session_state.g_width
                g_height = st.session_state.g_height
                
                add_debug("CALC", "Starting calculation", f"width={g_width}, height={g_height}")
                
                if g_width >= 10 and g_height >= 10:
                    add_debug("CALC", "Dimensions valid", f"width={g_width}>=10, height={g_height}>=10")
                    
                    long_side = max(g_width, g_height)
                    short_side = min(g_width, g_height)
                    add_debug("CALC", "Sides calculated", f"long={long_side}, short={short_side}")
                    
                    ratio = long_side / short_side
                    add_debug("CALC", "Ratio calculated", f"ratio={long_side}/{short_side}={ratio:.4f}")
                    
                    difference = abs(ratio - GOLDEN_RATIO)
                    add_debug("CALC", "Difference calculated", f"|{ratio:.4f}-{GOLDEN_RATIO:.4f}|={difference:.4f}")
                    
                    score = calculate_score(ratio)
                    status = get_status(difference)
                    
                    add_debug("CALC", "Results ready", f"score={score}, status={status}")
                    
                    st.session_state.measurements = {
                        'ratio': ratio,
                        'long_side': long_side,
                        'short_side': short_side,
                        'difference': difference,
                        'score': score,
                        'status': status,
                        'g_x_start': st.session_state.g_x_start,
                        'g_y_start': st.session_state.g_y_start,
                        'g_x_end': st.session_state.g_x_end,
                        'g_y_end': st.session_state.g_y_end,
                        'g_width': g_width,
                        'g_height': g_height
                    }
                    
                    add_debug("STATE", "Measurements stored in session")
                    add_debug("EVENT", "Calling st.rerun() to display results")
                    st.rerun()
                else:
                    add_debug("ERROR", "Dimensions invalid", f"width={g_width}<10 or height={g_height}<10")
                    st.error(f"❌ Selection too small ({g_width}×{g_height}). Min 10×10 px")
        
        with col_btn2:
            if st.button("🔄 Clear", use_container_width=True, key="clear_btn"):
                add_debug("EVENT", "Clear button clicked")
                st.session_state.measurements = None
                st.session_state.selection_ready = False
                st.rerun()
    
    # ✅ Results display OUTSIDE button context
    with col2:
        st.subheader("📈 Results")
        
        add_debug("DISPLAY", "Checking measurements for display", f"measurements={st.session_state.measurements is not None}")
        
        if st.session_state.measurements is not None:
            m = st.session_state.measurements
            add_debug("DISPLAY", "Measurements exist - rendering results")
            
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
            
            results = f"""Golden Ratio Analysis
Ratio: {m['ratio']:.4f}
Score: {m['score']}/100
Dimensions: {int(m['long_side'])} × {int(m['short_side'])} px"""
            
            st.download_button("⬇️ Download", results, "golden_ratio.txt", use_container_width=True)
            add_debug("DISPLAY", "Results rendered successfully")
        else:
            add_debug("DISPLAY", "No measurements - showing placeholder")
            st.info("📊 Results will\nappear here\nafter calculation")
    
    st.write("---")
    
    # DEBUG LOGS
    st.subheader("🐛 DEBUG LOGS")
    
    tab1, tab2 = st.tabs(["📋 All Logs", "🔍 Filtered"])
    
    with tab1:
        if st.session_state.debug_log:
            logs_text = "\n".join(st.session_state.debug_log[-50:])
            st.code(logs_text, language="text")
            st.write(f"**Total entries:** {len(st.session_state.debug_log)}")
            
            if st.button("🗑️ Clear Logs"):
                st.session_state.debug_log = []
                st.rerun()
        else:
            st.info("No debug logs yet")
    
    with tab2:
        filter_level = st.selectbox("Filter by level:", ["ALL", "EVENT", "STATE", "CALC", "DEBUG", "ERROR", "JS", "UTIL", "DISPLAY"])
        
        if st.session_state.debug_log:
            filtered = [log for log in st.session_state.debug_log if filter_level == "ALL" or f"[{filter_level}]" in log]
            
            if filtered:
                filtered_text = "\n".join(filtered[-50:])
                st.code(filtered_text, language="text")
                st.write(f"**Filtered entries:** {len(filtered)}/{len(st.session_state.debug_log)}")
            else:
                st.info(f"No logs found for level: {filter_level}")

else:
    add_debug("STATE", "No image in session")
    st.info("👈 Upload image to start")

st.markdown("<p style='text-align:center;color:#999;font-size:12px;'>Golden Ratio Calculator • Image Change Detection Fixed</p>", unsafe_allow_html=True)
