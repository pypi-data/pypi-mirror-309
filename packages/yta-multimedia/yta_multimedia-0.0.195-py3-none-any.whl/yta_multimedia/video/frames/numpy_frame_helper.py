from yta_general_utils.programming.parameter_validator import PythonValidator
from yta_general_utils.image.parser import ImageParser

import numpy as np


class NumpyFrameHelper:
    """
    Class to encapsulate functionality related to numpy
    frames.
    """
    @staticmethod
    def is_rgb_not_normalized(frame: np.ndarray):
        """
        Check if the provided 'frame' is a numpy array of
        ndim = 3, dtype = np.uint8 and all the values (3)
        are between 0 and 255.
        """
        frame = ImageParser.to_numpy(frame)

        if not PythonValidator.is_numpy_array(frame):
            raise Exception('The provided "frame" parameter is not a numpy array.')
        
        return frame.ndim == 3 and frame.dtype == np.uint8 and frame.shape[2] == 3 and np.all((frame >= 0) & (frame <= 255))
    
    @staticmethod
    def is_rgb_normalized(frame: np.ndarray):
        """
        Check if the provided 'frame' is a numpy array of
        ndim = 3, dtype = np.float64|np.float32 and all 
        the values (3) are between 0.0 and 1.0.
        """
        frame = ImageParser.to_numpy(frame)

        if not PythonValidator.is_numpy_array(frame):
            raise Exception('The provided "frame" parameter is not a numpy array.')
        
        return frame.ndim == 3 and frame.dtype in (np.float64, np.float32) and frame.shape[2] == 3 and np.all((frame >= 0.0) & (frame <= 1.0))
    
    @staticmethod
    def is_rgba_not_normalized(frame: np.ndarray):
        """
        Check if the provided 'frame' is a numpy array of
        ndim = 3, dtype = np.uint8 and all the values (4)
        are between 0 and 255.
        """
        """
        Check if the provided 'frame' is a numpy array of
        ndim = 3, dtype = np.uint8 and all the values (3)
        are between 0 and 255.
        """
        frame = ImageParser.to_numpy(frame)

        if not PythonValidator.is_numpy_array(frame):
            raise Exception('The provided "frame" parameter is not a numpy array.')
        
        return frame.ndim == 3 and frame.dtype == np.uint8 and frame.shape[2] == 4 and np.all((frame >= 0) & (frame <= 255))
    
    @staticmethod
    def is_rgba_normalized(frame: np.ndarray):
        """
        Check if the provided 'frame' is a numpy array of
        ndim = 3, dtype = np.float64|np.float32 and all 
        the values (4) are between 0.0 and 1.0.
        """
        frame = ImageParser.to_numpy(frame)

        if not PythonValidator.is_numpy_array(frame):
            raise Exception('The provided "frame" parameter is not a numpy array.')
        
        return frame.ndim == 3 and frame.dtype in (np.float64, np.float32) and frame.shape[2] == 4 and np.all((frame >= 0.0) & (frame <= 1.0))
    
    @staticmethod
    def is_alpha_not_normalized(frame: np.ndarray):
        """
        Check if the provided 'frame' is a numpy array of
        ndim = 2, dtype = np.uint8 and all
        the values are between 0 and 255.
        """
        frame = ImageParser.to_numpy(frame)

        if not PythonValidator.is_numpy_array(frame):
            raise Exception('The provided "frame" parameter is not a numpy array.')
        
        return frame.ndim == 2 and frame.dtype == np.uint8 and np.all((frame >= 0) & (frame <= 255))

    @staticmethod
    def is_alpha_normalized(frame: np.ndarray):
        """
        Check if the provided 'frame' is a numpy array of
        ndim = 2, dtype = np.float64|np.float32 and all
        the values are between 0.0 and 1.0.
        """
        frame = ImageParser.to_numpy(frame)

        if not PythonValidator.is_numpy_array(frame):
            raise Exception('The provided "frame" parameter is not a numpy array.')
        
        return frame.ndim == 2 and frame.dtype in (np.float64, np.float32) and np.all((frame >= 0.0) & (frame <= 1.0))

