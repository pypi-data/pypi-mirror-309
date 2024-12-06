from yta_multimedia.video.edition.effect.moviepy.position.interpolation import NormalizedCoordinate
from yta_general_utils.math import Math


class CoordinateCenter:
    """
    Class that encapsulates a coordinate (x, y) representing the
    center of a video in a movement effect envinronment. This 
    class is used as type to represent the position in which we
    want to place a video, considering this position as the
    center of the video.
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
    
    def as_tuple(self):
        return self.position

    @staticmethod
    def to_tuple(coordinate):
        # TODO: Check if coordinate is 'CoordinateCenter' (?)
        return coordinate.position
    
    def as_array(self):
        return [self.position[0], self.position[1]]

    @staticmethod
    def to_array(coordinate):
        # TODO: Check if coordinate is 'CoordinateCenter' (?)
        return [coordinate.position[0], coordinate.position[1]]
        
    def as_normalized_coordinate(self, min_value = -10000, max_value = 10000) -> NormalizedCoordinate:
        """
        Normalizes the coordinate to turn it into a value between
        0 and 1 to be able to use it in our GraphRateFunction 
        system. As we are working in a coordinates system that
        involves 1920x1080 scenarios and our videos can be 
        completely outside of the scene, I use this default values.
        """
        return CoordinateCenter.to_normalized_coordinate(self, min_value, max_value)
    
    @staticmethod
    def to_normalized_coordinate(coordinate, min_value = -10000, max_value = 10000) -> NormalizedCoordinate:
        """
        Normalizes the coordinate to turn it into a value between
        0 and 1 to be able to use it in our GraphRateFunction 
        system. As we are working in a coordinates system that
        involves 1920x1080 scenarios and our videos can be 
        completely outside of the scene, I use this default values.
        """
        # TODO: Check if coordinate is 'CoordinateCenter' (?)
        # TODO: Do this below
        # As the NormalizedCoordinate is considering the corner,
        # lets convert it first to that type and then normalize
        # it
        return NormalizedCoordinate(Math.normalize(coordinate.position[0], min_value, max_value), Math.normalize(coordinate.position[1], min_value, max_value))
    
    # TODO: Create a 'to_coordinate_corner' by receiving a 'video'
    # and a 'video_background', but it will generate a loop if I
    # do the same in CoordinateCorner to this one
    
    def recalculate_for_video(self, video, background_video):
        """
        This method will return the coords (x, y) in which we need to place the
        'video' to have its center in the desired ('x', 'y') position over the 
        also provided 'background_video' by making some calculations as below.

        Imagine a scene of a 1920x1080 black background and that the 'x' and 'y'
        you give as parameters are the center of the 'video'. We will calculate 
        to place the provided 'video' there in the real situation, over the 
        'background_video' that could be not 1920x1080.
        """
        # TODO: Implement checkings

        # Considering a 1920x1080 scene, recalculate actual coords
        x = (int) (background_video.w * self.position[0] / 1920)
        y = (int) (background_video.h * self.position[1] / 1080)

        # Coordinates were from center, so adapt to upper left corner
        x -= (video.w / 2)
        y -= (video.h / 2)

        x = int(x)
        y = int(y)

        return (x, y)