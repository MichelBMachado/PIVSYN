#---------------------------------------------------------------------------------------
# REQUIRED PACKAGES
#---------------------------------------------------------------------------------------
from os import listdir
from os.path import join, abspath, dirname
from zipfile import ZipFile 
from numpy import load

#---------------------------------------------------------------------------------------
# FUNCTIONS DEFINITION
#---------------------------------------------------------------------------------------
"""Make dataset avaiable"""
def load_data():

    #-----------------------------------------------------------------------------------
    """Remove the compressed dataset"""
    def remove_data():
        pass

    #-----------------------------------------------------------------------------------
    """Gets the dataset from web repository"""
    def get_data():
        pass
    
    #-----------------------------------------------------------------------------------
    """Extract already downloaded dataset"""
    def extract_data(dataset_dir, dataset_name, dataset_path):
        with ZipFile(dataset_path, 'r') as f:
            print('\n', 'Uncompressing: ', dataset_name)
            f.extractall(path = dataset_dir)
            f.close
        return 

    #-----------------------------------------------------------------------------------
    """Verify wich files are in place"""
    def check_data(dataset_dir, dataset_name, subset_names):
        file_list = listdir(dataset_dir)
        print('\n', 'Checking files ...')
        for name in subset_names:
            if name in file_list:
                print('\n', name, ' Found!')
            else:
                print('\n', name, ' Not found!')
                print('\n', 'Checking for',  dataset_name, ' ...')
                if dataset_name in file_list:
                    print('\n', dataset_name, ' is already downloaded!')
                    print('\n', dataset_name, ' must be uncompressed!')
                    extract_data(dataset_dir, dataset_name, dataset_path)
                    return 
                else:
                    print('\n', dataset_name, ' is not downloaded!')
                    get_data()
                    extract_data(dataset_dir, dataset_name, dataset_path)
                    return 
        return 
    
    #-----------------------------------------------------------------------------------
    def import_data(subset_path):
        print('\n', 'Importing data ...')
        output_data = [load(subset_path[0], mmap_mode = 'r'),
                       load(subset_path[1], mmap_mode = 'r'), 
                       load(subset_path[2], mmap_mode = 'r'), 
                       load(subset_path[3], mmap_mode = 'r'),
                       load(subset_path[4], mmap_mode = 'r'), 
                       load(subset_path[5], mmap_mode = 'r')]
        return output_data
    
    #-----------------------------------------------------------------------------------
    dataset_name = ['pivsyn_dataset.npz',]

    subset_names = ['train_x.npy', 
                    'train_y.npy', 
                    'valid_x.npy', 
                    'valid_y.npy', 
                    'test_x.npy' , 
                    'test_y.npy']

    dataset_dir = abspath(dirname(__file__))

    dataset_path = join(dataset_dir, dataset_name[0])

    subset_path = [join(dataset_dir, subset_names[0]),
                        join(dataset_dir, subset_names[1]),
                        join(dataset_dir, subset_names[2]),
                        join(dataset_dir, subset_names[3]),
                        join(dataset_dir, subset_names[4]),
                        join(dataset_dir, subset_names[5])]

    dataset_url = 'https://zenodo.org/record/7935215/files/pivsyn_dataset.npz?download=1'

    check_data(dataset_dir, dataset_name[0], subset_names)

    output_data = import_data(subset_path)
    
    print('\n', 'Data loading successful!')
    return (output_data[0], output_data[1]), (output_data[2], output_data[3]), (output_data[4], output_data[5])