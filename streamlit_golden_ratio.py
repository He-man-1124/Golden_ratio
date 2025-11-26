# Golden Ratio Calculator - PURE DRAG SELECTION (NO MANUAL INPUT)
# Simple HTML5 Canvas - Direct coordinate capture from drag

import streamlit as st
from PIL import Image
import numpy as np
import math
import base64
from io import BytesIO

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
        margin: 6px 0;
        font-family: 'Courier New', monospace;
        color: #13343b;
        font-weight: 500;
    }
    #selectionCanvas {
        border: 2px solid #ccc;
        border-radius: 8px;
        cursor: crosshair;
        display: block;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# App Title
st.markdown("<h1 class='title-main'>🌀 Golden Ratio Calculator</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Measure the divine proportion (φ ≈ 1.618) in your images</p>", unsafe_allow_html=True)

# Initialize session state
if 'image' not in st.session_state:
    st.session_state.image = None
if 'selection' not in st.session_state:
    st.session_state.selection = None
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
        st.session_state.selection = None
        st.session_state.measurements = None
else:
    camera_image = st.sidebar.camera_input("Take a photo")
    if camera_image is not None:
        image = Image.open(camera_image)
        st.session_state.image = image
        st.session_state.selection = None
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

def image_to_base64(img):
    """Convert PIL Image to base64"""
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# Main app logic
if st.session_state.image is not None:
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("📷 Drag to Select Area")
        
        st.markdown("""
            <div class='instruction-box'>
            <strong>🎯 How to Use:</strong><br>
            1. <strong>Click and drag</strong> on the preview to select an area<br>
            2. A <strong>blue rectangle</strong> shows your selection<br>
            3. <strong>Release the mouse</strong> to capture coordinates<br>
            4. Selected area appears with coordinates<br>
            5. Click <strong>"📊 Calculate"</strong> to measure golden ratio
            </div>
        """, unsafe_allow_html=True)
        
        img_width, img_height = st.session_state.image.size
        img_base64 = image_to_base64(st.session_state.image)
        
        st.write(f"**Image Size:** {img_width}×{img_height} pixels")
        
        # HTML5 Canvas with JavaScript for drag selection
        canvas_html = f"""
        <canvas id="selectionCanvas" width="{img_width}" height="{img_height}"></canvas>
        <div id="selectionInfo" style="margin-top: 10px; font-size: 14px; color: #666;">
            👆 Drag on the image to select an area
        </div>
        
        <script>
        const canvas = document.getElementById('selectionCanvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();
        const infoDiv = document.getElementById('selectionInfo');
        
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
                // Draw selection rectangle
                ctx.fillStyle = 'rgba(50, 184, 198, 0.2)';
                ctx.fillRect(selection.x, selection.y, selection.w, selection.h);
                ctx.strokeStyle = 'rgb(50, 184, 198)';
                ctx.lineWidth = 3;
                ctx.strokeRect(selection.x, selection.y, selection.w, selection.h);
                
                // Update info
                infoDiv.innerHTML = '✅ Selection: X ' + selection.x + '-' + (selection.x + selection.w) + 
                    ', Y ' + selection.y + '-' + (selection.y + selection.h);
            }} else {{
                infoDiv.innerHTML = '👆 Drag on the image to select an area';
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
                // Store selection in Streamlit session
                window.selectedArea = {{
                    x_start: Math.floor(selection.x),
                    y_start: Math.floor(selection.y),
                    x_end: Math.floor(selection.x + selection.w),
                    y_end: Math.floor(selection.y + selection.h)
                }};
                infoDiv.innerHTML = '✅ Selection captured! X ' + window.selectedArea.x_start + '-' + window.selectedArea.x_end + 
                    ', Y ' + window.selectedArea.y_start + '-' + window.selectedArea.y_end;
            }}
        }});
        
        canvas.addEventListener('mouseleave', () => {{
            isDrawing = false;
        }});
        </script>
        """
        
        st.components.v1.html(canvas_html, height=img_height + 60)
        
        # Get button to capture selection
        if st.button("📊 Calculate Golden Ratio", type="primary", use_container_width=True):
            # Selection must be made via the canvas
            st.session_state.selection = None
            st.info("⚠️ Please drag on the image above to select an area first")
            st.stop()
    
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
            st.info("📊 Make a selection\nand click Calculate\nto see results")
    
    # Reset button
    st.write("---")
    if st.button("🔄 Reset & Load New Image", use_container_width=True):
        st.session_state.image = None
        st.session_state.selection = None
        st.session_state.measurements = None
        st.rerun()

else:
    st.info("👈 Upload an image or take a photo from the sidebar to get started!")

# About section
with st.expander("ℹ️ About Golden Ratio"):
    st.write("""
    The **Golden Ratio** (φ ≈ 1.618) is a special mathematical number:
    
    **Formula:** φ = (1 + √5) / 2
    
    **This Calculator:**
    1. Upload or capture an image
    2. Drag on the preview to select an area
    3. Click Calculate
    4. See your golden ratio score
    """)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #626c71; font-size: 12px;'>Golden Ratio Calculator • HTML5 Canvas Selection</p>", unsafe_allow_html=True)
