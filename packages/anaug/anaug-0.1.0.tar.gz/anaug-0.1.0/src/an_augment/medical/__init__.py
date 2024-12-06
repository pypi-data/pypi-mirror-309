"""
The `medical` module provides augmentation techniques tailored specifically for medical imaging data.

This module supports various augmentation methods to simulate realistic clinical variations
in datasets such as MRI, CT, and X-ray images. These augmentations are designed to improve
model robustness and performance by diversifying the training data.

## Features
- **Elastic Deformation**: Simulate realistic tissue distortions.
- **Intensity Scaling**: Adjust brightness and contrast levels.
- **Gaussian Blur**: Mimic lower-resolution medical imaging.
- **Flipping and Rotation**: Enhance data diversity with spatial transformations.
- **Occlusion**: Simulate scenarios with partial visibility.
- **Noise Injection**: Add Gaussian or uniform noise for robustness.

## Usage
To apply medical augmentations, initialize the `MedicalAugmentation` class and specify the desired transformations.

Example:
```python
from an_augment.medical.medical_augmentation import MedicalAugmentation

augmentor = MedicalAugmentation()
augmented_image = augmentor.apply_augmentations(
    image,
    elastic_deformation=True,
    intensity_scaling=True
)
"""