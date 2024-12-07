"""
    # TODO: I think we should move this file to 
    'yta_multimedia.video.frames' instead.
"""
from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.frames.video_frame import VideoFrame
from yta_general_utils.color import Color
from yta_general_utils.programming.parameter_validator import NumberValidator
from moviepy.editor import ColorClip, VideoClip
from typing import Union


class ClipGenerator:
    @staticmethod
    def get_default_background_video(duration: float = 1 / 60):
        """
        Default full opaque black background video that lasts
        (1 / 60) seconds that represents our default moviepy
        scenario of 1920x1080 dimensions. This background is
        used for the basic position calculations. Check the
        transparent option if you are planning to stack some
        videos.
        """
        return ClipGenerator.generate_color_background((1920, 1080), [0, 0, 0], duration, 60, 1.0)
    
    @staticmethod
    def get_default_transparent_background_video(duration: float = 1 / 60):
        """
        Default full transparent background video that lasts
        (1 / 60) seconds and represents our default moviepy
        scenario of 1920x1080 dimensions. This background is
        used for the basic position calculations and, as it 
        is transparent, it should be perfect to work when
        layering other videos.
        """
        return ClipGenerator.generate_color_background((1920, 1080), [0, 0, 0], duration, 60, 0.0)

    @staticmethod
    def generate_color_background(size: tuple, color: Union[Color, 'ColorString', str], duration: float = 1 / 60, fps: int = 60, opacity: float = 1.0):
        color = Color.parse(color)
        ClipValidator.validate_size(size)
        ClipValidator.validate_duration(duration)
        ClipValidator.validate_fps(fps)
        ClipValidator.validate_opacity(opacity)
        
        color_clip = ColorClip(size, color, duration = duration).set_fps(fps)

        # A full opaque clip doesn't need a mask because it is,
        # by definition, full opaque
        if opacity < 1.0:
            color_clip = color_clip.set_mask(MaskGenerator.get_uniform_mask(color_clip.size, color_clip.duration, color_clip.fps, opacity))

        return color_clip

class ClipValidator:
    """
    Class to simplify parameter validation while working
    with moviepy clips and clip parameters.
    """
    @staticmethod
    def validate_size(size: tuple):
        # TODO: Check if tuple like (1920, 1080) with 2 values
        # and values between X and Y
        # Create PythonValidator.is_tuple() and more helpers
        
        return True
    
    @staticmethod
    def validate_duration(duration: float):
        # TODO: We could maybe accept 'fps' parameter to check
        # if 'duration' is a multiple
        if not NumberValidator.is_positive_number(duration, False):
            raise Exception('The provided "duration" is not a positive number.')
        
        return True
    
    @staticmethod
    def validate_fps(fps: int):
        if not NumberValidator.is_positive_number(fps) or not NumberValidator.is_int(fps):
            raise Exception('The provided "fps" is not a positive integer number.')
        
        return True
    
    @staticmethod
    def validate_opacity(opacity: float):
        if not NumberValidator.is_number_between(opacity, 0.0, 1.0):
            raise Exception('The provided "opacity" is not a float value between 1.0 and 0.0.')
        
        return True

class MaskGenerator:
    @staticmethod
    def get_uniform_mask(size: tuple = (1920, 1080), duration: float = 1 / 60, fps: int = 60, opacity: float = 1.0):
        """
        Get a ColorClip of the 'opacity' provided, where 1.0 indicates
        full opaque and 0.0 full transparent, to be used as a mask. 
        
        This is called uniform because it uses a ColorClip that doesn't
        change along its duration time.
        """
        ClipValidator.validate_size(size)
        ClipValidator.validate_duration(duration)
        ClipValidator.validate_fps(fps)
        ClipValidator.validate_opacity(opacity)
        
        return ColorClip(size, opacity, ismask = True, duration = duration).set_fps(fps)

    @staticmethod
    def get_uniform_opaque_mask(size: tuple = (1920, 1080), duration: float = 1 / 60, fps: int = 60):
        """
        Get a mask clip of the provided 'size' that is completely
        opaque and can be set as the mask of any other normal clip.
        
        This is called uniform because it uses a ColorClip that 
        doesn't change along its duration time.
        """
        return MaskGenerator.get_uniform_mask(size, duration, fps, 1)
    
    @staticmethod
    def get_uniform_transparent_mask(size: tuple = (1920, 1080), duration: float = 1 / 60, fps: int = 60):
        """
        Get a maskclip  of the provided 'size' that is completely
        transparent and can be set as the mask of any other normal
        clip.

        This is called uniform because it uses a ColorClip that 
        doesn't change along its duration time.
        """
        return MaskGenerator.get_uniform_mask(size, duration, fps, 0)
    
    @staticmethod
    def video_to_mask(video: VideoClip):
        """
        Turn the provided 'video' into a mask VideoClip that can be
        set as the mask of any other normal clip.
        """
        video = VideoParser.to_moviepy(video)

        # TODO: This is ok but very slow I think...
        mask_clip_frames = [VideoFrame(frame).as_mask() for frame in video.iter_frames()]

        return VideoClip(lambda t: mask_clip_frames[int(t * video.fps)], ismask = True).set_fps(video.fps)

