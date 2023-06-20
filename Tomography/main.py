# 1. Generate a test case
# 2. Conduct scan
# 3. Reconstruct the image based on the scan
# 4. Compare the reconstructed image with the original image

from config_fns import *
from configs import *

# Source images
circle = "Circle.bmp"
letter_A = "Letter A.bmp"

# 0. Open the image
img = open_image(f"{source_folder}/{letter_A}")

# 1. Generate a test scan
scan_angles = np.linspace(0, 360, 128)
raw_scan = simulated_scan(img, scan_angles, save_plot = True)

# 2. Filter the image
filtered_scan = filtering(raw_scan, arctan_filter, save_plot = True)

# 3. Reconstruct the image
reconstructed = reconstruction(img, filtered_scan, scan_angles, save_plot = True)

print("Done!")
