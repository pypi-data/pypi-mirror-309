import numpy as np
import cv2

def random_rotation(image, angle_range=(-30, 30)):
    """
    Applies a random rotation to the image within the specified angle range.
    
    Parameters:
    - image (np.array): Input image as a 2D or 3D numpy array.
    - angle_range (tuple): Range of angles to randomly rotate the image, e.g., (-30, 30).

    Returns:
    - np.array: Rotated image with the same shape as input.
    """
    # Randomly select an angle within the specified range
    angle = np.random.uniform(angle_range[0], angle_range[1])

    # Get the image dimensions and calculate the center
    h, w = image.shape[:2]
    center = (w / 2, h / 2)

    # Compute the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale=1.0)

    # Apply rotation
    rotated_image = cv2.warpAffine(image, rotation_matrix, (w, h), borderMode=cv2.BORDER_REFLECT)
    return rotated_image
