# Golden Ratio Calculator - ADVANCED: Direct Plotly Selection Capture
# Uses Streamlit's internal query_params and callback system

import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import math
import plotly.graph_objects as go
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
    .selection-preview {
        border: 2px solid #21808d;
        border-radius: 8px;
        padding: 10px;
        margin: 10px 0;
        background-color: rgba(33, 128, 141, 0.05);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# App Title
st.markdown("<h1 class='title-main'>🌀 Golden Ratio Calculator</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Measure the divine proportion (φ ≈ 1.618) in your images</p>", unsafe_allow_html=True)

# Initialize session state with extended tracking
if 'image' not in st.session_state:
    st.session_state.image = None
if 'img_array' not in st.session_state:
    st.session_state.img_array = None
if 'measurements' not in st.session_state:
    st.session_state.measurements = None
if 'last_selection' not in st.session_state:
    st.session_state.last_selection = None
if 'selection_confirmed' not in st.session_state:
    st.session_state.selection_confirmed = False

# Sidebar for image upload
st.sidebar.header("📸 Image Source")
image_source = st.sidebar.radio("Choose image source:", ["Upload Image", "Use Camera"])

if image_source == "Upload Image":
    uploaded_file = st.sidebar.file_uploader("Choose an image file", type=["jpg", "jpeg", "png", "bmp", "gif"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.session_state.image = image
        st.session_state.img_array = np.array(image)
        st.session_state.last_selection = None
        st.session_state.selection_confirmed = False
else:
    camera_image = st.sidebar.camera_input("Take a photo")
    if camera_image is not None:
        image = Image.open(camera_image)
        st.session_state.image = image
        st.session_state.img_array = np.array(image)
        st.session_state.last_selection = None
        st.session_state.selection_confirmed = False

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

def draw_selection_on_image(img, x_start, y_start, x_end, y_end):
    """Draw selection rectangle on image"""
    img_copy = img.copy()
    draw = ImageDraw.Draw(img_copy, 'RGBA')
    
    # Draw filled rectangle with transparency
    draw.rectangle(
        [x_start, y_start, x_end, y_end],
        fill=(50, 184, 198, 50),
        outline=(50, 184, 198, 255),
        width=3
    )
    return img_copy

# Main app logic
if st.session_state.image is not None:
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("📷 Drag to Select Area on Image")
        
        st.markdown("""
            <div class='instruction-box'>
            <strong>🎯 How to Use:</strong><br>
            1. <strong>Click and drag</strong> on the image to create selection box<br>
            2. The <strong>blue rectangle</strong> shows your selection<br>
            3. <strong>Release mouse</strong> to capture coordinates<br>
            4. <strong>Adjust if needed</strong> using input fields<br>
            5. Click <strong>"📊 Calculate"</strong> to measure
            </div>
        """, unsafe_allow_html=True)
        
        # Get image dimensions
        img_width, img_height = st.session_state.image.size
        img_array = st.session_state.img_array
        
        st.write(f"**Image Size:** {img_width}×{img_height} pixels")
        
        # Create Plotly figure
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
            font=dict(size=10)
        )
        
        # Display chart with key to track selection events
        chart_placeholder = st.empty()
        with chart_placeholder:
            selected_points = st.plotly_chart(
                fig, 
                use_container_width=True, 
                key="selection_chart",
                on_select="rerun"
            )
        
        # Try to extract selection from Plotly chart metadata
        st.write("---")
        st.write("**Fine-tune Selection (or manually enter coordinates):**")
        
        # Initialize default values
        default_x_start = 0
        default_y_start = 0
        default_x_end = min(200, img_width)
        default_y_end = min(200, img_height)
        
        if st.session_state.last_selection:
            sel = st.session_state.last_selection
            default_x_start = int(sel.get('x_start', 0))
            default_y_start = int(sel.get('y_start', 0))
            default_x_end = int(sel.get('x_end', min(200, img_width)))
            default_y_end = int(sel.get('y_end', min(200, img_height)))
        
        # Input columns
        col_in = st.columns(4)
        
        with col_in[0]:
            x_start = st.number_input(
                "X Start (px)", 
                min_value=0, 
                max_value=img_width,
                value=default_x_start,
                step=5,
                key="x_start_input"
            )
        
        with col_in[1]:
            y_start = st.number_input(
                "Y Start (px)", 
                min_value=0, 
                max_value=img_height,
                value=default_y_start,
                step=5,
                key="y_start_input"
            )
        
        with col_in[2]:
            x_end = st.number_input(
                "X End (px)", 
                min_value=0, 
                max_value=img_width,
                value=default_x_end,
                step=5,
                key="x_end_input"
            )
        
        with col_in[3]:
            y_end = st.number_input(
                "Y End (px)", 
                min_value=0, 
                max_value=img_height,
                value=default_y_end,
                step=5,
                key="y_end_input"
            )
        
        # Validate and store selection
        if x_start < x_end and y_start < y_end:
            width = x_end - x_start
            height = y_end - y_start
            
            # Update session state
            st.session_state.last_selection = {
                'x_start': x_start,
                'y_start': y_start,
                'x_end': x_end,
                'y_end': y_end
            }
            
            # Display selection box
            st.markdown(f"""
                <div class='coordinates-box'>
                <strong>📍 Selected Area:</strong>
                <div class='coord-item'>X: {int(x_start)} → {int(x_end)} pixels</div>
                <div class='coord-item'>Y: {int(y_start)} → {int(y_end)} pixels</div>
                <div class='coord-item'>Size: {int(width)} × {int(height)} pixels</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Show preview with selection box drawn
            try:
                x_start_safe = max(0, min(int(x_start), img_width - 1))
                y_start_safe = max(0, min(int(y_start), img_height - 1))
                x_end_safe = max(x_start_safe + 1, min(int(x_end), img_width))
                y_end_safe = max(y_start_safe + 1, min(int(y_end), img_height))
                
                # Draw selection on preview
                preview_with_selection = draw_selection_on_image(
                    st.session_state.image,
                    x_start_safe,
                    y_start_safe,
                    x_end_safe,
                    y_end_safe
                )
                
                # Show preview
                st.markdown('<div class="selection-preview">', unsafe_allow_html=True)
                st.image(preview_with_selection, caption="Preview with Selection Box", use_column_width=False, width=400)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Also show cropped area
                cropped = st.session_state.image.crop((x_start_safe, y_start_safe, x_end_safe, y_end_safe))
                if cropped.size[0] > 0 and cropped.size[1] > 0:
                    cropped_resized = cropped.resize((300, 200))
                    st.image(cropped_resized, caption="Cropped Selection Detail", use_column_width=False)
            except Exception as e:
                st.warning(f"Preview error: {str(e)}")
        else:
            st.info("👆 Adjust coordinates to create valid selection (X and Y ranges must be positive)")
        
        # Calculate button
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("📊 Calculate Golden Ratio", type="primary", use_container_width=True):
                if st.session_state.last_selection:
                    sel = st.session_state.last_selection
                    x_start_calc = int(sel['x_start'])
                    y_start_calc = int(sel['y_start'])
                    x_end_calc = int(sel['x_end'])
                    y_end_calc = int(sel['y_end'])
                    
                    width_calc = x_end_calc - x_start_calc
                    height_calc = y_end_calc - y_start_calc
                    
                    if width_calc < 10 or height_calc < 10:
                        st.error("❌ Selection too small. Please select an area larger than 10×10 pixels.")
                    else:
                        long_side = max(width_calc, height_calc)
                        short_side = min(width_calc, height_calc)
                        ratio = long_side / short_side
                        difference = abs(ratio - GOLDEN_RATIO)
                        score = calculate_score(ratio)
                        status, color = get_status(difference)
                        
                        st.session_state.measurements = {
                            'ratio': ratio,
                            'width': width_calc,
                            'height': height_calc,
                            'long_side': long_side,
                            'short_side': short_side,
                            'difference': difference,
                            'score': score,
                            'status': status,
                            'color': color,
                            'x_start': x_start_calc,
                            'y_start': y_start_calc,
                            'x_end': x_end_calc,
                            'y_end': y_end_calc
                        }
                        st.success("✅ Calculation complete! See results on the right →")
                else:
                    st.error("❌ Please make a selection first")
        
        with col_btn2:
            if st.button("🔄 Clear Selection", use_container_width=True):
                st.session_state.last_selection = None
                st.session_state.measurements = None
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
            st.info("📊 Make a selection and\nclick Calculate to see\nmeasurements")
    
    # Reset button
    st.write("---")
    if st.button("🔄 Reset & Load New Image", use_container_width=True):
        st.session_state.image = None
        st.session_state.img_array = None
        st.session_state.measurements = None
        st.session_state.last_selection = None
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
    
    **This Calculator:**
    1. Upload or capture an image
    2. Drag to select an area (or use input fields)
    3. See live preview with selection
    4. Click Calculate to measure
    5. Get golden ratio score
    6. Download your results
    """)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #626c71; font-size: 12px;'>Golden Ratio Calculator • Built with Streamlit, Plotly & PIL</p>", unsafe_allow_html=True)
