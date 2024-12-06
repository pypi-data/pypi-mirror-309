from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.frames.video_frame_handler import VideoFrameHandler
from yta_general_utils.image.parser import ImageParser
from yta_general_utils.programming.enum import YTAEnum as Enum
from moviepy.editor import VideoClip
from typing import Union

import numpy as np


class MoviepyAlphaTransitionProcessingMethod(Enum):
    MEAN = 'mean'
    """
    Calculates the mean value of the RGB pixel color
    values and uses it as a normalized value between
    0.0 and 1.0 to set as transparency.
    """
    PURE_BLACK_AND_WHITE = 'pure_black_and_white'
    """
    Apply a threshold and turn pixels into pure black
    and white pixels, setting them to pure 1.0 or 0.0
    values to be completely transparent or opaque.
    """

class MoviepyAlphaTransitionHandler:
    """
    Class to handle the functionality related to turning
    alpha clips into moviepy mask clips to be able to 
    apply them and create affects and transitions.
    """
    @staticmethod
    def alpha_clip_to_mask_clip(video: Union[str, VideoClip], method: MoviepyAlphaTransitionProcessingMethod = MoviepyAlphaTransitionProcessingMethod.PURE_BLACK_AND_WHITE):
        """
        The provided alpha 'video' is turned into a moviepy
        mask clip that can be set in any other video by
        using the '.set_mask()' method.

        If you apply the resulting mask to a clip (called 
        'video2' in below) then you can do this below to
        enjoy an incredible transition, or using a black
        background instead of the 'video1' in below.

        CompositeVideoClip([
            video,
            video2
        ]).write_videofile('alpha_masked_transition.mp4')
        """
        video = VideoParser.to_moviepy(video, True, True)
        method = MoviepyAlphaTransitionProcessingMethod.to_enum(method)

        transparent_pixel_in_mask = False
        if video.mask:
            for alpha_frame in video.mask.iter_frames():
                if (alpha_frame < 1.0).any():
                    transparent_pixel_in_mask = True

        # If mask has transparency, we keep the mask
        mask_clip = video.mask
        if not transparent_pixel_in_mask:
            if method == MoviepyAlphaTransitionProcessingMethod.MEAN:
                # Frame by frame, to np.mean and use it as mask
                mask_clip_frames = [VideoFrameHandler.frame_to_mask_frame(frame) for frame in video.iter_frames()]
            elif method == MoviepyAlphaTransitionProcessingMethod.PURE_BLACK_AND_WHITE:
                # Frame by frame, to pure black and white image
                # and turn it into a mask
                mask_clip_frames = [frame_to_mask_frame(frame) for frame in video.iter_frames()]
            
            mask_clip = VideoClip(lambda t: mask_clip_frames[int(t * video.fps)], ismask = True).set_fps(video.fps)

        return mask_clip
    
def frame_to_mask_frame(frame: np.ndarray, do_invert_frame: bool = False):
    """
    Turn the 'frame' parameter into a frame that can
    be used as a mask frame. The provided 'frame'
    should be a frame of a alpha transition clip that
    is almost black and white (or has an alpha layer).

    This method will use an specific strategy to set
    pixels as transparent or opaque by converting the
    frame into a pure black and white image.

    You can use the provided 'frame' but inverted if
    'do_invert_frame' is set as True.
    """
    frame = ImageParser.to_numpy(frame)

    if do_invert_frame:
        frame = VideoFrameHandler.invert_frame(frame)

    frame = VideoFrameHandler.pure_black_and_white_image_to_moviepy_mask_numpy_array(VideoFrameHandler.frame_to_pure_black_and_white_image(frame))

    return frame