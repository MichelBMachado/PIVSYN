#-----------------------------------------------------------------------------------
# CODE DETAILS
#-----------------------------------------------------------------------------------
# Author: Michel Bernardino Machado 
# Date:
# version:

#-----------------------------------------------------------------------------------
# REQUIRED PACKAGES
#-----------------------------------------------------------------------------------
from keras.utils import Sequence
from keras.backend import clear_session
from numpy import ceil
from ..common_tools.preprocessors import preprocess_data
import gc

#-----------------------------------------------------------------------------------
# CODE ROUTINES
#-----------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------
class batch_data(Sequence):
	"""
	A class to provide a custom keras generator with batching, and user customized
	pre-processing routines.
	"""

	#===============================================================================
	def __init__(self, x, y, batch_size):
		"""
		Future docstring
		"""
		self.x = x
		self.y = y
		self.batch_size = batch_size
		self.samples = len(self.x)
		self.x_preprocessor = preprocess_data()
		self.y_preprocessor = preprocess_data()

	#===============================================================================
	def __len__(self):
		"""
		Future docstring
		"""
		return int(ceil(self.samples / self.batch_size))
	
	#===============================================================================
	def add_x_preprocessing_operation(self, operation):
		"""
		Future docstring
		"""
		self.x_preprocessor.add_operation(operation)
	
	#===============================================================================
	def add_y_preprocessing_operation(self, operation):
		"""
		Future docstring
		"""
		self.y_preprocessor.add_operation(operation)
	
	#===============================================================================
	def __getitem__(self, index):
		"""
		Future docstring
		"""
		holder_x = self.x[index * self.batch_size : (index + 1) * self.batch_size]
		holder_y = self.y[index * self.batch_size : (index + 1) * self.batch_size]

		batch_x = self.x_preprocessor.preprocess_batch(holder_x)
		batch_y = self.y_preprocessor.preprocess_batch(holder_y)

		return batch_x, batch_y
	