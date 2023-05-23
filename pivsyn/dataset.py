import os
from zipfile import ZipFile 
import numpy as np
import urllib.request
from pathlib import Path
import socket

dataset_dir = os.path.abspath(os.path.dirname(__file__))
dataset_name = 'pivsyn_dataset.npz'
dataset_path = os.path.join(dataset_dir, dataset_name)
dataset_url = 'https://zenodo.org/record/7935215/files/pivsyn_dataset.npz?download=1'
desired_files = ['train_x.npy', 'train_y.npy', 'valid_x.npy', 'valid_y.npy', 'test_x.npy', 'test_y.npy']

def check_file_existance(directory, files):

    file_list = os.listdir(directory)

    for file in files:

        if file not in file_list:

            return False
        
    return True

def get_data(url: str, outfile: Path, overwrite: bool = False):
    
    #urllib.request.urlretrieve(dataset_url, dataset_path)
    outfile = Path(outfile).expanduser().resolve()
    if outfile.is_dir():
        raise ValueError("Please specify full filepath, including filename")
    # need .resolve() in case intermediate relative dir doesn't exist
    if overwrite or not outfile.is_file():
        outfile.parent.mkdir(parents=True, exist_ok=True)
        try:
            urllib.request.urlretrieve(url, str(outfile))
        except (socket.gaierror, urllib.error.URLError) as err:
            raise ConnectionError(
                "could not download {} due to {}".format(url, err)
            )

def extract_data():

    with ZipFile(dataset_path, 'r') as f:

        print('\nExtracting: ', dataset_name)

        f.extractall(path = dataset_dir)

    f.close

def load_data():

    print('\nChecking for PIVSYN dataset ...')

    if check_file_existance(dataset_dir, [dataset_name]):
        print('\nPIVSYN dataset is already downloaded!')
        pass

    else:
        print('\nPIVSYN dataset is not downloaded!')
        print('\nDownloading PIVSYN dataset ...')
        get_data(url = dataset_url, outfile = dataset_path)
        print('\nPIVSYN dataset downloaded!')

    print('\nChecking for splited sets ...')

    if check_file_existance(dataset_dir, desired_files):
        print('\nPIVSYN dataset is already splited!')
        pass
    else:
        print('\nPIVSYN dataset must be splited!')
        extract_data()

    train_x_path = os.path.join(dataset_dir, 'train_x.npy')
    train_y_path = os.path.join(dataset_dir, 'train_y.npy')
    valid_x_path = os.path.join(dataset_dir, 'valid_x.npy')
    valid_y_path = os.path.join(dataset_dir, 'valid_y.npy')
    test_x_path  = os.path.join(dataset_dir, 'test_x.npy' )
    test_y_path  = os.path.join(dataset_dir, 'test_y.npy' )

    print('Loading data ...')
    train_x = np.load(train_x_path, mmap_mode = 'r')
    train_y = np.load(train_y_path, mmap_mode = 'r')
    valid_x = np.load(valid_x_path, mmap_mode = 'r')
    valid_y = np.load(valid_y_path, mmap_mode = 'r')
    test_x  = np.load(test_x_path , mmap_mode = 'r')
    test_y  = np.load(test_y_path , mmap_mode = 'r')
    print('Data loading successful!')

    return (train_x, train_y), (valid_x, valid_y), (test_x, test_y)

