
from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.frames.video_frame_extractor import VideoFrameExtractor
from yta_multimedia.video.generation import generate_video_from_image
from yta_multimedia.video.edition.effect.speed.change_speed_effect import ChangeSpeedVideoEffect
from yta_general_utils.programming.enum import YTAEnum as Enum
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, ColorClip, concatenate_videoclips
from typing import Union


# TODO: Move this to a better place
class ExtendVideoMode(Enum):
    """
    This is a Enum to set the parameter option to extend the video
    duration with one of these modes (strategies).
    """
    LOOP = 'loop'
    """
    This mode will make the video loop (restart from the begining)
    until it reaches the expected duration.
    """
    FREEZE_LAST_FRAME = 'freeze_last_frame'
    """
    This mode will freeze the last frame of the video and extend 
    it until it reaches the expected duration.
    """
    SLOW_DOWN = 'slow_down'
    """
    This mode will change the speed of the provided video to make
    it fit the needed duration by deccelerating it. As you should
    know, this method changes the whole video duration so the 
    result could be unexpected. Use it carefully.
    """
    SPEED_UP_OR_SLOW_DOWN = 'speed_up_or_slow_down'
    """
    This mode will change the speed of the provided video to make
    it fit the needed duration by accelerating or deccelerating 
    it. This will speed up the video if the requested duration is
    shorter than the provided 'video', or will slow it down if it
    is larger. The result could be not as good as expected because
    of the speed change. Use it carefully.
    """
    # TODO: This was thought to enlarge the video if needed and 
    # only subclip it if 'duration' was less than the real video
    # duration, but now we are able to speed it up instead of 
    # subclipping the video. Maybe we need 'enshort_mode' and
    # 'enlarge_mode' instead of only 'mode' parameter to be able
    # to chose both strategies. This will simplify the if logic
    # and make it more customizable but being solid.


def set_video_duration(video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip, ColorClip], duration = float, mode: ExtendVideoMode = ExtendVideoMode.LOOP):
    """
    This method will return a copy of the provided 'video' with the desired
    'duration' by applying crops or loops. If the provided 'duration' is
    lower than the actual 'video' duration, it will be shortened. If it is
    greater, it will be looped until we reach the desired 'duration'.

    The 'mode' provided will determine the way in which we extend the video
    duration if needed.

    This method makes a 'video.copy()' internally to work and avoid problems.
    """
    video = VideoParser.to_moviepy(video)

    if not duration:
        raise Exception('No "duration" provided.')
    
    if not mode:
        mode = ExtendVideoMode.LOOP
    else:
        mode = ExtendVideoMode.to_enum(mode)

    final_video = video.copy()

    if video.duration > duration:
        # TODO: Take a look at the TODO on the top, please
        if mode == ExtendVideoMode.SPEED_UP_OR_SLOW_DOWN:
            final_video = ChangeSpeedVideoEffect.apply(final_video, duration)
        else:
            final_video = final_video.subclip(0, duration)
    elif video.duration < duration:
        if mode == ExtendVideoMode.LOOP:
            times_to_loop = (int) (duration / video.duration) - 1
            remaining_time = duration % video.duration
            for _ in range(times_to_loop):
                final_video = concatenate_videoclips([final_video, video])
            final_video = concatenate_videoclips([final_video, video.subclip(0, remaining_time)])
        elif mode == ExtendVideoMode.FREEZE_LAST_FRAME:
            remaining_time = duration - video.duration
            frame = VideoFrameExtractor.get_frame_by_time(video, video.duration)
            frame_freezed_video = generate_video_from_image(frame, remaining_time)
            final_video = concatenate_videoclips([video, frame_freezed_video])
        elif mode in [ExtendVideoMode.SLOW_DOWN, ExtendVideoMode.SPEED_UP_OR_SLOW_DOWN]:
            final_video = ChangeSpeedVideoEffect.apply(final_video, duration)

    return final_video