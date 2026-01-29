"""
Modern GUI application for Image to Word conversion.
Built with CustomTkinter for a clean, modern interface.
"""

import os
import sys
import threading
from tkinter import filedialog, messagebox
from typing import Optional
import customtkinter as ctk
from PIL import Image, ImageTk
import subprocess

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.ocr_engine import OCRConverter


class ImageToWordApp:
    """Main application class for the Image to Word converter."""
    
    def __init__(self):
        """Initialize the application."""
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Image to Word Converter")
        self.root.geometry("900x700")
        
        # Instance variables
        self.selected_image_path: Optional[str] = None
        self.output_file_path: Optional[str] = None
        self.ocr_converter: Optional[OCRConverter] = None
        self.preview_image: Optional[ImageTk.PhotoImage] = None
        
        # Initialize OCR converter (TrOCR will load on startup)
        try:
            self.status_label = None  # Will be set in UI
            self.ocr_converter = OCRConverter()
        except RuntimeError as e:
            messagebox.showerror("TrOCR Model Error", str(e))
            self.root.destroy()
            sys.exit(1)
        
        # Build UI
        self._create_ui()
        
    def _create_ui(self):
        """Create the user interface."""
        # Title
        title_label = ctk.CTkLabel(
            self.root,
            text="📄 Image to Word Converter",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            self.root,
            text="Convert JPG/PNG images to formatted Word documents",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Main content frame
        content_frame = ctk.CTkFrame(self.root)
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Left panel - Image preview
        left_panel = ctk.CTkFrame(content_frame)
        left_panel.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)
        
        preview_label = ctk.CTkLabel(
            left_panel,
            text="Image Preview",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        preview_label.pack(pady=10)
        
        # Image display area
        self.image_display = ctk.CTkLabel(
            left_panel,
            text="No image selected",
            width=400,
            height=400,
            fg_color="gray20",
            corner_radius=10
        )
        self.image_display.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Right panel - Controls
        right_panel = ctk.CTkFrame(content_frame, width=300)
        right_panel.pack(side="right", fill="y", padx=(5, 10), pady=10)
        right_panel.pack_propagate(False)
        
        controls_label = ctk.CTkLabel(
            right_panel,
            text="Controls",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        controls_label.pack(pady=15)
        
        # Browse button
        self.browse_btn = ctk.CTkButton(
            right_panel,
            text="📂 Browse Image",
            command=self._browse_image,
            width=250,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.browse_btn.pack(pady=10)
        
        # File info
        self.file_info_label = ctk.CTkLabel(
            right_panel,
            text="No file selected",
            wraplength=250,
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.file_info_label.pack(pady=10)
        
        # Separator
        separator = ctk.CTkFrame(right_panel, height=2, fg_color="gray30")
        separator.pack(fill="x", padx=20, pady=20)
        
        # Preprocessing option
        self.preprocess_var = ctk.CTkCheckBox(
            right_panel,
            text="Enable Image Preprocessing",
            font=ctk.CTkFont(size=12)
        )
        self.preprocess_var.pack(pady=10)
        # Disabled by default for TrOCR (works better with raw images)
        
        # Convert button
        self.convert_btn = ctk.CTkButton(
            right_panel,
            text="🔄 Convert to Word",
            command=self._start_conversion,
            width=250,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            state="disabled"
        )
        self.convert_btn.pack(pady=20)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(right_panel, width=250)
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            right_panel,
            text="Ready",
            font=ctk.CTkFont(size=12),
            wraplength=250
        )
        self.status_label.pack(pady=10)
        
        # Open output button (initially hidden)
        self.open_output_btn = ctk.CTkButton(
            right_panel,
            text="📖 Open Word Document",
            command=self._open_output_file,
            width=250,
            height=40,
            font=ctk.CTkFont(size=13),
            fg_color="green",
            hover_color="darkgreen"
        )
        # Don't pack yet - will show after conversion
        
        # Footer
        footer_label = ctk.CTkLabel(
            self.root,
            text="Powered by Microsoft TrOCR & Python-DOCX | Supports Handwritten & Printed Text",
            font=ctk.CTkFont(size=10),
            text_color="gray50"
        )
        footer_label.pack(side="bottom", pady=10)
        
    def _browse_image(self):
        """Open file dialog to select an image."""
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.selected_image_path = file_path
            self._display_image(file_path)
            self._update_file_info(file_path)
            self.convert_btn.configure(state="normal")
            self.status_label.configure(text="Image loaded successfully")
            
            # Hide open output button if visible
            self.open_output_btn.pack_forget()
    
    def _display_image(self, image_path: str):
        """Display the selected image in the preview area."""
        try:
            # Load and resize image
            image = Image.open(image_path)
            
            # Calculate aspect ratio and resize
            display_width = 400
            display_height = 400
            
            img_width, img_height = image.size
            aspect_ratio = img_width / img_height
            
            if aspect_ratio > 1:
                # Landscape
                new_width = display_width
                new_height = int(display_width / aspect_ratio)
            else:
                # Portrait
                new_height = display_height
                new_width = int(display_height * aspect_ratio)
            
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            self.preview_image = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(new_width, new_height)
            )
            
            self.image_display.configure(image=self.preview_image, text="")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image:\n{str(e)}")
    
    def _update_file_info(self, file_path: str):
        """Update the file information label."""
        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path) / 1024  # Convert to KB
        
        info_text = f"📄 {filename}\n💾 {file_size:.1f} KB"
        self.file_info_label.configure(text=info_text)
    
    def _start_conversion(self):
        """Start the conversion process in a background thread."""
        if not self.selected_image_path:
            messagebox.showwarning("No Image", "Please select an image first.")
            return
        
        # Ask for output file location
        default_name = os.path.splitext(os.path.basename(self.selected_image_path))[0] + ".docx"
        output_path = filedialog.asksaveasfilename(
            title="Save Word Document As",
            defaultextension=".docx",
            initialfile=default_name,
            filetypes=[("Word Document", "*.docx"), ("All files", "*.*")]
        )
        
        if not output_path:
            return
        
        self.output_file_path = output_path
        
        # Disable buttons during conversion
        self.browse_btn.configure(state="disabled")
        self.convert_btn.configure(state="disabled")
        self.open_output_btn.pack_forget()
        
        # Start progress animation
        self.progress_bar.set(0)
        self.status_label.configure(text="Converting... Please wait")
        
        # Run conversion in background thread
        thread = threading.Thread(target=self._perform_conversion, daemon=True)
        thread.start()
        
        # Start progress animation
        self._animate_progress()
    
    def _perform_conversion(self):
        """Perform the actual OCR conversion (runs in background thread)."""
        try:
            preprocess = self.preprocess_var.get() == 1
            
            # Define progress callback
            def update_status(message):
                self.root.after(0, lambda: self.status_label.configure(text=message))
            
            success = self.ocr_converter.convert_image_to_docx(
                self.selected_image_path,
                self.output_file_path,
                preprocess=preprocess,
                progress_callback=update_status
            )
            
            if success:
                self.root.after(0, self._conversion_success)
            else:
                self.root.after(0, self._conversion_failed, "Conversion failed")
                
        except Exception as e:
            self.root.after(0, self._conversion_failed, str(e))
    
    def _animate_progress(self):
        """Animate the progress bar during conversion."""
        current_value = self.progress_bar.get()
        
        # Continue animating but slow down as we approach 1.0
        if current_value < 0.98:
            # Exponential slowdown for smoother appearance
            increment = 0.01 * (1 - current_value)
            new_value = current_value + increment
            self.progress_bar.set(new_value)
            self.root.after(100, self._animate_progress)
    
    def _conversion_success(self):
        """Handle successful conversion."""
        self.progress_bar.set(1.0)
        self.status_label.configure(
            text="✅ Conversion successful!",
            text_color="lightgreen"
        )
        
        # Re-enable buttons
        self.browse_btn.configure(state="normal")
        self.convert_btn.configure(state="normal")
        
        # Show open output button
        self.open_output_btn.pack(pady=10)
        
        # Show success message
        messagebox.showinfo(
            "Success",
            f"Document created successfully!\n\nSaved to:\n{self.output_file_path}"
        )
    
    def _conversion_failed(self, error_message: str):
        """Handle failed conversion."""
        self.progress_bar.set(0)
        self.status_label.configure(
            text="❌ Conversion failed",
            text_color="red"
        )
        
        # Re-enable buttons
        self.browse_btn.configure(state="normal")
        self.convert_btn.configure(state="normal")
        
        # Show error message
        messagebox.showerror(
            "Conversion Failed",
            f"An error occurred during conversion:\n\n{error_message}"
        )
    
    def _open_output_file(self):
        """Open the generated Word document."""
        if self.output_file_path and os.path.exists(self.output_file_path):
            try:
                if sys.platform == "win32":
                    os.startfile(self.output_file_path)
                elif sys.platform == "darwin":
                    subprocess.run(["open", self.output_file_path])
                else:
                    subprocess.run(["xdg-open", self.output_file_path])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file:\n{str(e)}")
        else:
            messagebox.showwarning("File Not Found", "Output file does not exist.")
    
    def run(self):
        """Start the application main loop."""
        self.root.mainloop()


def main():
    """Main entry point for the GUI application."""
    app = ImageToWordApp()
    app.run()


if __name__ == "__main__":
    main()
