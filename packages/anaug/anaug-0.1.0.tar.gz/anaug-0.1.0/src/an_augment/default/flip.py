import numpy as np

def flip(image, flip_horizontal=True, flip_vertical=False):
    """
    Flips the image horizontally, vertically, or both, based on the parameters.
    
    Parameters:
    - image (np.ndarray): Input image as a 2D (grayscale) or 3D (multi-channel) numpy array.
    - flip_horizontal (bool): If True, applies a horizontal flip.
    - flip_vertical (bool): If True, applies a vertical flip.

    Returns:
    - np.ndarray: Flipped image based on specified parameters.

    Raises:
    - TypeError: If the input image is not a numpy array.
    - ValueError: If the input image has invalid dimensions.
    """
    # Validate input type
    if not isinstance(image, np.ndarray):
        raise TypeError("Input image must be a numpy array.")
    
    # Validate dimensions
    if image.ndim < 2 or image.ndim > 3:
        raise ValueError("Input image must be a 2D (grayscale) or 3D (multi-channel) array.")
    
    # Apply flips
    if flip_horizontal:
        image = np.fliplr(image)  # Horizontal flip
    if flip_vertical:
        image = np.flipud(image)  # Vertical flip

    return image
