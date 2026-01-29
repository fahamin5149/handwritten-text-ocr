# Image to Word Converter - Streamlit Edition

A modern web-based application that converts images (JPG/PNG) containing text into formatted Word documents using Microsoft TrOCR.

## Features

- ✍️ **Handwritten Text Recognition** - Accurately extracts handwritten text
- 🖨️ **Printed Text Support** - Works with printed documents
- 📐 **Layout Preservation** - Maintains document structure
- 🎯 **High Accuracy** - Powered by Microsoft TrOCR
- 🌐 **Web Interface** - Modern, responsive Streamlit UI
- 💾 **Direct Download** - Download converted documents instantly

## Installation

1. **Clone or download the project**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python main.py
```

Or directly with Streamlit:
```bash
streamlit run gui/streamlit_app.py
```

## Usage

1. **Access the web interface** - The app will open in your default browser
2. **Upload an image** - Choose a JPG, PNG, or other supported format
3. **Configure options** - Optionally enable image preprocessing
4. **Convert** - Click "Convert to Word"
5. **Download** - Download your generated Word document

## Supported File Formats

- **Input:** PNG, JPG, JPEG, BMP, TIFF
- **Output:** DOCX (Microsoft Word)

## Requirements

- Python 3.8+
- Streamlit 1.32+
- PyTorch 2.0+
- Transformers 4.30+
- OpenCV
- Python-DOCX
- Pillow

## Technical Details

### Models Used
- **TrOCR Base Handwritten** - Microsoft's transformer-based OCR model
- Can be switched to printed text model by modifying `core/ocr_engine.py`

### Processing Pipeline
1. Image upload and validation
2. Text region detection using OpenCV
3. Text extraction with TrOCR
4. Document generation with formatting
5. Download ready Word document

## Project Structure

```
PPIT/
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── core/
│   ├── __init__.py
│   └── ocr_engine.py         # OCR conversion logic
├── gui/
│   ├── __init__.py
│   ├── streamlit_app.py      # Streamlit web interface (NEW)
│   └── app.py                # Original CustomTkinter GUI (deprecated)
└── utils/
    ├── __init__.py
    └── image_processing.py   # Image preprocessing utilities
```

## Migration from CustomTkinter

This version replaces the CustomTkinter desktop GUI with a modern Streamlit web interface. Key changes:

- **No desktop installation** - Runs in web browser
- **Responsive design** - Works on desktop and mobile
- **Easier deployment** - Can be hosted on Streamlit Cloud
- **Better UX** - Drag-and-drop file upload, instant download

## Troubleshooting

### Model Download Issues
The TrOCR model will be downloaded automatically on first run (requires internet connection). The model is ~1GB in size.

### CUDA/GPU Support
The application will automatically use GPU if available for faster processing. CPU mode works fine for most use cases.

### Memory Issues
For very large images, consider:
- Resizing the image before upload
- Using the printed text model (smaller)
- Ensuring sufficient RAM (4GB+ recommended)

## License

Educational project - PPIT University

## Credits

- Microsoft TrOCR for OCR capabilities
- Streamlit for the web framework
- Python-DOCX for document generation
