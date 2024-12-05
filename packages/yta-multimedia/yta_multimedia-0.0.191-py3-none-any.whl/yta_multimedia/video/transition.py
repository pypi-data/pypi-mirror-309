from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.edition.effect.moviepy.video_effect import MoviepySetPosition
from yta_multimedia.video.edition.effect.moviepy.t_function import TFunctionSetPosition
from yta_multimedia.video.edition.effect.moviepy.position.objects.coordinate_corner import CoordinateCorner
from yta_multimedia.video.frames.video_frame_extractor import VideoFrameExtractor
from yta_multimedia.video.edition.effect.moviepy.alpha import MoviepyAlphaTransitionHandler, MoviepyAlphaTransitionProcessingMethod
from yta_multimedia.video.edition.duration import set_video_duration, ExtendVideoMode
from yta_general_utils.math.rate_functions import RateFunction
from yta_general_utils.programming.parameter_validator import NumberValidator
from yta_general_utils.programming.error_message import ErrorMessage
from yta_general_utils.programming.parameter_validator import PythonValidator
from yta_general_utils.programming.enum import YTAEnum as Enum
from moviepy.editor import ImageClip, CompositeVideoClip, VideoClip, concatenate_videoclips
from typing import Callable


class TransitionMode(Enum):
    """
    Class to represent the transition modes (the way we
    join the videos between a transition).
    """
    FREEZE = 'freeze'
    """
    Freeze the last frame of the first video and the first
    frame ot he second video and make the transition with
    those static frames so the duration is extended by the
    transition duration.
    """
    PLAYING = 'playing'
    """
    Keep both video playing while the transition is run.
    """

class VideoTransition:
    """
    Class to encapsulate the logic to apply in a video 
    transition, containing the mode of transition and 
    the logic to apply on it.
    """
    mode: TransitionMode
    """
    The mode of transition we want to apply.
    """
    duration: float
    """
    The duration that the transition logic will last being
    applied.
    """
    method: Callable
    """
    The method we want to apply as the transition logic, that
    must be a static function of the Transition class.
    """
    kwargs: list
    """
    Other attributes we could need for some specific type of
    transition generation methods.
    """
    def __init__(self, mode: TransitionMode, duration: float, method: Callable, **kwargs):
        """
        The provided 'method' must be one of the static methods
        existing in the Transition class.
        """
        if not PythonValidator.is_class_staticmethod(TransitionMethod, method):
            raise Exception('The provided "method" parameter is not an static method of the Transition class.')
        
        if not NumberValidator.is_positive_number(duration):
            raise Exception(ErrorMessage.parameter_is_not_positive_number('duration'))
        # TODO: Maybe make 'duration' be multiple of frame_time
        # and multiple of a pair frame_time to allow the 
        # transition work equally in both videos

        mode = TransitionMode.to_enum(mode)
        
        self.mode = mode
        self.duration = duration
        self.method = method
        self.kwargs = kwargs

class Transition:
    """
    Class to encapsulate all the transition methods we
    handle in our system. Each transition is a way of
    connecting two different videos.

    This class is built to be used within the
    TransitionGenerator class as parameter to build 
    videos with those transitions.
    """
    # TODO: Delete this
    # @staticmethod
    # def create_alpha_transition(video1, video2, alpha_video, mode: TransitionMode, duration: float):
    #     """
    #     Create the transition between 'video1' and 'video2' using
    #     the 'alpha_video' as a mask, and return the items once it's
    #     been created in the next order: video1, transition, video2.
    #     """
    #     transition = VideoTransition(mode, duration, TransitionMethod.alpha, alpha_video = alpha_video)

    #     return Transition.create_transition(video1, video2, transition)

    @staticmethod
    def create_transition(video1, video2, transition: VideoTransition = None):
        """
        Create the transition between 'video1' and 'video2' and 
        return the items in the next order: video1, transition,
        video2. Those items are ready to be concatenated in 
        that order to obtain both videos played with the expected
        transition in between.
        """
        video1 = VideoParser.to_moviepy(video1)
        video2 = VideoParser.to_moviepy(video2)
        
        if not PythonValidator.is_instance(transition, VideoTransition):
            raise Exception('The provided "transition" is not a VideoTransition instance.')

        # Handle transition and videos
        if transition.mode == TransitionMode.FREEZE:
            # Original videos are not modified
            transition_first_clip = ImageClip(VideoFrameExtractor.get_last_frame(video1), duration = transition.duration).set_fps(60)
            transition_second_clip = ImageClip(VideoFrameExtractor.get_first_frame(video2), duration = transition.duration).set_fps(60)
        elif transition.mode == TransitionMode.PLAYING:
            if transition.duration > video1.duration or transition.duration > video2.duration:
                # TODO: Make this Exception more description (which video is wrong)
                # and talk about that we use the half of the provided duration
                raise Exception(f'The provided "transition.duration" parameter {str(transition.duration)} is not valid according to the provided video duration.')
            
            transition_first_clip = video1.subclip(video1.duration - transition.duration, video1.duration)
            transition_second_clip = video2.subclip(0, transition.duration)
            video1 = video1.subclip(0, video1.duration - transition.duration)
            video2 = video2.subclip(transition.duration, video2.duration)
        
        return video1, transition.method(video1 = transition_first_clip, video2 = transition_second_clip, **transition.kwargs), video2
    
