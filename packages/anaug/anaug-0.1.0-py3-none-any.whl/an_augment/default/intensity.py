import numpy as np

def intensity(image, brightness_factor=1.0, contrast_factor=1.0):
    """
    Adjusts brightness and contrast of a given image.
    
    Parameters:
    - image (np.array): Input image as a 2D or 3D numpy array.
    - brightness_factor (float): Factor to adjust brightness. Values > 1 increase brightness.
    - contrast_factor (float): Factor to adjust contrast. Values > 1 increase contrast.

    Returns:
    - np.array: Image with adjusted brightness and contrast.
    """
    # Convert image to float for calculations to avoid overflow
    image = image.astype(float)

    # Adjust brightness
    image = image * brightness_factor

    # Adjust contrast
    mean_intensity = np.mean(image)
    image = contrast_factor * (image - mean_intensity) + mean_intensity

    # Clip values to ensure they remain within the valid range [0, 1] or [0, 255]
    return np.clip(image, 0, 255 if image.max() > 1 else 1).astype(image.dtype)
