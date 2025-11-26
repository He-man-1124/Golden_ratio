# 🌀 Golden Ratio Calculator

A beautiful and intuitive Streamlit web application to measure the divine proportion (φ ≈ 1.618) in images. Perfect for exploring the golden ratio in nature, art, architecture, and photography!

## ✨ Features

- 📸 **Multiple Input Options**
  - Upload images from your device
  - Capture photos using your camera in real-time
  
- 📐 **Precise Measurements**
  - Manual pixel-based area selection
  - Simple x,y coordinate input system
  - Real-time calculations
  
- 🎯 **Golden Ratio Analysis**
  - Calculates how close your selection is to φ (1.618)
  - Score system (0-100)
  - Visual status indicators (Excellent, Good, Fair, Not Close)
  
- 📊 **Detailed Results**
  - Measured ratio
  - Pixel dimensions
  - Difference from φ
  - Color-coded score display
  
- ⬇️ **Export Results**
  - Download measurements as text file
  - Easy sharing and documentation

## 🚀 Live Demo

[**Try the Golden Ratio Calculator**](https://golden-ratio-calculator-YOUR_USERNAME.streamlit.app)

*(Replace YOUR_USERNAME with your actual GitHub username)*

## 🔬 About the Golden Ratio

The **golden ratio** (φ ≈ 1.618033988749...) is a special mathematical number with remarkable properties:

- **Formula:** φ = (1 + √5) / 2
- **Found in Nature:** Flower petals, seashells, spiral galaxies, human body proportions
- **Used in Art & Design:** Renaissance paintings, modern architecture, graphic design
- **Aesthetic Appeal:** Rectangles with this ratio are considered naturally pleasing to the eye

This calculator helps you discover golden ratio proportions in any image!

## 💻 Local Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/golden-ratio-calculator.git
cd golden-ratio-calculator

# 2. Create a virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
streamlit run app.py
```

The app will automatically open at `http://localhost:8501`

## 📖 How to Use

### Step 1: Choose Your Image Source
- **Upload Image:** Select an image file from your device (JPG, PNG, BMP, GIF)
- **Use Camera:** Capture a live photo using your device camera

### Step 2: Select Area to Measure
- Use the number inputs to specify pixel coordinates
  - X Start: Starting x-coordinate
  - Y Start: Starting y-coordinate
  - X End: Ending x-coordinate
  - Y End: Ending y-coordinate

### Step 3: Calculate
- Click the "📊 Calculate Golden Ratio" button
- Minimum selection size: 10×10 pixels

### Step 4: View Results
- **Golden Ratio Score:** 0-100 scale (100 = perfect match)
- **Status:** Visual indicator of how close to φ
- **Measurements:** Exact dimensions and ratio values

### Step 5: Download (Optional)
- Click "⬇️ Download Results" to save measurements as a text file

## 🛠️ Technology Stack

- **Framework:** [Streamlit](https://streamlit.io) - Fast web app framework for Python
- **Image Processing:** Pillow, OpenCV
- **Numerical Computing:** NumPy
- **Language:** Python 3.8+

## 📁 Project Structure

```
golden-ratio-calculator/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python package dependencies
├── .gitignore               # Git ignore rules
├── README.md                # This file
└── .streamlit/              # Streamlit configuration (optional)
```

## 🔧 Configuration

### Optional: Customize Streamlit Settings

Create a `.streamlit/config.toml` file:

```toml
[theme]
primaryColor = "#21808d"
backgroundColor = "#fcfcf9"
secondaryBackgroundColor = "#fffffd"
textColor = "#13343b"
font = "sans serif"

[server]
maxUploadSize = 200
enableXsrfProtection = true
```

## 📊 Understanding Your Results

| Score Range | Status | Interpretation |
|-------------|--------|-----------------|
| 95-100 | ✨ Excellent | Perfect golden ratio match |
| 85-94 | 👍 Good | Very close to φ |
| 70-84 | 📐 Fair | Moderately close to φ |
| Below 70 | 📏 Not Close | Significantly different from φ |

## 🚀 Deployment

### Deploy to Streamlit Cloud (Recommended)

1. Push your code to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Click "New app"
4. Select your repository, branch (`main`), and file (`app.py`)
5. Click "Deploy"

Your app will be live at: `https://golden-ratio-calculator-YOUR_USERNAME.streamlit.app`

### Other Deployment Options

- **Heroku:** Traditional cloud hosting with more control
- **AWS:** Scalable infrastructure
- **DigitalOcean:** Simple VPS deployment
- **PythonAnywhere:** Beginner-friendly Python hosting

See `deployment_guide.md` for detailed instructions.

## 🐛 Troubleshooting

### Camera not working
- Ensure you're using HTTPS (automatically used by Streamlit Cloud)
- Allow camera permissions in your browser
- Try in a different browser if issues persist

### Module not found error
```bash
pip install --upgrade -r requirements.txt
```

### App crashes with large images
- Streamlit Cloud has a 200MB upload limit
- Use smaller image files

### Selection too small error
- Minimum selection size is 10×10 pixels
- Draw a larger selection area

## 🎓 Learning Resources

- **Mathematics:**
  - [Golden Ratio on Wikipedia](https://en.wikipedia.org/wiki/Golden_ratio)
  - [Phi and Fibonacci](https://en.wikipedia.org/wiki/Fibonacci_number)

- **Development:**
  - [Streamlit Documentation](https://docs.streamlit.io)
  - [OpenCV Tutorials](https://docs.opencv.org)
  - [Python Pillow Guide](https://pillow.readthedocs.io)

## 🤝 Contributing

Found a bug or want to add features? Contributions welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the **MIT License** - see LICENSE file for details.

### MIT License Summary
- ✅ Use commercially
- ✅ Modify the code
- ✅ Distribute
- ✅ Use privately
- ⚠️ Include license and copyright notice
- ⚠️ No liability

## 👤 Author & Contact

Created with ❤️ using [Streamlit](https://streamlit.io)

**GitHub:** [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)

**Email:** your.email@example.com

---

## 🌟 Support

If you found this project helpful, please consider:
- ⭐ Starring the repository
- 🐦 Sharing on social media
- 💬 Giving feedback and suggestions
- 🐛 Reporting bugs and issues

## 📈 Version History

**Version 1.0** (Nov 2025)
- Initial release
- Camera capture feature
- Image upload functionality
- Golden ratio calculation
- Score and analysis display
- Results export

## 🎯 Roadmap

Planned features for future versions:
- [ ] Batch image processing
- [ ] Automatic golden ratio detection (AI)
- [ ] Advanced image filters
- [ ] Export to PDF with detailed analysis
- [ ] Multi-language support
- [ ] Mobile app version
- [ ] Historical results tracking

## 📞 FAQ

**Q: What's the golden ratio exactly?**
A: It's approximately 1.618, written as φ (phi). It appears frequently in nature and is considered aesthetically pleasing.

**Q: Can I use this commercially?**
A: Yes! The MIT license allows commercial use. Just include a attribution.

**Q: Is my data stored?**
A: No. Your images and measurements are processed locally and never stored on servers.

**Q: Can I deploy this myself?**
A: Yes! See the deployment section. You can use Streamlit Cloud (free), Heroku, AWS, or your own server.

**Q: How accurate is the calculation?**
A: Accuracy depends on your selection precision. Measurements are pixel-perfect from your input coordinates.

---

**Made with 🎨 for mathematicians, designers, and curious minds everywhere**

Last updated: November 26, 2025
