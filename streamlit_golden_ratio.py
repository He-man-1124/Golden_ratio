# Golden Ratio Calculator - Streamlit App with Drawable Canvas
# Install: pip install streamlit pillow numpy streamlit-drawable-canvas

import streamlit as st
from PIL import Image, ImageDraw
from streamlit_drawable_canvas import st_canvas
import numpy as np
import math

# Set page configuration
st.set_page_config(
    page_title="Golden Ratio Calculator",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define golden ratio constant
GOLDEN_RATIO = (1 + math.sqrt(5)) / 2  # ≈ 1.618

# Custom CSS styling
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
if 'original_image' not in st.session_state:
    st.session_state.original_image = None

# Sidebar for image upload
st.sidebar.header("📸 Image Source")
image_source = st.sidebar.radio("Choose image source:", ["Upload Image", "Use Camera"])

if image_source == "Upload Image":
    uploaded_file = st.sidebar.file_uploader("Choose an image file", type=["jpg", "jpeg", "png", "bmp", "gif"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.session_state.original_image = image
        st.session_state.image = np.array(image)
else:
    camera_image = st.sidebar.camera_input("Take a photo")
    if camera_image is not None:
        image = Image.open(camera_image)
        st.session_state.original_image = image
        st.session_state.image = np.array(image)

# Helper function to calculate score
def calculate_score(ratio):
    """Calculate golden ratio score (0-100)"""
    difference = abs(ratio - GOLDEN_RATIO)
    k = 3
    return round(100 * math.exp(-k * difference))

# Helper function to get status
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
    col1, col2 = st.columns([2.5, 1])
    
    with col1:
        st.subheader("📷 Tap & Drag to Select Area")
        
        st.markdown("""
            <div class='instruction-box'>
            <strong>🎯 How to Use:</strong><br>
            1. Click and drag on the image below to draw a rectangle<br>
            2. The selection will be highlighted with a blue box<br>
            3. Adjust until you're happy with the selection<br>
            4. Click "📊 Calculate Golden Ratio" to measure<br>
            <br>
            <strong>💡 Tips:</strong> You can adjust the stroke width and color using the options on the left
            </div>
        """, unsafe_allow_html=True)
        
        # Get image dimensions
        img_height, img_width = st.session_state.image.shape[:2]
        
        # Create drawable canvas
        st.write("**Draw a rectangle on the image to select the area:**")
        
        canvas_result = st_canvas(
            fill_color="rgba(50, 184, 198, 0.2)",
            stroke_width=3,
            stroke_color="rgb(50, 184, 198)",
            background_image=Image.fromarray(st.session_state.image.astype('uint8')),
            height=img_height,
            width=img_width,
            drawing_mode="rect",
            key="canvas",
        )
        
        # Extract coordinates from canvas
        if canvas_result.json_data is not None:
            objects = canvas_result.json_data["objects"]
            
            if len(objects) > 0:
                # Get the last rectangle drawn
                rect = objects[-1]
                
                x_start = int(rect["left"])
                y_start = int(rect["top"])
                x_end = int(rect["left"] + rect["width"])
                y_end = int(rect["top"] + rect["height"])
                
                # Display selected coordinates
                st.write(f"**Selection Coordinates:** X({x_start}, {x_end}) Y({y_start}, {y_end})")
                
                # Calculate button
                if st.button("📊 Calculate Golden Ratio", type="primary", use_container_width=True):
                    width = abs(x_end - x_start)
                    height = abs(y_end - y_start)
                    
                    if width < 10 or height < 10:
                        st.error("❌ Selection too small. Please draw a larger selection.")
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
                        st.success("✅ Calculation complete!")
            else:
                st.info("👆 Draw a rectangle on the image to select an area")
        else:
            st.info("👆 Draw a rectangle on the image to select an area")
    
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
                    <strong>Ratio:</strong> {m['ratio']:.4f}
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class='metric-box'>
                    <strong>Size:</strong> {int(m['long_side'])} × {int(m['short_side'])} px
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class='metric-box'>
                    <strong>Difference:</strong> {m['difference']:.4f}
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class='metric-box'>
                    <strong>φ:</strong> {GOLDEN_RATIO:.4f}
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
            st.info("Draw on the image and calculate to see results")
    
    # Reset button
    st.write("---")
    if st.button("🔄 Reset & Load New Image", use_container_width=True):
        st.session_state.image = None
        st.session_state.measurements = None
        st.session_state.original_image = None
        st.rerun()

else:
    st.info("👈 Upload an image or take a photo from the sidebar to get started!")

# About section
with st.expander("ℹ️ About Golden Ratio"):
    st.write("""
    The **Golden Ratio** (φ ≈ 1.618) is a special mathematical number:
    
    - **Formula:** φ = (1 + √5) / 2
    - **Found in Nature:** Flower petals, seashells, spiral galaxies
    - **Used in Art:** Renaissance paintings, modern design, photography
    - **Why it matters:** Rectangles with this ratio are aesthetically pleasing
    
    **How to use:**
    1. Upload or capture an image
    2. Draw a rectangle on the image by clicking and dragging
    3. Click "Calculate Golden Ratio"
    4. See how close your selection is to φ (0-100 scale)
    """)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #626c71; font-size: 12px;'>Golden Ratio Calculator • Built with Streamlit & Drawable Canvas</p>", unsafe_allow_html=True)
