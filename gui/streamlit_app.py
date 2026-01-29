"""
Modern Streamlit Web Application for Image to Word conversion.
Built with Streamlit for a clean, modern web interface.
"""

import os
import sys
from typing import Optional
import streamlit as st
from PIL import Image
import tempfile
import subprocess

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.ocr_engine import OCRConverter


def init_session_state():
    """Initialize session state variables."""
    if 'ocr_converter' not in st.session_state:
        with st.spinner("Loading TrOCR model... This may take a moment on first run."):
            try:
                st.session_state.ocr_converter = OCRConverter()
            except RuntimeError as e:
                st.error(f"❌ TrOCR Model Error: {str(e)}")
                st.stop()
    
    if 'output_file_path' not in st.session_state:
        st.session_state.output_file_path = None


def display_header():
    """Display the application header."""
    st.title("📄 Image to Word Converter")
    st.markdown("**Convert JPG/PNG images to formatted Word documents**")
    st.markdown("---")


def display_image_preview(uploaded_file):
    """Display the uploaded image preview."""
    try:
        image = Image.open(uploaded_file)
        
        # Display image with max width
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        # Display file info
        file_size = len(uploaded_file.getvalue()) / 1024  # KB
        st.info(f"📄 **Filename:** {uploaded_file.name}  \n💾 **Size:** {file_size:.1f} KB")
        
        return image
    except Exception as e:
        st.error(f"Failed to load image: {str(e)}")
        return None


def perform_conversion(uploaded_file, preprocess: bool):
    """Perform the OCR conversion."""
    try:
        # Create temporary files for input and output
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_input:
            tmp_input.write(uploaded_file.getvalue())
            tmp_input_path = tmp_input.name
        
        # Generate output filename
        output_filename = os.path.splitext(uploaded_file.name)[0] + ".docx"
        tmp_output_path = os.path.join(tempfile.gettempdir(), output_filename)
        
        # Progress tracking
        progress_bar = st.progress(0, text="Starting conversion...")
        status_placeholder = st.empty()
        
        def update_status(message):
            """Update conversion status."""
            status_placeholder.info(f"🔄 {message}")
            # Update progress bar based on message
            if "Loading" in message:
                progress_bar.progress(20, text=message)
            elif "Detecting" in message:
                progress_bar.progress(40, text=message)
            elif "Extracting" in message:
                progress_bar.progress(60, text=message)
            elif "Creating" in message:
                progress_bar.progress(80, text=message)
            elif "Complete" in message:
                progress_bar.progress(100, text=message)
        
        # Perform conversion
        success = st.session_state.ocr_converter.convert_image_to_docx(
            tmp_input_path,
            tmp_output_path,
            preprocess=preprocess,
            progress_callback=update_status
        )
        
        # Clean up input temp file
        os.unlink(tmp_input_path)
        
        if success:
            st.session_state.output_file_path = tmp_output_path
            progress_bar.progress(100, text="✅ Conversion complete!")
            status_placeholder.success("✅ **Conversion successful!**")
            return tmp_output_path, output_filename
        else:
            status_placeholder.error("❌ Conversion failed")
            return None, None
            
    except Exception as e:
        st.error(f"❌ **Conversion Failed:** {str(e)}")
        return None, None


def main():
    """Main application entry point."""
    # Page configuration
    st.set_page_config(
        page_title="Image to Word Converter",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    init_session_state()
    
    # Display header
    display_header()
    
    # Create two-column layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📷 Image Preview")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=["png", "jpg", "jpeg", "bmp", "tiff"],
            help="Upload a JPG or PNG image containing text"
        )
        
        if uploaded_file is not None:
            # Display image preview
            image = display_image_preview(uploaded_file)
        else:
            st.info("👆 Please upload an image to get started")
    
    with col2:
        st.header("⚙️ Controls")
        
        # Preprocessing option
        preprocess = st.checkbox(
            "Enable Image Preprocessing",
            value=False,
            help="Apply image enhancement (deskewing, noise removal). Generally not needed for TrOCR."
        )
        
        st.markdown("---")
        
        # Convert button
        if uploaded_file is not None:
            if st.button("🔄 Convert to Word", type="primary", use_container_width=True):
                with st.spinner("Converting..."):
                    output_path, output_filename = perform_conversion(uploaded_file, preprocess)
                    
                    if output_path and os.path.exists(output_path):
                        # Provide download button
                        with open(output_path, "rb") as file:
                            st.download_button(
                                label="📥 Download Word Document",
                                data=file,
                                file_name=output_filename,
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                use_container_width=True
                            )
        else:
            st.button("🔄 Convert to Word", disabled=True, use_container_width=True)
            st.caption("Upload an image first to enable conversion")
    
    # Sidebar with information
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This application converts images containing text into formatted Word documents.
        
        **Features:**
        - ✍️ Supports handwritten text
        - 🖨️ Supports printed text
        - 📐 Layout preservation
        - 🎯 High accuracy with Microsoft TrOCR
        
        **Supported Formats:**
        - PNG, JPG, JPEG
        - BMP, TIFF
        
        **How to Use:**
        1. Upload an image file
        2. (Optional) Enable preprocessing
        3. Click "Convert to Word"
        4. Download the generated document
        """)
        
        st.markdown("---")
        st.caption("Powered by Microsoft TrOCR & Python-DOCX")
    
    # Footer
    st.markdown("---")
    st.caption("PPIT Project | January 2026")


if __name__ == "__main__":
    main()
