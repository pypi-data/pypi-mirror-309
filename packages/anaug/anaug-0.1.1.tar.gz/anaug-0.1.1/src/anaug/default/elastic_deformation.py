import numpy as np
from scipy.ndimage import gaussian_filter, map_coordinates

def elastic_deformation(image, alpha=34, sigma=4):
    """
    Applies elastic deformation to a given image.
    
    Parameters:
    - image (np.array): Input image as a 2D or 3D numpy array.
    - alpha (float): Scale factor that controls the intensity of the deformation.
    - sigma (float): Standard deviation of the Gaussian kernel that controls the smoothness.

    Returns:
    - np.array: Deformed image with the same shape as input.
    """
    if alpha <= 0 or sigma <= 0:
        raise ValueError("Alpha and sigma must be positive values.")

    random_state = np.random.RandomState(None)
    shape = image.shape

    # Create displacement fields for x and y axes
    dx = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma) * alpha
    dy = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma) * alpha

    # Initialize dz if image has 3 dimensions (optional for 3D deformation)
    dz = np.zeros_like(dx) if image.ndim == 3 else None

    # Create coordinate meshgrid
    x, y = np.meshgrid(np.arange(shape[0]), np.arange(shape[1]), indexing='ij')
    indices = (np.reshape(x + dx, (-1, 1)), np.reshape(y + dy, (-1, 1)))

    # If 3D image, add third dimension to indices
    if dz is not None:
        z = np.arange(shape[2])
        indices += (np.reshape(z + dz, (-1, 1)),)

    # Apply deformation
    deformed_image = map_coordinates(image, indices, order=1).reshape(shape)
    return deformed_image