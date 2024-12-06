from yta_multimedia.video.edition.effect.moviepy.position.interpolation import NormalizedCoordinate
from yta_general_utils.math import Math


class CoordinateCorner:
    """
    Class that encapsulates a coordinate (x, y) representing the
    upper left corner of a video in a movement effect 
    envinronment. This class is used as type to represent the 
    position in which we want to place a video, considering this 
    position as the upper left corner of the video.
    """
    position = (0, 0)
    """
    The (x, y) tuple containing the position coordinate.
    """

    def __init__(self, x: int, y: int):
        if not x and x != 0:
            raise Exception('No "x" provided.')
        
        if not y and y != 0:
            raise Exception('No "y" provided.')
        
        # TODO: Check 'x' and 'y' are numbers and cast to int
        
        self.position = (x, y)

    def get_x(self):
        return self.position[0]
    
    def get_y(self):
        return self.position[1]

    def to_tuple(self):
        return self.position
    
    def to_array(self):
        return [self.position[0], self.position[1]]
    
    def to_normalized_coordinate(self, min_value = -10000, max_value = 10000) -> NormalizedCoordinate:
        """
        Normalizes the coordinate to turn it into a value between
        0 and 1 to be able to use it in our GraphRateFunction 
        system. As we are working in a coordinates system that
        involves 1920x1080 scenarios and our videos can be 
        completely outside of the scene, I use this default values.
        """
        return NormalizedCoordinate(Math.normalize(self.position[0], min_value, max_value), Math.normalize(self.position[1], min_value, max_value))
    
    def recalculate_for_video(self, background_video):
        """
        This method will return the coords (x, y) in which we need to place the
        a to have its upper left corner in the desired ('x', 'y') position over 
        the provided 'background_video' by making some calculations as below.

        Imagine a scene of a 1920x1080 black background and that the 'x' and 'y'
        you give as parameters are the upper left corner of the video. We will
        calculate to place that video there in the real situation, 
        over the 'background_video' that could be not 1920x1080.

        TODO: Maybe we could return an instance of a CoordinateCorner class, as
        it is what it is.
        """
        # TODO: Implement checkings

        # Considering a 1920x1080 scene, recalculate actual coords
        x = (int) (background_video.w * self.position[0] / 1920)
        y = (int) (background_video.h * self.position[1] / 1080)

        return (x, y)