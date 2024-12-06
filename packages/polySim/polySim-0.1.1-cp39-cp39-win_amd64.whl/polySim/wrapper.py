import numpy as np
from .libpolySim import generateStructure  # Import directly from the compiled module

def generate_structure(img, nucleation_rate, growth_rate, height=300, randomize_gray_values=True):
    length, width = img.shape
    randomize_flag = 1 if randomize_gray_values else 0

    # Ensure the image is contiguous and of type uint16
    img = np.ascontiguousarray(img, dtype=np.uint16)

    # Call the C++ function directly
    num_grains, avrami_exponent = generateStructure(
        img, length - 1, width - 1, height - 1,
        nucleation_rate, growth_rate, randomize_flag
    )

    # Return the modified image, number of grains, and Avrami exponent
    return img, num_grains, avrami_exponent
