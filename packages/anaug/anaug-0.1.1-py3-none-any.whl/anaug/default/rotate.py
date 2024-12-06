from scipy.ndimage import rotate as scipy_rotate
import numpy as np

def rotate(image, angle, mode='nearest'):
    """
    Rotate the image by the specified angle.
    
    Parameters:
    - image (np.ndarray): Input image as a 2D (grayscale) or 3D (multi-channel) numpy array.
    - angle (float): Angle by which to rotate the image (in degrees).
    - mode (str): Points outside the boundaries of the input are filled according to the given mode 
                  ('constant', 'nearest', 'mirror', or 'wrap').
    
    Returns:
    - np.ndarray: Rotated image.
    
    Raises:
    - TypeError: If the input image is not a numpy array.
    - ValueError: If the angle is not numeric or if the mode is invalid.
    """
    # Validate input type
    if not isinstance(image, np.ndarray):
        raise TypeError("Input image must be a numpy array.")
    
    # Validate angle
    if not isinstance(angle, (int, float)):
        raise ValueError("Angle must be a numeric value.")
    
    # Validate image dimensions
    if image.ndim < 2 or image.ndim > 3:
        raise ValueError("Input image must be a 2D (grayscale) or 3D (multi-channel) array.")
    
    # Validate mode
    valid_modes = ['constant', 'nearest', 'mirror', 'wrap']
    if mode not in valid_modes:
        raise ValueError(f"Invalid mode '{mode}'. Supported modes are: {valid_modes}")
    
    # Rotate the image
    return scipy_rotate(image, angle, reshape=False, mode=mode)
