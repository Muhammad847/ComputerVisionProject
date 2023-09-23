
# Python 2/3 compatibility
from __future__ import print_function
 
import cv2 # Import the OpenCV library
import numpy as np # Import Numpy library
import matplotlib.pyplot as plt # Import matplotlib functionality
import sys # Enables the passing of arguments
 
# Project: Histogram Matching Using OpenCV
 
# Define the file name of the images
SOURCE_IMAGE = "Junayed_reference.jpg"
REFERENCE_IMAGE = "Junayed_source.jpg"

# MASK_IMAGE = "mask.jpg"
# MASK_IMAGE = "mask2.jpg"
MASK_IMAGE = "mask3.jpg"


OUTPUT_IMAGE = "Output_without_mask.jpg"
OUTPUT_MASKED_IMAGE = "Output_with_mask.jpg"
 
def calculate_cdf(histogram):
    """
    This method calculates the cumulative distribution function
    :param array histogram: The values of the histogram
    :return: normalized_cdf: The normalized cumulative distribution function
    :rtype: array
    """
    # Get the cumulative sum of the elements
    cdf = histogram.cumsum()
 
    # Normalize the cdf
    normalized_cdf = cdf / float(cdf.max())
 
    return normalized_cdf
 
def calculate_lookup(src_cdf, ref_cdf):
    """
    This method creates the lookup table
    :param array src_cdf: The cdf for the source image
    :param array ref_cdf: The cdf for the reference image
    :return: lookup_table: The lookup table
    :rtype: array
    """
    lookup_table = np.zeros(256)
    lookup_val = 0
    for src_pixel_val in range(len(src_cdf)):
        lookup_val
        for ref_pixel_val in range(len(ref_cdf)):
            if ref_cdf[ref_pixel_val] >= src_cdf[src_pixel_val]:
                lookup_val = ref_pixel_val
                break
        lookup_table[src_pixel_val] = lookup_val
    return lookup_table
 
def match_histograms(src_image, ref_image):
    """
    This method matches the source image histogram to the
    reference signal
    :param image src_image: The original source image
    :param image  ref_image: The reference image
    :return: image_after_matching
    :rtype: image (array)
    """
    # Split the images into the different color channels
    # b means blue, g means green and r means red
    src_b, src_g, src_r = cv2.split(src_image)
    ref_b, ref_g, ref_r = cv2.split(ref_image)
 
    # Compute the b, g, and r histograms separately
    # The flatten() Numpy method returns a copy of the array c
    # collapsed into one dimension.
    src_hist_blue, bin_0 = np.histogram(src_b.flatten(), 256, [0,256])
    src_hist_green, bin_1 = np.histogram(src_g.flatten(), 256, [0,256])
    src_hist_red, bin_2 = np.histogram(src_r.flatten(), 256, [0,256])    
    ref_hist_blue, bin_3 = np.histogram(ref_b.flatten(), 256, [0,256])    
    ref_hist_green, bin_4 = np.histogram(ref_g.flatten(), 256, [0,256])
    ref_hist_red, bin_5 = np.histogram(ref_r.flatten(), 256, [0,256])
    
     
# Assuming you have six images stored in variables img1, img2, img3, img4, img5, and img6

    # Create a new figure with a 2x3 grid of subplots
#     plt.figure()

#     # Subplot 1
#     plt.subplot(2, 3, 1)
#     plt.hist(src_hist_blue, bins=255, edgecolor='black')
#     plt.title('Image 1')

#     # Subplot 2
#     plt.subplot(2, 3, 2)
#     plt.hist(src_hist_green, bins=255, edgecolor='black')
#     plt.title('Image 2')

#     # Subplot 3
#     plt.subplot(2, 3, 3)
#     plt.hist(src_hist_red, bins=255, edgecolor='black')
#     plt.title('Image 3')

#     # Subplot 4
#     plt.subplot(2, 3, 4)
#     plt.hist(ref_hist_green, bins=255, edgecolor='black')
#     plt.title('Image 4')

#     # Subplot 5
#     plt.subplot(2, 3, 5)
#     plt.hist(ref_hist_blue, bins=255, edgecolor='black')
#     plt.title('Image 5')

#     # Subplot 6
#     plt.subplot(2, 3, 6)
#     plt.hist(ref_hist_red, bins=255, edgecolor='black')
#     plt.title('Image 6')

#     # Adjust spacing between subplots for better layout
#     plt.tight_layout()

#     # Show the figure with all the subplots
#     plt.show()
 
# # Customize the plot (optional)
#     plt.title('Histogram Example')
#     plt.xlabel('Values')
#     plt.ylabel('Frequency')

