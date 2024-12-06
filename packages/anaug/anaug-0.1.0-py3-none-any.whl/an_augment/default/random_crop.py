import numpy as np
import cv2

def random_crop(image, crop_size=(0.8, 0.8), scaling_factor=1.0):
    """
    Randomly crops a portion of the image and scales it to the original size.
    
    Parameters:
    - image (np.array): Input image as a 2D or 3D numpy array.
    - crop_size (tuple): The size of the cropped area as a percentage of the original dimensions.
    - scaling_factor (float): Factor to scale the cropped area when resizing to the original dimensions.

    Returns:
    - np.array: Cropped and scaled image with the original shape.
    """
    h, w = image.shape[:2]
    crop_h, crop_w = int(h * crop_size[0]), int(w * crop_size[1])

    # Ensure crop size is at least 1 pixel in each dimension
    crop_h = max(1, crop_h)
    crop_w = max(1, crop_w)

    # Randomly select top-left corner of the crop
    start_x = np.random.randint(0, h - crop_h)
    start_y = np.random.randint(0, w - crop_w)

    # Crop the image
    cropped_image = image[start_x:start_x + crop_h, start_y:start_y + crop_w]

    # Resize the cropped image back to the original size with scaling factor
    target_size = (int(w * scaling_factor), int(h * scaling_factor))
    scaled_image = cv2.resize(cropped_image, target_size, interpolation=cv2.INTER_LINEAR)

    # If the scaled image is smaller than original dimensions, pad it
    padded_image = np.zeros_like(image)
    pad_x = min(target_size[0], w)
    pad_y = min(target_size[1], h)
    padded_image[:pad_y, :pad_x] = scaled_image[:pad_y, :pad_x]

    return padded_image
