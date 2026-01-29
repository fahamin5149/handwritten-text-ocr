"""
Image preprocessing utilities for improved OCR accuracy.
Includes deskewing, noise removal, and contrast enhancement.
"""

import cv2
import numpy as np
from PIL import Image


def preprocess_image(image_path: str) -> np.ndarray:
    """
    Complete preprocessing pipeline for OCR optimization.
    
    Args:
        image_path: Path to the input image file
        
    Returns:
        Preprocessed image as numpy array
    """
    # Load image
    image = cv2.imread(image_path)
    
    if image is None:
        raise ValueError(f"Unable to load image from {image_path}")
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply deskewing
    gray = deskew_image(gray)
    
    # Remove noise
    denoised = remove_noise(gray)
    
    # Apply adaptive thresholding for better text extraction
    processed = apply_threshold(denoised)
    
    return processed


def deskew_image(image: np.ndarray) -> np.ndarray:
    """
    Detect and correct skew in the image.
    
    Args:
        image: Grayscale image as numpy array
        
    Returns:
        Deskewed image
    """
    # Detect edges
    edges = cv2.Canny(image, 50, 150, apertureSize=3)
    
    # Detect lines using Hough transform
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
    
    if lines is None:
        return image
    
    # Calculate the dominant angle
    angles = []
    for rho, theta in lines[:, 0]:
        angle = np.degrees(theta) - 90
        if -45 < angle < 45:
            angles.append(angle)
    
    if not angles:
        return image
    
    # Use median angle for stability
    median_angle = np.median(angles)
    
    # Only rotate if skew is significant (> 0.5 degrees)
    if abs(median_angle) > 0.5:
        # Get image center and rotation matrix
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, median_angle, 1.0)
        
        # Perform rotation with white background
        rotated = cv2.warpAffine(
            image, 
            rotation_matrix, 
            (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=255
        )
        return rotated
    
    return image


def remove_noise(image: np.ndarray) -> np.ndarray:
    """
    Apply noise reduction filters.
    
    Args:
        image: Grayscale image as numpy array
        
    Returns:
        Denoised image
    """
    # Apply Non-Local Means Denoising
    denoised = cv2.fastNlMeansDenoising(image, None, h=10, templateWindowSize=7, searchWindowSize=21)
    
    # Apply Gaussian blur for additional smoothing
    blurred = cv2.GaussianBlur(denoised, (3, 3), 0)
    
    return blurred


def apply_threshold(image: np.ndarray) -> np.ndarray:
    """
    Apply adaptive thresholding for better text/background separation.
    
    Args:
        image: Grayscale image as numpy array
        
    Returns:
        Thresholded binary image
    """
    # Use Otsu's thresholding after Gaussian filtering
    blur = cv2.GaussianBlur(image, (5, 5), 0)
    _, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Alternative: Adaptive thresholding (uncomment if Otsu doesn't work well)
    # binary = cv2.adaptiveThreshold(
    #     image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    # )
    
    return binary


def resize_image_for_ocr(image: np.ndarray, target_height: int = 2000) -> np.ndarray:
    """
    Resize image to optimal size for OCR (larger is often better).
    
    Args:
        image: Input image as numpy array
        target_height: Target height in pixels
        
    Returns:
        Resized image
    """
    height, width = image.shape[:2]
    
    if height < target_height:
        # Scale up small images
        scale = target_height / height
        new_width = int(width * scale)
        resized = cv2.resize(image, (new_width, target_height), interpolation=cv2.INTER_CUBIC)
        return resized
    
    return image


def pil_to_cv2(pil_image: Image.Image) -> np.ndarray:
    """
    Convert PIL Image to OpenCV format.
    
    Args:
        pil_image: PIL Image object
        
    Returns:
        OpenCV image (numpy array)
    """
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)


def cv2_to_pil(cv2_image: np.ndarray) -> Image.Image:
    """
    Convert OpenCV image to PIL format.
    
    Args:
        cv2_image: OpenCV image (numpy array)
        
    Returns:
        PIL Image object
    """
    return Image.fromarray(cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB))
