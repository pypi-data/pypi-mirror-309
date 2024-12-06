"""Apply an occlusion mask to the image to \
    simulate partial visibility."""

import numpy as np


def occlusion(image, mask_shape='rectangle', mask_size_range=(0.1, 0.3)):
    """
    Apply an occlusion to a random part of the image.

    Parameters:
        image (np.array): Input image as a 2D or \
            3D numpy array.
        mask_shape (str): Shape of the mask to apply. \
            Default is 'rectangle'.
        mask_size_range (tuple): Range for the \
            size of the mask as a percentage of image size.

    Returns:
        np.array: Image with an added occlusion.

    Raises:
        ValueError: If the specified mask shape is not supported.
    """
    h, w = image.shape[:2]
    mask_h = int(np.random.uniform(
        mask_size_range[0], 
        mask_size_range[1]
    ) * h)
    mask_w = int(np.random.uniform(
        mask_size_range[0], 
        mask_size_range[1]
    ) * w)

    # Ensure the mask dimensions are valid
    mask_h = max(1, mask_h)
    mask_w = max(1, mask_w)

    # Randomly choose the position of the mask
    start_x = np.random.randint(0, h - mask_h + 1)
    start_y = np.random.randint(0, w - mask_w + 1)

    # Apply the mask by setting the area to zero (black)
    occluded_image = image.copy()
    if mask_shape == 'rectangle':
        occluded_image[start_x:start_x + mask_h, 
                       start_y:start_y + mask_w] = 0
    else:
        raise ValueError("Unsupported mask shape. Currently only 'rectangle' is supported.")

    return occluded_image
