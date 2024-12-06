from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.frames.video_frame_handler import VideoFrameHandler
from moviepy.editor import VideoClip, VideoClip
from typing import Union


class VideoHandler:
    """
    Class created to simplify and encapsulate the working process
    with moviepy videos.
    """
    @staticmethod
    def invert_video(video: Union[str, VideoClip]):
        """
        Invert the received 'video' (that must be a moviepy 
        mask or normal clip) and return it inverted as a
        VideoClip. If the provided 'video' is a mask, this 
        will be also a mask.

        If the 'clip' provided is a mask clip, remember to
        set it as the new mask of your main clip.

        This inversion is a process in which the numpy array
        values of each frame are inverted by substracting the
        highest value. If the frame is an RGB frame with 
        values between 0 and 255, it will be inverted by 
        doing 255 - X on each frame pixel value. If it is
        normalized and values are between 0 and 1 (it is a 
        mask clip frame), by doing 1 - X on each mask frame
        pixel value.
        """
        video = VideoParser.to_moviepy(video)

        mask_frames = [VideoFrameHandler.invert_frame(frame) for frame in video.iter_frames()]

        return VideoClip(lambda t: mask_frames[int(t * video.fps)], ismask = video.ismask).set_fps(video.fps)