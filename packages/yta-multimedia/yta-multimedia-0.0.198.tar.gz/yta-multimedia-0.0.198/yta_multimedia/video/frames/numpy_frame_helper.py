from yta_multimedia.video.frames.enums import FrameMaskingMethod
from yta_general_utils.image.parser import ImageParser
from typing import Union

import numpy as np


class NumpyFrameHelper:
    """
    Class to encapsulate functionality related to numpy
    frames. Numpy frames are frames with width and height,
    and 1 or 3 values per pixel (per cell).
    """

    @staticmethod
    def normalize(frame: np.ndarray, do_check: bool = True):
        """
        Normalize the frame if not normalized.
        """
        if do_check and NumpyFrameHelper.is_rgb_not_normalized(frame) or NumpyFrameHelper.is_alpha_not_normalized(frame) or NumpyFrameHelper.is_rgba_not_normalized(frame):
            frame = frame / 255.0

        return frame

    @staticmethod
    def denormalize(frame: np.ndarray, do_check: bool = True):
        """
        Denormalize the frame if normalized.
        """
        if do_check and NumpyFrameHelper.is_rgb_normalized(frame) or NumpyFrameHelper.is_alpha_normalized(frame) or NumpyFrameHelper.is_rgba_normalized(frame):
            frame = (frame * 255).astype(np.uint8)

        return frame
    
    @staticmethod
    def is_normalized(frame: np.ndarray):
        """
        Check if the provided frame is a a normalized one, which
        means that its type is .float64 or .float32 and that all
        values are between 0.0 and 1.0.
        """
        frame = ImageParser.to_numpy(frame)

        return frame.dtype in (np.float64, np.float32) and np.all((frame >= 0.0) & (frame <= 1.0))

    @staticmethod
    def is_not_normalized(frame: np.ndarray):
        """
        Check if the provided frame is not a normalized one, which
        means that its type is .uint8 and that all values are 
        between 0 and 255.
        """
        frame = ImageParser.to_numpy(frame)
        
        return frame.dtype == np.uint8 and np.all((frame >= 0) & (frame <= 255))

    @staticmethod
    def is_rgb(frame: np.ndarray, is_normalized: Union[None, bool] = None):
        """
        Check if the provided 'frame' is an RGB frame, which means
        that its dimension is 3 and its shape is also 3 per pixel.

        If 'is_normalized' is provided, it will check if the frame
        is normalized or not according to the boolean value passed
        as parameter.
        """
        frame = ImageParser.to_numpy(frame)

        is_rgb = frame.ndim == 3 and frame.shape[2] == 3

        if is_normalized is None:
            return is_rgb
        
        if is_normalized:
            return is_rgb and NumpyFrameHelper.is_normalized(frame)
        
        return is_rgb and NumpyFrameHelper.is_not_normalized(frame)

    @staticmethod
    def is_rgba(frame: np.ndarray, is_normalized: Union[None, bool] = None):
        """
        Check if the provided 'frame' is an RGBA frame, which means
        that its dimension is 3 and its shape is 4 per pixel.

        If 'is_normalized' is provided, it will check if the frame
        is normalized or not according to the boolean value passed
        as parameter.

        TODO: This is not actually a frame we can use in moviepy
        videos, but it could be a frame we build to later decompose
        in clip and mask clip, so I keep the code. Maybe it is 
        useless in the future and thats why this is a TODO.
        """
        frame = ImageParser.to_numpy(frame)

        is_rgba = frame.ndim == 3 and frame.shape[2] == 4

        if is_normalized is None:
            return is_rgba
        
        if is_normalized:
            return is_rgba and NumpyFrameHelper.is_normalized(frame)
        
        return is_rgba and NumpyFrameHelper.is_not_normalized(frame)
    
    @staticmethod
    def is_alpha(frame: np.ndarray, is_normalized: Union[None, bool] = None):
        """
        Check if the provided 'frame' is an alpha frame, which means
        that its dimension is 2 because there is only one single
        value per pixel.

        
        If 'is_normalized' is provided, it will check if the frame
        is normalized or not according to the boolean value passed
        as parameter.
        """
        frame = ImageParser.to_numpy(frame)

        # if not PythonValidator.is_numpy_array(frame):
        #     raise Exception('The provided "frame" parameter is not a numpy array.')

        is_alpha = frame.ndim == 2

        if is_normalized is None:
            return is_alpha
        
        if is_normalized:
            return is_alpha and NumpyFrameHelper.is_normalized(frame)
        
        return is_alpha and NumpyFrameHelper.is_not_normalized(frame)

    @staticmethod
    def is_rgb_not_normalized(frame: np.ndarray):
        """
        Check if the provided 'frame' is a numpy array of
        ndim = 3, dtype = np.uint8 and all the values (3)
        are between 0 and 255.
        """
        return NumpyFrameHelper.is_rgb(frame, is_normalized = False)
    
    @staticmethod
    def is_rgb_normalized(frame: np.ndarray):
        """
        Check if the provided 'frame' is a numpy array of
        ndim = 3, dtype = np.float64|np.float32 and all 
        the values (3) are between 0.0 and 1.0.
        """
        return NumpyFrameHelper.is_rgb(frame, is_normalized = True)

    @staticmethod
    def is_rgba_normalized(frame: np.ndarray):
        return NumpyFrameHelper.is_rgba(frame, is_normalized = True)
    
    @staticmethod
    def is_rgba_not_normalized(frame: np.ndarray):
        return NumpyFrameHelper.is_rgba(frame, is_normalized = False)

    @staticmethod
    def is_alpha_normalized(frame: np.ndarray):
        return NumpyFrameHelper.is_alpha(frame, is_normalized = True)

    @staticmethod
    def is_alpha_not_normalized(frame: np.ndarray):
        return NumpyFrameHelper.is_alpha(frame, is_normalized = False)

    @staticmethod
    def to_rgb(frame: np.ndarray, do_normalize: bool = False):
        """
        Turn the provided 'frame' to a normal (rgb) frame,
        normalized or not according to the provided as
        'do_normalize' parameter.

        This method will return a numpy array containing 3
        values for each pixel, and each one for them will be
        from 0.0 to 1.0 if normalized, or from 0 to 255 if
        not normalized.

        A default moviepy frame is a numpy array of 3 values
        per pixel from 0 to 255.
        """
        if NumpyFrameHelper.is_alpha_normalized(frame):
            frame = np.stack((frame, frame, frame), axis = -1)
            if not do_normalize:
                frame = NumpyFrameHelper.denormalize(frame, do_check = False)
        if NumpyFrameHelper.is_alpha_not_normalized(frame):
            frame = np.stack((frame, frame, frame), axis = -1)
            if do_normalize:
                frame = NumpyFrameHelper.normalize(frame, do_check = False)
        elif NumpyFrameHelper.is_rgb_normalized(frame):
            if not do_normalize:
                frame = NumpyFrameHelper.denormalize(frame, do_check = False)
        elif NumpyFrameHelper.is_rgb_not_normalized(frame):
            if do_normalize:
                frame = NumpyFrameHelper.normalize(frame, do_check = False)
        elif NumpyFrameHelper.is_rgba_normalized(frame):
            frame = frame[:, :, :3]
            if not do_normalize:
                frame = NumpyFrameHelper.denormalize(frame, do_check = False)
        elif NumpyFrameHelper.is_rgba_not_normalized(frame):
            frame = frame[:, :, :3]
            if do_normalize:
                frame = NumpyFrameHelper.normalize(frame, do_check = False)
        else:
            raise Exception('The provided "frame" is not recognized as a valid frame (RGB, RGBA or alpha).')

        return frame
    
    @staticmethod
    def to_alpha(frame: np.ndarray, do_normalize: bool = True, masking_method: FrameMaskingMethod = FrameMaskingMethod.MEAN):
        """
        Turn the provided 'frame' to an alpha frame, normalized
        or not according to the provided as 'do_normalize'
        parameter.

        This method will return a numpy array containing one
        single value for each pixel, that will be from 0.0 to
        1.0 if normalized, or from 0 to 255 if not normalized.

        A default moviepy mask frame is a numpy array of one
        single value per pixel from 0.0 to 1.0.

        The 'masking_method' will determine the method that is
        needed to be used to turn the normal frame into a mask
        frame.
        """
        masking_method = FrameMaskingMethod.to_enum(masking_method)

        if NumpyFrameHelper.is_alpha_normalized(frame):
            if not do_normalize:
                frame = NumpyFrameHelper.denormalize(frame, do_check = False)
        if NumpyFrameHelper.is_alpha_not_normalized(frame):
            frame = np.stack((frame, frame, frame), axis = -1)
            if do_normalize:
                frame = NumpyFrameHelper.normalize(frame, do_check = False)
        elif NumpyFrameHelper.is_rgb_normalized(frame):
            frame = masking_method.to_mask_frame(frame)
            if not do_normalize:
                frame = NumpyFrameHelper.denormalize(frame, do_check = False)
        elif NumpyFrameHelper.is_rgb_not_normalized(frame):
            frame = masking_method.to_mask_frame(frame)
            if do_normalize:
                frame = NumpyFrameHelper.normalize(frame, do_check = False)
        elif NumpyFrameHelper.is_rgba_normalized(frame):
            frame = frame[:, :, :3]
            frame = masking_method.to_mask_frame(frame)
            if not do_normalize:
                frame = NumpyFrameHelper.denormalize(frame, do_check = False)
        elif NumpyFrameHelper.is_rgba_not_normalized(frame):
            frame = frame[:, :, :3]
            frame = masking_method.to_mask_frame(frame)
            if do_normalize:
                frame = NumpyFrameHelper.normalize(frame, do_check = False)
        else:
            raise Exception('The provided "frame" is not recognized as a valid frame (RGB, RGBA or alpha).')

        return frame

    def invert(frame: np.ndarray):
        """
        Invert the provided array according to if it is a normalized
        or a not normalized one.
        """
        if NumpyFrameHelper.is_normalized():
            frame = 1.0 - frame
        elif NumpyFrameHelper.is_not_normalized():
            frame = 255 - frame
        else:
            raise Exception('The provided "frame" is not a normalized array nor a not normalized one.')
        
        return frame

# TODO: Maybe a NumpyHelper to make reusable methods
# such as 'as_zeros(array)' to get a similar one but
# filled with zeros, to calculate the mean