from yta_multimedia.video.frames.numpy_frame_helper import NumpyFrameHelper
from yta_general_utils.image.parser import ImageParser

import numpy as np


WHITE = [255, 255, 255]
BLACK = [0, 0, 0]

class VideoFrameHandler:
    """
    Class to encapsulate functionality related to moviepy
    video frame handling.
    """
    # TODO: This method should be in Image utils
    @staticmethod
    def is_pure_black_and_white_image(image):
        """
        Check if the provided 'image' only contains pure 
        black ([0, 0, 0]) and white ([255, 255, 255]) colors.
        """
        image = ImageParser.to_numpy(image)

        if np.any(~np.all((image == WHITE) | (image == BLACK), axis = -1)):
            return False
        
        return True
    
    @staticmethod
    def pure_black_and_white_image_to_moviepy_mask_numpy_array(image):
        """
        Turn the received 'image' (that must be a pure black
        and white image) to a numpy array that can be used as
        a moviepy mask (by using ImageClip).

        This is useful for static processed images that we 
        want to use as masks, such as frames to decorate our
        videos.
        """
        image = ImageParser.to_numpy(image)

        if not VideoFrameHandler.is_pure_black_and_white_image(image):
            raise Exception(f'The provided "image" parameter "{str(image)}" is not a black and white image.')

        # Image to a numpy parseable as moviepy mask
        mask = np.zeros(image.shape[:2], dtype = int) # 3col to 1col
        mask[np.all(image == WHITE, axis = -1)] = 1 # white to 1 value

        return mask
    
    def frame_to_pure_black_and_white_image(frame):
        """
        Process the provided moviepy clip mask frame (that
        must have values between 0.0 and 1.0) or normal clip
        frame (that must have values between 0 and 255) and
        convert it into a pure black and white image (an
        image that contains those 2 colors only).

        This method returns a not normalized numpy array of only
        2 colors (pure white [255, 255, 255] and pure black
        [0, 0, 0]), perfect to turn into a mask for moviepy clips.

        This is useful when handling an alpha transition video 
        that can include (or not) an alpha layer but it is also
        clearly black and white so you transform it into a mask
        to be applied on a video clip.
        """
        frame = ImageParser.to_numpy(frame)

        if not VideoFrameHandler.frame_is_mask_clip_frame(frame) and not VideoFrameHandler.frame_is_normal_clip_frame(frame):
            raise Exception('The provided "frame" parameter is not a moviepy mask clip frame nor a normal clip frame.')
        
        if VideoFrameHandler.frame_is_normal_clip_frame(frame):
            # TODO: Process it with some threshold to turn it
            # into pure black and white image (only those 2
            # colors) to be able to transform them into a mask.
            threshold = 220
            white_pixels = np.all(frame >= threshold, axis = -1)

            # Image to completely and pure black
            new_frame = np.array(frame)
            
            # White pixels to pure white
            new_frame[white_pixels] = [255, 255, 255]
            new_frame[~white_pixels] = [0, 0, 0]
        elif VideoFrameHandler.frame_is_mask_clip_frame(frame):
            transparent_pixels = frame == 1

            new_frame = np.array(frame)
            
            # Transparent pixels to pure white
            new_frame[transparent_pixels] = [255, 255, 255]
            new_frame[~transparent_pixels] = [0, 0, 0]

        return new_frame
    
    @staticmethod
    def frame_is_normal_clip_frame(frame: np.ndarray):
        """
        Checks if the provided 'frame' numpy array is recognized as
        a frame of a normal moviepy clip with values between 0 and
        255.

        This numpy array should represent a frame of a clip.
        
        A non-modified clip is '.ndim = 3' and '.dtype = np.uint8'.
        """
        return NumpyFrameHelper.is_rgb_not_normalized(frame)
        
    @staticmethod
    def frame_is_mask_clip_frame(frame: np.ndarray):
        """
        Checks if the provided 'mask_clip' numpy array is recognized
        as an original moviepy mask clip with values between 0 and 1.
        This numpy array should represent a frame of a mask clip.
        
        A non-modified mask clip is '.ndim = 2' and '.dtype = np.float64'.
        """
        return NumpyFrameHelper.is_alpha_normalized(frame)
        
    @staticmethod
    def invert_frame(frame: np.ndarray):
        """
        Invert the values of the provided 'frame', that can be
        a moviepy normal clip frame (with values between 0 and
        255) or a mask clip frame (with values between 0 and 1).

        This method invert the values by applying the max value
        (255 for normal frame, 1 for mask frame) minus each value
        in the numpy array.

        This method returns the numpy array inverted.
        """
        if not VideoFrameHandler.frame_is_normal_clip_frame(frame) and not VideoFrameHandler.frame_is_mask_clip_frame(frame):
            raise Exception('The provided "frame" is not actually a moviepy normal clip frame nor a mask clip frame.')
        
        if VideoFrameHandler.frame_is_normal_clip_frame(frame):
            frame = 255 - frame
        elif VideoFrameHandler.frame_is_mask_clip_frame(frame):
            frame = 1 - frame

        return frame
    
    @staticmethod
    def frame_to_mask_frame(frame: np.ndarray):
        """
        Turn the provided 'frame', that must be represented by
        RGB pixel values ([0-255, 0-255, 0-255]), to a mask
        frame represented by a single value between 0 and 1
        ([0.0-1.0]).
        """
        frame = ImageParser.to_numpy(frame)

        if not VideoFrameHandler.frame_is_normal_clip_frame(frame):
            raise Exception('The provided "frame" is not actually a moviepy normal clip frame.')
        
        frame = np.mean(frame, axis = -1) / 255.0

        return frame
    