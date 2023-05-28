#-----------------------------------------------------------------------------------
# CODE DETAILS
#-----------------------------------------------------------------------------------
# Author: Michel Bernardino Machado 
# Date:
# version:

#-----------------------------------------------------------------------------------
# REQUIRED PACKAGES
#-----------------------------------------------------------------------------------
from numpy import sqrt
from cv2 import threshold, THRESH_BINARY

#-----------------------------------------------------------------------------------
# CODE ROUTINES
#-----------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------
def normalization(input_data):
    """
    Normalize the images symply dividing the array by 255
    """
    output_data = input_data/255

    return output_data

#-----------------------------------------------------------------------------------
def thresholding(input_data):
    """
    
    """
    output_data = threshold(input_data, 127, 255, THRESH_BINARY)[1]

    return output_data

#-----------------------------------------------------------------------------------
def vectoraddition(input_data):
    """
    Determines the magnitude of the velocity field using its u and v components
    """
    u_comp = input_data[:, 0]
    v_comp = input_data[:, 1]
    output_data = sqrt(u_comp ** 2 + v_comp ** 2)

    return output_data