import cv2

def scale(image, scale_factor):
    """
    Scale an image by a given factor.
    
    Args:
        image (numpy.ndarray): Input image.
        scale_factor (float): Factor to scale the image.
        
    Returns:
        numpy.ndarray: Scaled image.
    """
    height, width = image.shape[:2]
    new_dims = (int(width * scale_factor), int(height * scale_factor))
    return cv2.resize(image, new_dims, interpolation=cv2.INTER_LINEAR)