class TransitionMethod:
    """
    This class is for internal use only. It is used by
    the TransitionGenerator class to generate clip
    transitions.

    This class encapsulates the functionality to generate 
    transition clips and the different methods to build
    them.
    """
    @staticmethod
    def slide(video1: VideoClip, video2: VideoClip, **kwargs):
        """
        Simple transition in which the last frame of the provided 'video1'
        is replaced by the first frame of the provided 'video2' by sliding
        from right to left.
        """
        video1 = VideoParser.to_moviepy(video1)
        video2 = VideoParser.to_moviepy(video2)

        # TODO: I was working before in setting the position
        # constants so I could use them to easily handle slides
        # from different sides of the screen

        # Transition from last frame of video1 to first of video2
        transition_clip_1 = MoviepySetPosition(CoordinateCorner(0, 0), CoordinateCorner(-video1.w, 0), TFunctionSetPosition.linear, RateFunction.linear).apply(video1)
        # TODO: Maybe set 'transition_clip_1.pos' instead of (0, 0)
        transition_clip_2 = MoviepySetPosition(CoordinateCorner(video2.w, 0), CoordinateCorner(0, 0), TFunctionSetPosition.linear, RateFunction.linear).apply(video2)

        return CompositeVideoClip([
            transition_clip_1,
            transition_clip_2
        ])
    
    @staticmethod
    def alpha(video1: VideoClip, video2: VideoClip, alpha_video: VideoClip, alpha_processing_method: MoviepyAlphaTransitionProcessingMethod = MoviepyAlphaTransitionProcessingMethod.MEAN, **kwargs):
        """
        Transition that involves an alpha clip in between the
        two provided 'video1' and 'video2' clips by applying
        that alpha clip as a mask in the second one to appear
        over the first one.
        """
        video1 = VideoParser.to_moviepy(video1)
        video2 = VideoParser.to_moviepy(video2)
        alpha_video = VideoParser.to_moviepy(alpha_video)
        alpha_processing_method = MoviepyAlphaTransitionProcessingMethod.to_enum(alpha_processing_method)

        # We need to adjust the clip to the transition duration
        if (alpha_video.duration != video1.duration):
            alpha_video = set_video_duration(alpha_video, video1.duration, ExtendVideoMode.SPEED_UP_OR_SLOW_DOWN)
        
        mask_clip = MoviepyAlphaTransitionHandler.alpha_clip_to_mask_clip(alpha_video, method = alpha_processing_method)
        video2 = video2.set_mask(mask_clip)

        return CompositeVideoClip([
            video1,
            video2
        ])

class TransitionGenerator:
    """
    Class to simplify and encapsulate the functionality
    related to transition between videos
    """
    @staticmethod
    def apply(videos, transitions: list[VideoTransition] = None):
        """
        Build a transition by using the provided 'transition_method' 
        (that must be a transition method within the Transition class)
        and put it between all the provided videos that are played
        completely before and after the transition.

        So, the sequence is the next.
        1. The 'videoX' is played completely.
        2. The transition is played completely.
        3. Go to step 1 with the next video until last one
        4. Last video is played completely
        """
        if not PythonValidator.is_list(videos):
            videos = [VideoParser.to_moviepy(video)]
        
        if len(videos) == 1:
            return videos[0]

        if not PythonValidator.is_list(transitions):
            if not PythonValidator.is_instance(transitions, VideoTransition):
                raise Exception('The provided "transitions" parameter is not a list of VideoTransition nor a single VideoTransition.')
            else:
                transitions = [transitions] * (len(videos) - 1)
        else:
            if len(transitions) != len(videos) - 1:
                raise Exception(f'The number of videos is {str(len(videos))} and the amount of transitions must be {str(len(videos) - 1)} and you provided {str(len(transitions))} transitions.')

        videos = [VideoParser.to_moviepy(video) for video in videos]

        video_transitions = []
        for i in range(1, len(videos)):
            video, video_transition, next_video = Transition.create_transition(videos[i - 1], videos[i], transitions[i - 1])

            videos[i - 1] = video
            videos[i] = next_video
            video_transitions.append(video_transition)
            
        clips_to_concat = []
        for video, video_transition in zip(videos[:-1], video_transitions):
            clips_to_concat.extend([video, video_transition])
        clips_to_concat.append(videos[-1])

        return concatenate_videoclips(clips_to_concat)