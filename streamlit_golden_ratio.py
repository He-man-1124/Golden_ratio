# Golden Ratio Calculator - Streamlit App with Custom HTML5 Canvas
# Drag directly on image to select area

import streamlit as st
from PIL import Image, ImageDraw
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

# Custom CSS and JavaScript
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
    #canvas-container {
        position: relative;
        display: inline-block;
        border: 2px solid #ccc;
        border-radius: 8px;
        overflow: hidden;
    }
    #canvas {
        display: block;
        cursor: crosshair;
        background: white;
    }
    .canvas-info {
        font-size: 12px;
        color: #666;
        margin-top: 10px;
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
    """Convert PIL Image to base64 string"""
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# Main app logic
if st.session_state.image is not None:
    col1, col2 = st.columns([2.5, 1])
    
    with col1:
        st.subheader("📷 Click & Drag to Select Area")
        
        st.markdown("""
            <div class='instruction-box'>
            <strong>🎯 How to Use:</strong><br>
            1. Click on the image and drag to draw a rectangle<br>
            2. The blue box shows your selection<br>
            3. Release the mouse to finalize<br>
            4. Click "📊 Calculate Golden Ratio" to measure
            </div>
        """, unsafe_allow_html=True)
        
        # Get image dimensions
        img_width, img_height = st.session_state.image.size
        
        # Convert image to base64
        img_base64 = image_to_base64(st.session_state.image)
        
        st.write(f"**Image Size:** {img_width}×{img_height} pixels")
        
        # Create custom HTML5 canvas
        canvas_html = f"""
        <div id="canvas-container">
            <canvas id="canvas" width="{img_width}" height="{img_height}"></canvas>
        </div>
        <div class="canvas-info">Coordinates: <span id="coords">Drag to select area</span></div>
        
        <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();
        
        let isDrawing = false;
        let startX = 0;
        let startY = 0;
        let selection = null;
        
        // Load the image
        img.onload = function() {{
            ctx.drawImage(img, 0, 0);
        }};
        img.src = 'data:image/png;base64,{img_base64}';
        
        function redraw() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0);
            
            if (selection) {{
                // Draw selection rectangle
                ctx.strokeStyle = 'rgb(50, 184, 198)';
                ctx.lineWidth = 3;
                ctx.fillStyle = 'rgba(50, 184, 198, 0.2)';
                ctx.fillRect(selection.x, selection.y, selection.w, selection.h);
                ctx.strokeRect(selection.x, selection.y, selection.w, selection.h);
                
                // Update coordinates display
                document.getElementById('coords').textContent = 
                    'X: ' + selection.x + '-' + (selection.x + selection.w) + 
                    ', Y: ' + selection.y + '-' + (selection.y + selection.h);
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
        
        canvas.addEventListener('mouseup', (e) => {{
            isDrawing = false;
            if (selection && selection.w > 0 && selection.h > 0) {{
                // Save selection to Streamlit
                const coords = {{
                    x_start: selection.x,
                    y_start: selection.y,
                    x_end: selection.x + selection.w,
                    y_end: selection.y + selection.h
                }};
                window.selection_data = coords;
            }}
        }});
        
        canvas.addEventListener('mouseleave', () => {{
            isDrawing = false;
        }});
        </script>
        """
        
        st.components.v1.html(canvas_html, height=img_height + 60)
        
        # Get selection from JavaScript using a hidden container
        selection_data = st.session_state.get('selection')
        
        # Button to capture selection
        col_button1, col_button2 = st.columns(2)
        
        with col_button1:
            if st.button("📊 Calculate Golden Ratio", type="primary", use_container_width=True):
                # Use JavaScript to get coordinates via hidden input
                selection_html = """
                <div id="selection-capture">
                    <input type="hidden" id="selection-coords" value="">
                </div>
                <script>
                    if (window.selection_data) {
                        document.getElementById('selection-coords').value = JSON.stringify(window.selection_data);
                    }
                </script>
                """
                st.components.v1.html(selection_html, height=50)
                
                # For now, show info message
                st.info("📍 Please draw a selection on the image first!")
        
        with col_button2:
            if st.button("🔄 Clear Selection", use_container_width=True):
                st.session_state.selection = None
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
            st.info("📊 Draw on the image to see results")
    
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
    
    **How to use this calculator:**
    1. Upload or capture an image
    2. Drag a rectangle on the image
    3. See how close it is to φ
    4. Score: 0-100 (100 = perfect)
    """)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #626c71; font-size: 12px;'>Golden Ratio Calculator • Built with Streamlit & HTML5 Canvas</p>", unsafe_allow_html=True)
