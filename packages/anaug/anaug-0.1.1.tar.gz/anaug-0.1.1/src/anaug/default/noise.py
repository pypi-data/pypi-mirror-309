import numpy as np

def noise(image, noise_type='gaussian', noise_intensity=0.05):
    """
    Adds noise to the image to simulate different scanning conditions.
    
    Parameters:
    - image (np.ndarray): Input image as a 2D (grayscale) or 3D (multi-channel) numpy array.
    - noise_type (str): Type of noise to add ('gaussian' or 'salt_and_pepper').
    - noise_intensity (float): Intensity of the noise. For Gaussian, it represents the standard deviation; 
                               for salt_and_pepper, it represents the proportion of affected pixels.

    Returns:
    - np.ndarray: Image with added noise.

    Raises:
    - TypeError: If the input image is not a numpy array.
    - ValueError: If the noise type is unsupported or noise intensity is invalid.
    """
    # Validate input type
    if not isinstance(image, np.ndarray):
        raise TypeError("Input image must be a numpy array.")
    
    # Validate noise intensity
    if noise_intensity < 0 or noise_intensity > 1:
        raise ValueError("Noise intensity must be between 0 and 1.")

    if noise_type == 'gaussian':
        # Gaussian noise
        mean = 0
        gauss = np.random.normal(mean, noise_intensity, image.shape)
        noisy_image = image + gauss
        return np.clip(noisy_image, 0, 1)  # Assuming image is in range [0, 1]
    
    elif noise_type == 'salt_and_pepper':
        # Salt-and-pepper noise
        noisy_image = image.copy()
        num_salt = np.ceil(noise_intensity * image.size * 0.5).astype(int)
        num_pepper = np.ceil(noise_intensity * image.size * 0.5).astype(int)

        # Generate salt coordinates
        coords_salt = [np.random.randint(0, dim, num_salt) for dim in image.shape]
        noisy_image[tuple(coords_salt)] = 1

        # Generate pepper coordinates
        coords_pepper = [np.random.randint(0, dim, num_pepper) for dim in image.shape]
        noisy_image[tuple(coords_pepper)] = 0

        return noisy_image
    
    else:
        raise ValueError("Unsupported noise type. Use 'gaussian' or 'salt_and_pepper'.")