#     # Show the histogram
#     plt.show()
 

    # Compute the normalized cdf for the source and reference image
    src_cdf_blue = calculate_cdf(src_hist_blue)
    src_cdf_green = calculate_cdf(src_hist_green)
    src_cdf_red = calculate_cdf(src_hist_red)
    ref_cdf_blue = calculate_cdf(ref_hist_blue)
    ref_cdf_green = calculate_cdf(ref_hist_green)
    ref_cdf_red = calculate_cdf(ref_hist_red)
 
    # Make a separate lookup table for each color
    blue_lookup_table = calculate_lookup(src_cdf_blue, ref_cdf_blue)
    green_lookup_table = calculate_lookup(src_cdf_green, ref_cdf_green)
    red_lookup_table = calculate_lookup(src_cdf_red, ref_cdf_red)
    
    # Use the lookup function to transform the colors of the original
    # source image
    blue_after_transform = cv2.LUT(src_b, blue_lookup_table)
    green_after_transform = cv2.LUT(src_g, green_lookup_table)
    red_after_transform = cv2.LUT(src_r, red_lookup_table)
 
    # Put the image back together
    image_after_matching = cv2.merge([
        blue_after_transform, green_after_transform, red_after_transform])
    image_after_matching = cv2.convertScaleAbs(image_after_matching)
 
    return image_after_matching
 
def mask_image(image, mask):
    """
    This method overlays a mask on top of an image
    :param image image: The color image that you want to mask
    :param image mask: The mask
    :return: masked_image
    :rtype: image (array)
    """
 
    # Split the colors into the different color channels
    blue_color, green_color, red_color = cv2.split(image)
 
    # Resize the mask to be the same size as the source image
    resized_mask = cv2.resize(
        mask, (image.shape[1], image.shape[0]), cv2.INTER_NEAREST)
 
    # Normalize the mask
    normalized_resized_mask = resized_mask / float(255)
 
    # Scale the color values
    blue_color = blue_color * normalized_resized_mask
    blue_color = blue_color.astype(int)
    green_color = green_color * normalized_resized_mask
    green_color = green_color.astype(int)
    red_color = red_color * normalized_resized_mask
    red_color = red_color.astype(int)
 
    # Put the image back together again
    merged_image = cv2.merge([blue_color, green_color, red_color])
    masked_image = cv2.convertScaleAbs(merged_image)
    return masked_image
 
def main():
    """
    Main method of the program.
    """
    start_the_program = input("Press ENTER to perform histogram matching...") 
 
    # A flag to indicate if the mask image was provided or not by the user
    
    
    # mask_provided = False
    mask_provided = True
 
    # Pull system arguments
    try:
        image_src_name = sys.argv[1]
        image_ref_name = sys.argv[2]
    

    except:
        image_src_name = SOURCE_IMAGE
        image_ref_name = REFERENCE_IMAGE
 
    try:
        image_mask_name = MASK_IMAGE
        mask_provided = True
    except:
        print("\nNote: A mask was not provided.\n")
    
    image_src_name = SOURCE_IMAGE
    image_src = cv2.imread(image_src_name)
    image_ref_name = REFERENCE_IMAGE
    image_ref = cv2.imread(image_ref_name)
    # Load the images and store them into a variable
    # image_src = cv2.imread(cv2.samples.findFile(image_src_name))
    # image_ref = cv2.imread(cv2.samples.findFile(image_ref_name))
 
    image_mask = MASK_IMAGE 
    if mask_provided:
        image_mask = cv2.imread(cv2.samples.findFile(image_mask_name))
 
    # Check if the images loaded properly
    if image_src is None:
        print('Failed to load source image file:', image_src_name)
        sys.exit(1)
    elif image_ref is None:
        print('Failed to load reference image file:', image_ref_name)
        sys.exit(1)
    else:
        # Do nothing
        pass
 
    # Convert the image mask to grayscale
    if mask_provided:
        image_mask = cv2.cvtColor(image_mask, cv2.COLOR_BGR2GRAY)
        
    # Calculate the matched image
    output_image = match_histograms(image_src, image_ref)
 
    # Mask the matched image
    if mask_provided:
        output_masked = mask_image(output_image, image_mask)
 
    # Save the output images
    cv2.imwrite(OUTPUT_IMAGE, output_image)
    if mask_provided:
        cv2.imwrite(OUTPUT_MASKED_IMAGE, output_masked)
   
    ## Display images, used for debugging
    cv2.imshow('Source Image', image_src)
    cv2.imshow('Reference Image', image_ref)
    cv2.imshow('Output Image', output_image)
    if mask_provided:
        cv2.imshow('Mask', image_mask)
        cv2.imshow('Output Image (Masked)', output_masked)
    
    cv2.waitKey(0) # Wait for a keyboard event
 
if __name__ == '__main__':
    print(__doc__)
    main()
    cv2.destroyAllWindows()