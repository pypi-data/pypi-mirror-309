from yta_multimedia.video.frames.video_frame_handler import VideoFrameHandler
from yta_general_utils.file.checker import FileValidator
from yta_general_utils.file.enums import FileType
from yta_general_utils.file.filename import filename_is_type
from yta_general_utils.programming.parameter_validator import PythonValidator
from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip, ImageClip, ImageSequenceClip, VideoClip
from typing import Union


class VideoParser:
    """
    Class to simplify the way we parse video parameters.
    """
    @classmethod
    def to_moviepy(cls, video: Union[str, VideoFileClip, CompositeVideoClip, ColorClip, ImageClip], do_include_mask: bool = False, do_check_duration: bool = False):
        """
        This method is a helper to turn the provided 'video' to a moviepy
        video type. If it is any of the moviepy video types specified in
        method declaration, it will be returned like that. If not, it will
        be load as a VideoFileClip if possible, or will raise an Exception
        if not.

        The 'do_include_mask' parameter includes the mask in the video if
        True value provided. The 'do_check_duration' parameter checks and
        updates the real video duration to fix a bug in moviepy lib.
        """
        if not video:
            raise Exception('No "video" provided.')
        
        # TODO: Maybe check if subclass of VideoClip
        if not PythonValidator.is_string(video) and not PythonValidator.is_instance(video, VideoFileClip) and not PythonValidator.is_instance(video, CompositeVideoClip) and not PythonValidator.is_instance(video, ColorClip) and not PythonValidator.is_instance(video, ImageClip) and not PythonValidator.is_instance(video, ImageSequenceClip) and not PythonValidator.is_instance(video, VideoClip):
            raise Exception('The "video" parameter provided is not a valid type. Check valid types in method declaration.')
        
        if PythonValidator.is_string(video):
            if not filename_is_type(video, FileType.VIDEO):
                raise Exception('The "video" parameter provided is not a valid video filename.')
            
            if not FileValidator.file_is_video_file(video):
                raise Exception('The "video" parameter is not a valid video file.')
            
            video = VideoFileClip(video, has_mask = do_include_mask)

        if do_check_duration:
            # We need to fix an existing bug in moviepy lib
            # see https://github.com/Zulko/moviepy/issues/1826
            video = verify_and_update_duration(video)

        # TODO: This below just adds a mask attribute but
        # without fps and empty, so it doesn't make sense
        # if do_include_mask and not video.mask:
        #     video = video.add_mask()

        return video
    
    @staticmethod
    def is_normal_clip(clip: Union[str, VideoClip]):
        """
        Normal clips have frames as numpy arrays with values between
        0 and 255 (where 255 means full of color).

        A non-modified clip is '.ndim = 3' and '.dtype = uint8'.
        """
        clip = VideoParser.to_moviepy(clip)

        # TODO: Should I do 'is_subclass' instead of 'is_instance' (?)
        # TODO: I'm not sure, maybe a CompositeVideoClip is a mask (?)
        if not PythonValidator.is_instance(clip, VideoClip):
            # TODO: False or Exception (?)
            raise Exception('The provided "clip" parameter is not a moviepy VideoClip instance.')
        
        return VideoFrameHandler.frame_is_normal_clip_frame(clip.get_frame(t = 0))

    @staticmethod
    def is_mask_clip(clip: Union[str, VideoClip]):
        """
        Mask clips have frames as numpy arrays with values only between
        0.0 and 1.0 (where 1.0 means completely opaque). 
        
        A non-modified mask is '.ndim = 2' and '.dtype = float64'.
        """
        clip = VideoParser.to_moviepy(clip)

        # TODO: Should I do 'is_subclass' instead of 'is_instance' (?)
        # TODO: I'm not sure, maybe a CompositeVideoClip is a mask (?)
        if not PythonValidator.is_instance(clip, VideoClip):
            # TODO: False or Exception (?)
            raise Exception('The provided "clip" parameter is not a moviepy VideoClip instance.')

        return VideoFrameHandler.frame_is_mask_clip_frame(clip.get_frame(t = 0))

def verify_and_update_duration(video):
    """
    Try to subclip the provided 'video' with the last
    frames detected by moviepy and check if the duration
    is the real one and updates it if not. This method
    returns the video updated to the its new duration.

    Moviepy has a bug in which some videos are detected
    larger than they actually are, and that makes the 
    software fails when trying to work with all those 
    wrong detected videos.

    When trying to subclip a moviepy video, the system
    will fail when the 't_start' parameter is larger or
    equal to the actual video duration (not the one
    detected by moviepy), so we are using that slow
    function to detect the real duration and updating
    the video accordingly.
    """
    frame_time = 1 / video.fps
    
    for frame_number in reversed(range(int(video.fps * video.duration))):
        try:
            real_duration = frame_number * frame_time
            video.subclip(real_duration, 9999)
            # 't_start' can't be the last frame but the penultimate
            # so the real duration is one 'frame_time' later
            real_duration += frame_time
            break
        except:
            pass

    video = video.subclip(0, real_duration)

    return video