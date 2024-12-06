def crop(image, top, left, height, width):
    """
    Crop an image to the specified size and position.
    
    Args:
        image (numpy.ndarray): Input image.
        top (int): Top pixel coordinate.
        left (int): Left pixel coordinate.
        height (int): Desired height.
        width (int): Desired width.
        
    Returns:
        numpy.ndarray: Cropped image.
        
    Raises:
        ValueError: If crop parameters are invalid or exceed image boundaries.
        TypeError: If input parameters are not integers.
    """
    # Validate types
    if not all(isinstance(x, int) for x in [top, left, height, width]):
        raise TypeError("All crop parameters (top, left, height, width) must be integers.")
    
    # Validate dimensions and boundaries
    if (
        top < 0 or left < 0 or height <= 0 or width <= 0 or
        top + height > image.shape[0] or left + width > image.shape[1]
    ):
        raise ValueError(
            f"Invalid crop parameters: (top={top}, left={left}, height={height}, width={width}) "
            f"exceed image dimensions {image.shape[:2]}."
        )
    
    # Perform cropping
    return image[top:top+height, left:left+width]
