# Image to Word Converter

A production-ready desktop application that converts images (JPG/PNG) into formatted Word documents (.docx) using Microsoft TrOCR technology with layout preservation.

## Features

- 🖼️ **Image Support**: JPG, PNG, BMP, TIFF formats
- 🔍 **Advanced OCR**: Powered by Microsoft TrOCR (Transformer-based OCR)
- ✍️ **Handwriting Support**: Excellent recognition for both handwritten and printed text
- 📄 **Layout Preservation**: Maintains paragraphs, lines, and basic formatting
- 🎨 **Modern UI**: Clean, dark-themed interface built with CustomTkinter
- ⚙️ **Image Preprocessing**: Optional deskewing, noise removal, and thresholding
- 📊 **Progress Tracking**: Real-time conversion progress feedback
- 💾 **Direct Export**: Save and open Word documents directly from the app

## Prerequisites

### Python Requirements

Python 3.8 or higher is required.

**Note:** No external OCR software installation needed! TrOCR model will be downloaded automatically on first run (~500MB).

## Installation

1. **Clone or download this repository**

2. **Navigate to the project directory**
   ```powershell
   cd "e:\University\PPIT"
   ```

3. **Install Python dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

Simply run the main script:

```powershell
python main.py
```

### Using the Application

1. **Browse Image**: Click the "Browse Image" button to select an image file
2. **Preview**: The selected image will be displayed in the preview panel
3. **Configure**: Enable/disable image preprocessing as needed
4. **Convert**: Click "Convert to Word" and choose where to save the output
5. **Open Document**: After conversion, click "Open Word Document" to view the result

## Project Structure

```
PPIT/
├── main.py                      # Entry point
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── core/
│   ├── __init__.py
│   └── ocr_engine.py           # OCR conversion logic
├── utils/
│   ├── __init__.py
│   └── image_processing.py     # Image preprocessing functions
└── gui/
    ├── __init__.py
    └── app.py                  # GUI application
```

## Technical Details

### Microsoft TrOCR
This application uses Microsoft's TrOCR (Transformer-based OCR) model:
- **Model**: `microsoft/trocr-base-handwritten`
- **Architecture**: Vision Transformer (ViT) + Transformer decoder
- **Capabilities**: Excellent for both handwritten and printed text
- **First Run**: Model will be downloaded automatically (~500MB)

### Image Preprocessing Pipeline (Optional)
1. **Grayscale Conversion**: Convert to single-channel image
2. **Deskewing**: Detect and correct image rotation
3. **Noise Removal**: Apply Non-Local Means Denoising
4. **Thresholding**: Use Otsu's method for binary conversion

### OCR Process
1. **Region Detection**: Use OpenCV to detect text regions
2. **Text Extraction**: Process each region with TrOCR transformer model
3. **Layout Reconstruction**: Preserve paragraph structure based on spatial positioning
4. **Document Generation**: Create formatted Word document with proper spacing

### Word Document Generation
- Paragraphs are created based on vertical spacing between text regions
- Font: Calibri 11pt (default)
- Margins: 1 inch on all sides
- Proper line breaks and spacing preserved

## Configuration

### TrOCR Model Selection
You can change the TrOCR model in `core/ocr_engine.py`:

```python
# For handwritten text (current default)
TROCR_MODEL_NAME = "microsoft/trocr-base-handwritten"

# For better quality (slower, requires more memory)
TROCR_MODEL_NAME = "microsoft/trocr-large-handwritten"

# For printed text only (faster)
TROCR_MODEL_NAME = "microsoft/trocr-base-printed"
```

## Troubleshooting

### Model Download Issues
- First run requires internet connection to download TrOCR model (~500MB)
- If download fails, check your internet connection and try again
- Model is cached locally after first download

### Poor OCR Quality for Handwriting
- Ensure handwriting is clear and legible
- Try different lighting or scan quality
- For very messy handwriting, results may vary
- Consider using the `trocr-large-handwritten` model for better accuracy

### Slow Performance
- TrOCR is computationally intensive, especially without GPU
- First run will be slower due to model download
- With CUDA-capable GPU, performance is significantly faster
- Consider using the base model instead of large for faster results

### Memory Issues
- TrOCR requires significant RAM (~2-4GB)
- Close other applications if you encounter memory errors
- Use base model instead of large if memory is limited

## Dependencies

- **customtkinter** (>=5.2.0): Modern UI framework
- **transformers** (>=4.30.0): Hugging Face transformers for TrOCR
- **torch** (>=2.0.0): PyTorch deep learning framework
- **python-docx** (>=1.1.0): Word document creation
- **opencv-python** (>=4.8.0): Image processing and region detection
- **Pillow** (>=10.4.0): Image handling
- **numpy** (>=1.26.0): Numerical operations

## GPU Support

For significantly faster OCR processing, install PyTorch with CUDA support:

```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

The application will automatically use GPU if available.

## License

This project is for educational purposes (PPIT University Project).

## Support

For issues or questions, please refer to:
- [TrOCR Paper](https://arxiv.org/abs/2109.10282)
- [Hugging Face TrOCR Models](https://huggingface.co/microsoft/trocr-base-handwritten)
- [Python-DOCX Documentation](https://python-docx.readthedocs.io/)
- [CustomTkinter Documentation](https://customtkinter.tomschimansky.com/)
