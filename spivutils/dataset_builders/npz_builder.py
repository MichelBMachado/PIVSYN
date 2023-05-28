#-----------------------------------------------------------------------------------
# CODE DETAILS
#-----------------------------------------------------------------------------------
# Author: Michel Bernardino Machado 
# Date:
# version:

#-----------------------------------------------------------------------------------
# REQUIRED PACKAGES
#-----------------------------------------------------------------------------------
from os import scandir
from os.path import join, split
from scipy.io import loadmat
import numpy as np
from cv2 import imread
import tempfile

#-----------------------------------------------------------------------------------
# CODE ROUTINES
#-----------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------
def build_data(input_dir, output_dir, dataset_name):
    """
    Build an npz dataset from image files and velocity vector field matrix files.
    """

    #===============================================================================
    def find_data(root_directory):
        """
        Examines the internal directories of a defined root directory and gets the 
        data path of each file.
        """
        directories_with_files = []
        for entry in scandir(root_directory):
            if entry.is_file():
                directories_with_files.append(root_directory)
                break
            elif entry.is_dir():
                subdirectories_with_files = find_data(entry.path)
                directories_with_files.extend(subdirectories_with_files)
        return directories_with_files

    #===============================================================================
    def indexes_data(input_path_list):
        """
        Stablishes a indexed relationship with each image file path of image pair and its 
        respective velocity vector field file path.
        """
        print('\n', 'Indexing data')
        output_path_list = []

        for path in input_path_list:
            velocity_field_file_list = [f.path for f in scandir(path) if f.name.endswith('.mat') and f.is_file()]
            particle_image_file_list = [f.path for f in scandir(path) if f.name.endswith('.tif') and f.is_file()] 

            number_of_files = len(velocity_field_file_list)

            for i in range(0, number_of_files):

                output_path_list.append([particle_image_file_list[0::2][i], 
                                         particle_image_file_list[1::2][i], 
                                         velocity_field_file_list[i]])

        output_path_list = np.array(output_path_list)

        return output_path_list

    #===============================================================================
    def randomize_data(input_path_list):
        """
        Randomize the path list of indexed files.
        """
        print('\n', 'Randomizing data')
        output_path_list = np.copy(input_path_list)
        np.random.shuffle(output_path_list)
        return output_path_list
    
    #===============================================================================
    def split_data(input_path_list, train_ratio, valid_ratio):
        """
        Split the list of randomized path files according to 
        train, validation and test ratios.
        """
        print('\n', 'Spliting data', '\n')
        train_indexes = int(len(input_path_list)*(train_ratio))
        valid_indexes = int(len(input_path_list)*(1 - valid_ratio))
        train_path_list, valid_path_list, test_path_list = np.split(input_path_list, [train_indexes, valid_indexes])

        return train_path_list, valid_path_list, test_path_list

    #===============================================================================
    def particle_image_importing(input_list, img_shape):
        """
        Import particle image files according to the file paths inside the input list. 
        """
        files_amount = (len(input_list),)
        output_path = tempfile.NamedTemporaryFile(dir = output_dir, delete = True)
        output_shape = files_amount + img_shape
        output_data = np.memmap(output_path, dtype = np.uint8, mode = 'w+', shape = output_shape)

        for i in range(output_shape[0]):

            for j in range(output_shape[1]):

                # Obtém o caminho de cada uma das imagens do par
                file_path = input_list[i,j]
                _, tail = split(file_path)

                print('Importing: ', tail)
                
                output_data[i, j, :, :] = np.reshape(imread(file_path, 0), (630, 665, 1))

        print('\n', 'Flushing data into disk', '\n')
        output_data.flush()

        return output_data

    #===============================================================================
    def velocity_field_importing(input_list, opf_shape):
        """
        Import velcocity field matrices files according to the file paths 
        inside the input list. 
        """
        files_amount = (len(input_list),)
        output_path = tempfile.NamedTemporaryFile(dir = output_dir, delete = True)
        output_shape = files_amount + opf_shape
        output_data = np.memmap(output_path, dtype = np.float16, mode = 'w+', shape = output_shape)

        for i in range(output_shape[0]):

            file_path = input_list[i,2]
            _, tail = split(file_path)

            print('Importing: ', tail)
            
            output_data[i, 0, :, :] = loadmat(file_path, simplify_cells = True)['exactOpticalFlowDisplacements']['velocities']['u']
            output_data[i, 1, :, :] = loadmat(file_path, simplify_cells = True)['exactOpticalFlowDisplacements']['velocities']['v']

        print('\n', 'Flushing data into disk', '\n')
        output_data.flush()

        return output_data
    
    #===============================================================================
    def data_exporter(train_list, valid_list, test_list, img_shape, opf_shape):
        """
        Exports data as a collection of .NPY files inside a compressed .NPZ file. 
        """
        data_dict = {
                    'train_x': particle_image_importing(train_list, img_shape),
                    'train_y': velocity_field_importing(train_list, opf_shape),
                    'valid_x': particle_image_importing(valid_list, img_shape),
                    'valid_y': velocity_field_importing(valid_list, opf_shape),
                    'test_x' : particle_image_importing(test_list, img_shape),
                    'test_y' : velocity_field_importing(test_list, opf_shape)
                    }

        dataset_path = join(output_dir, dataset_name)

        print('\n', 'Saving: ', dataset_name)
        np.savez_compressed(dataset_path, **data_dict)
        
    #===============================================================================
    img_width = 665     # Each image width.
    img_height = 630    # Each image height.
    img_frame = 2       # Quantity of sequential images.
    img_channel = 1     # Each image number of channels.
    vel_comp = 2        # Optical flow velocity components.
    train_ratio = 0.7   # Percentage of files used for training purpose.
    valid_ratio = 0.15  # Percentage of files usef for validation purpose.

    #===============================================================================
    img_shape = (img_frame, img_height, img_width, img_channel)
    opf_shape = (vel_comp, img_height, img_width)
    
    #===============================================================================
    print('\n', 'Scaning for data')
    raw_data_dir_list = find_data(input_dir)

    indexed_data_list = indexes_data(raw_data_dir_list)

    randomized_data_list = randomize_data(indexed_data_list)

    train_list, valid_list, test_list = split_data(randomized_data_list, train_ratio, valid_ratio)

    data_exporter(train_list, valid_list, test_list, img_shape, opf_shape)