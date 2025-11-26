# 1. Create project folder and virtual environment
mkdir golden-ratio-calculator && cd golden-ratio-calculator
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 2. Install dependencies
pip install streamlit pillow opencv-python numpy

# 3. Save the Python script as app.py and run
streamlit run app.py

# 4. Test at http://localhost:8501
