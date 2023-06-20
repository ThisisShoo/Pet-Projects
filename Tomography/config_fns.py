# Configuration function for a tomography scanner
import numpy as np
from matplotlib import pyplot as plt
import scipy

from configs import *

# Open an image
def open_image(image_file):
    """Function that converts an image file into a numpy array
    
    Args:
        image_file (str): a string indicating the file path to the object's cross-sectional image.

    Returns:
        gray_array (numpy.ndarray): a 2D array corresponding to the initial image's 
            black-and-white version.
    """
    print("Opening image...")
    img = plt.imread(f"{image_file}")
    image_array = np.array(img)

    gray_array = np.zeros(image_array.shape[0:2])
    for count, ele in enumerate(image_array):
        for count2, ele2 in enumerate(ele):
            gray_array[count][count2] = np.mean(ele2)/255

    return gray_array

# Simulate a tomography scan
def simulated_scan(image, scan_angles, save_plot = False, plot_name = 'sinogram'):
    """Produces a simulated scan of the given image.
    For each angle, the image will be rotated to that angle, 
        then the scan will be taken by taking the sum of the pixels in each column.

    Args:
        image (numpy.ndarray): The image to be scanned;
        scan_angles (list): A sequence (or numpy array) of integers or floats indicating 
            the angles at which the object is being scanned.
    
    Returns:
        optics_space (numpy.ndarray): The scan of the image.
    """
    print("Generating simulated scan...")
    optics_space = []
    for ele in scan_angles:
        rotated = scipy.ndimage.rotate(image, ele, reshape=False)
        scan = sum(rotated)
        optics_space.append(scan)

    if save_plot:
        fig, sinogram_plot = plt.subplots(1, 1, figsize=(5, 7))

        sinogram_plot.imshow(optics_space, cmap="gray")
        sinogram_plot.set_ylabel("Angle (degrees)")
        sinogram_plot.set_xlabel("Pixels")

        fig.tight_layout()

        fig.savefig(f"{intermediate_folder}/{plot_name}")

    return optics_space

def filtering(sinogram, filter_fn, save_plot = False, plot_name = 'filter', save_row = 0):
    """Filters the sinogram using the given filter function
    
    Args:
        sinogram (numpy.ndarray): The scan of the image;
        filter_fn (function): A function that takes in two integers (start and end) and
            returns a numpy array of the same length as the input.

    Returns:
        filtered (numpy.ndarray): The filtered sinogram.
    """
    print("Filtering sinogram...")
    filtered = []
    for row in sinogram:
        fft_row = np.fft.fft(row)
        # fft_filter = filter_fn(-len(fft_row), len(fft_row))
        fft_filter = filter_fn(0, len(fft_row))
        filtered_row = np.multiply(fft_row, fft_filter)

        filtered_row = np.real(np.fft.ifft(filtered_row))

        filtered.append(filtered_row)

    output = np.copy(filtered)

    if save_plot:
        fig, filtered_plot = plt.subplots(3, 1, figsize=(5, 7))

        filtered_plot[0].plot(sinogram[save_row])
        filtered_plot[0].set_title("Original")

        filtered_plot[1].plot(fft_filter)
        filtered_plot[1].set_title("FFT filter")

        filtered_plot[2].plot(filtered_row)
        filtered_plot[2].set_title("Filtered row")

        fig.tight_layout()

        fig.savefig(f"{intermediate_folder}/{plot_name + str(save_row)}")

    return output

def reconstruction(img, sinogram, scan_angles, smear_depth = None, 
                   save_plot = False, plot_name = 'Result'):
    """Reconstructs the image from sinogram.
    First, smear each sinogram row over the entire image. 
    Second, overlap at each angle.
    Third, profit! 

    Args:
        sinogram (numpy.ndarray): The scan of the image;
        scan_angles (list): A sequence (or numpy array) of integers or floats indicating
            the angles at which the object is being scanned.
        smear_depth (int): The number of pixels to smear each sinogram row over.
            If not specified, the default value is the number of pixels in each sinogram row.

    Returns:
        result (numpy.ndarray): The reconstructed image.
    """
    print("Reconstructing image...")
    smear_depth = smear_depth or len(img[0])

    result = np.zeros((len(img[0]), smear_depth))
    for count, rows in enumerate(sinogram):
        smear = np.tile(rows, (smear_depth, 1))

        temp_image = scipy.ndimage.rotate(smear, scan_angles[count], reshape=False)

        result = np.add(result, temp_image)

        count += 1
    
    result = np.flip(result)

    if save_plot:
        fig, result_plot = plt.subplots(1, 1, figsize=(5, 7))

        result_plot.imshow(result, cmap="gray")

        fig.tight_layout()

        fig.savefig(f"{intermediate_folder}/{plot_name}")

    return result

# Mathematical functions
def laplace(start, end):
    """Defines a function for Laplace equation"""
    a = end/2
    b = 20
    c = 1

    x = np.linspace(start, end, end)

    return -c * np.exp(-np.abs(x-a)/b) + c

def abs_fn(start, end):
    """Defines a function for the absolute value"""
    x = np.linspace(start, end, end)

    return np.abs(np.cos(np.pi * x/len(x)))

def Gaussian(start, end):
    """Defines a function for a Gaussian"""
    x = np.linspace(start, end, end)

    a = 0.5 * (end - start)
    b = (end - start) * 0.1

    gaussian = (2 * np.pi)**-0.5 * np.exp(-0.5 * ((x-a)/(2*b))**2)
    # gaussian = -gaussian/np.max(gaussian)+1
    gaussian = -gaussian + np.max(gaussian)
    gaussian = gaussian/np.max(gaussian)

    return gaussian

def quadratic(start, end):
    """Defines a quadratic function"""
    x = np.linspace(start, end, end)

    a = 1
    b = 1
    c = 0

    output = a * x**2 + b * x + c
    output = output/np.max(output)
    return output

def arctan_filter(start, end):
    """Defines an arctan function"""
    x = np.linspace(start, end, end)

    a = 2/np.pi
    b = end * 0.005
    c = 0

    output = a * np.arctan(x - b) + c
    output -= np.min(output)
    output = output/np.max(output) 
    return output