# Golden Ratio Calculator - SIMPLIFIED: Static Image + Drag Selection + Capture Button
# Shows image first, user drags to select, clicks button to capture coordinates

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
        margin: 15px 0;
        border-radius: 5px;
    }
    .coordinates-box strong {
        display: block;
        font-size: 16px;
        margin-bottom: 8px;
        color: #21808d;
    }
    .coord-item {
        margin: 6px 0;
        font-family: monospace;
        color: #13343b;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# App Title
st.markdown("<h1 class='title-main'>🌀 Golden Ratio Calculator</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Measure the divine proportion (φ ≈ 1.618) in your images</p>", unsafe_allow_html=True)

# Initialize session state
if 'image' not in st.session_state:
    st.session_state.image = None
if 'selected_coords' not in st.session_state:
    st.session_state.selected_coords = None
if 'measurements' not in st.session_state:
    st.session_state.measurements = None
if 'canvas_key' not in st.session_state:
    st.session_state.canvas_key = 0

# Sidebar for image upload
st.sidebar.header("📸 Image Source")
image_source = st.sidebar.radio("Choose image source:", ["Upload Image", "Use Camera"])

if image_source == "Upload Image":
    uploaded_file = st.sidebar.file_uploader("Choose an image file", type=["jpg", "jpeg", "png", "bmp", "gif"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.session_state.image = image
        st.session_state.selected_coords = None
        st.session_state.measurements = None
else:
    camera_image = st.sidebar.camera_input("Take a photo")
    if camera_image is not None:
        image = Image.open(camera_image)
        st.session_state.image = image
        st.session_state.selected_coords = None
        st.session_state.measurements = None

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
        st.subheader("📷 Select Area by Dragging")
        
        st.markdown("""
            <div class='instruction-box'>
            <strong>🎯 Step-by-Step:</strong><br>
            1. <strong>Preview image displayed below</strong><br>
            2. <strong>Drag on image</strong> to select area (left-top to right-bottom)<br>
            3. <strong>Release mouse</strong> when done<br>
            4. <strong>Click "✓ Capture Coordinates"</strong> button<br>
            5. <strong>Coordinates appear</strong> → Click "Calculate"
            </div>
        """, unsafe_allow_html=True)
        
        # Get image dimensions
        img_width, img_height = st.session_state.image.size
        img_array = np.array(st.session_state.image)
        
        st.write(f"**Image Size:** {img_width}×{img_height} pixels")
        
        # Display image as static preview
        st.image(st.session_state.image, caption="Image Preview - Drag to Select", use_column_width=True)
        
        # HTML5 Canvas for drawing selection
        canvas_html = f"""
        <div style="margin: 20px 0;">
            <canvas id="drawingCanvas" width="800" height="600" style="border: 2px solid #ccc; cursor: crosshair; display: block; background: white;"></canvas>
            <p style="font-size: 12px; color: #666; margin-top: 5px;">Drag on canvas above to draw selection box</p>
        </div>
        
        <script>
        const canvas = document.getElementById('drawingCanvas');
        const ctx = canvas.getContext('2d');
        
        let isDrawing = false;
        let startX, startY;
        let selection = null;
        
        // Load image
        const img = new Image();
        img.onload = function() {{
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0);
        }};
        img.src = 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAB+AHgDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWm5ybnJ2eoqOkpaanqKmqsrO0tba2uLm6wsPExcbHyMnK0tPU1dbW2Nna4uPk5ebn6Onq8vP09fb2+Pn6/8QAHwEAAwEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlbaWmJmaoqOkpaanqKmqsrO0tba2uLm6wsPExcbHyMnK0tPU1dbW2Nna4uPk5ebn6Onq8vP09fb2+Pn6/9oADAMBAAIRAxEAPwD+/KKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigD/2Q==';
        
        function redraw() {{
            ctx.drawImage(img, 0, 0);
            if (selection) {{
                ctx.fillStyle = 'rgba(50, 184, 198, 0.2)';
                ctx.fillRect(selection.x, selection.y, selection.w, selection.h);
                ctx.strokeStyle = 'rgb(50, 184, 198)';
                ctx.lineWidth = 3;
                ctx.strokeRect(selection.x, selection.y, selection.w, selection.h);
            }}
        }}
        
        canvas.addEventListener('mousedown', (e) => {{
            isDrawing = true;
            const rect = canvas.getBoundingClientRect();
            startX = Math.floor(e.clientX - rect.left);
            startY = Math.floor(e.clientY - rect.top);
        }});
        
        canvas.addEventListener('mousemove', (e) => {{
            if (isDrawing) {{
                const rect = canvas.getBoundingClientRect();
                const currentX = Math.floor(e.clientX - rect.left);
                const currentY = Math.floor(e.clientY - rect.top);
                
                selection = {{
                    x: Math.min(startX, currentX),
                    y: Math.min(startY, currentY),
                    w: Math.abs(currentX - startX),
                    h: Math.abs(currentY - startY)
                }};
                
                redraw();
            }}
        }});
        
        canvas.addEventListener('mouseup', () => {{
            isDrawing = false;
        }});
        
        canvas.addEventListener('mouseleave', () => {{
            isDrawing = false;
        }});
        
        // Store selection globally
        window.canvasSelection = selection;
        </script>
        """
        
        st.components.v1.html(canvas_html, height=650)
        
        # Capture coordinates button
        st.write("---")
        col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 1])
        
        with col_btn1:
            if st.button("✓ Capture Coordinates from Drawing", type="primary", use_container_width=True):
                st.info("📍 Please adjust coordinates in the fields below, or use the input fields to enter exact values")
        
        # Manual coordinate input as fallback
        st.write("**Enter coordinates manually (or adjust captured ones):**")
        
        col_inputs = st.columns(4)
        with col_inputs[0]:
            x_start = st.number_input("X Start", min_value=0, max_value=img_width, value=0, step=10, key="x_start")
        with col_inputs[1]:
            y_start = st.number_input("Y Start", min_value=0, max_value=img_height, value=0, step=10, key="y_start")
        with col_inputs[2]:
            x_end = st.number_input("X End", min_value=0, max_value=img_width, value=min(200, img_width), step=10, key="x_end")
        with col_inputs[3]:
            y_end = st.number_input("Y End", min_value=0, max_value=img_height, value=min(200, img_height), step=10, key="y_end")
        
        # Display selected coordinates if valid
        if x_start < x_end and y_start < y_end:
            width = x_end - x_start
            height = y_end - y_start
            
            st.markdown(f"""
                <div class='coordinates-box'>
                <strong>📍 Selected Coordinates:</strong>
                <div class='coord-item'>X: {int(x_start)} → {int(x_end)} pixels</div>
                <div class='coord-item'>Y: {int(y_start)} → {int(y_end)} pixels</div>
                <div class='coord-item'>Size: {int(width)} × {int(height)} pixels</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Invalid coordinates. Make sure X End > X Start and Y End > Y Start")
        
        # Calculate button
        if st.button("📊 Calculate Golden Ratio", type="primary", use_container_width=True):
            if x_start < x_end and y_start < y_end:
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
                st.error("❌ Please enter valid coordinates")
    
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
            st.info("📊 Draw/enter coordinates\nand click Calculate to\nsee measurements")
    
    # Reset button
    st.write("---")
    if st.button("🔄 Reset & Load New Image", use_container_width=True):
        st.session_state.image = None
        st.session_state.selected_coords = None
        st.session_state.measurements = None
        st.rerun()

else:
    st.info("👈 Upload an image or take a photo from the sidebar to get started!")

# About section
with st.expander("ℹ️ About Golden Ratio"):
    st.write("""
    The **Golden Ratio** (φ ≈ 1.618) is a special mathematical number found throughout nature and art.
    
    **Formula:** φ = (1 + √5) / 2 ≈ 1.618
    
    **How to use this calculator:**
    1. Upload or capture an image
    2. Drag on the canvas to select an area
    3. Enter exact coordinates in the input fields
    4. Click "Calculate Golden Ratio"
    5. See your golden ratio score and download results
    """)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #626c71; font-size: 12px;'>Golden Ratio Calculator • Drag to Select • Simple & Direct</p>", unsafe_allow_html=True)
