"""
    Thanks to https://omaraflak.medium.com/b%C3%A9zier-interpolation-8033e9a262c2
    for interpolation explanation and code.

    Thanks to https://github.com/vmichals/python-algos/blob/master/catmull_rom_spline.py
    for the catmull-rom-spline interpolation code.
"""
from yta_general_utils.programming.parameter_validator import NumberValidator, PythonValidator
from yta_multimedia.video.edition.effect.moviepy.position.objects.video_position import Coordinate
from yta_multimedia.video.edition.effect.moviepy.position.objects.video_position import VideoPosition
from yta_multimedia.video.position import Position
from yta_general_utils.math import Math
from typing import Callable
from math import comb

import random
import bezier
import numpy as np
import matplotlib.pyplot as plt


# TODO: Remove this when refactored
# class NormalizedCoordinate(Coordinate):
#     """
#     A coordinate to be used in the graphic rate
#     function building system, which is a normalized
#     2D environment with values between 0.0 and 1.0.
#     """
#     def __init__(self, x: float, y: float):
#         if not NumberValidator.is_number_between(x, 0.0, 1.0) or not NumberValidator.is_number_between(y, 0.0, 1.0):
#             raise Exception(f'The provided "x" and/or "y" parameters {str(x)},{str(y)} values are not between 0.0 and 1.0.')
        
#         super().__init__(x, y)

#     @staticmethod
#     def generate(amount: int = 1):
#         """
#         Generate 'amount' normalized coordinates with random
#         values that are returned as an array of instances.

#         The amount parameter is limited to the interval 
#         [1, 100].
#         """
#         if not NumberValidator.is_number_between(amount, 1, 100):
#             raise Exception(f'The provided "amount" parameter "{str(amount)}" is not a number between 1 and 100.')
        
#         return [NormalizedCoordinate(random.uniform(0, 1), random.uniform(0, 1)) for _ in range(amount)]
    
#     @staticmethod
#     def to_numpy(coordinates: list):
#         """
#         Convert a list of BizierCoordinate 'coordinates' to
#         numpy array to be able to work with them.

#         This method does the next operation:
#         np.array([[coord.x, coord.y] for coord in coordinates])
#         """
#         if not PythonValidator.is_list(coordinates):
#             if not PythonValidator.is_instance(coordinates, NormalizedCoordinate):
#                 raise Exception('The provided "coordinates" parameter is not a list of NormalizedCoordinates nor a single NormalizedCoordinate instance.')
#             else:
#                 coordinates = [coordinates]
#         elif any(not PythonValidator.is_instance(coordinate, NormalizedCoordinate) for coordinate in coordinates):
#             raise Exception('At least one of the provided "coordinates" is not a NormalizedCoordinate instance.')

#         return np.array([coordinate.to_array() for coordinate in coordinates])


# Here below are some functions to obtain the graphic
# between points
class InterpolationFormula:
    """
    Class to encapsulate interpolation formulas.
    """
    @staticmethod
    def catmull_rom_spline(spline_x: float, p0, p1, p2, p3):
        """
        Function to evaluate one spline of the Catmull-Rom
        between two points by using 4 control points.

        It returns the x,y point in the spline.

        Computes interpolated y-coord for given x-coord using
        Catmull-Rom. The 'spline_x' is the current position in
        the graphic interpolation between the points p0 and p1
        represented by a value between 0 and 1.

        Computes an interpolated y-coordinate for the given
        x-coordinate between the support points v1 and v2. The
        neighboring support points v0 and v3 are used by
        Catmull-Rom to ensure a smooth transition between the
        spline segments.
        """
        c1 = 1. * p1
        c2 = -.5 * p0 + .5 * p2
        c3 = 1. * p0 + -2.5 * p1 + 2. * p2 -.5 * p3
        c4 = -.5 * p0 + 1.5 * p1 + -1.5 * p2 + .5 * p3

        return (((c4 * spline_x + c3) * spline_x + c2) * spline_x + c1)
    
    @staticmethod
    def linear(spline_x: float, p0, p1):
        """
        Function to evaluate one spline of a linear function
        between two points.

        It returns the x,y point in the spline.

        Computes interpolated y-coord for given x-coord using
        linear function.
        """
        x = p0[0] + (p1[0] - p0[0]) * spline_x
        y = p0[1] + (p1[1] - p0[1]) * spline_x

        return (x, y)

class GraphicRateFunction:
    """
    Class to simplify the way we work with rate functions
    being able to personalize a graphic that will allow us
    using it as a rate function to create our own effects.

    We receive a list of points that are coordinates of the
    graph we want to create as a rate function, and the 
    code will analyze it and obtain the function that allows
    us to determine the value of any 't' value between 0.0
    and 1.0.
    
    The 't' value provided is representing the distance in the
    graphic curve that has been generated with the points
    provided and the interpolation method applied. This curve
    is representing some effect, animation or transition
    duration, from 0 to 1. So, if the provided 't' is 0.20,
    that is representing the moment in which the 20% of the
    animation has been played, and will return the 'y' value
    that must be used in the animation for that specific 
    moment.

    We have a graphic representation of a function in which we
    use the 'x' and 'y' axis to represent it. There is another
    value that we call 't' and it is one point within the 
    graphic that has been generated with the provided points
    and the 'interpolation_formula'. This 't' is representing
    an instant during the execution of an animation or
    transition.
    """
    points: np.ndarray
    """
    The list of points [x, y] the graph will go through.
    """
    interpolation_formula: Callable
    """
    The method to calculate the interpolation between each
    pair of points.

    TODO: By now it is the same for the whole graph but it
    could change in a near future and be specific for each
    pair of points. We should create an InterpolationStep
    or similar to include 2 coordinates and 1 interpolation
    formula, and receive a list of instances of that class
    as a parameter to be able to customize each type of
    interpolation.
    """

    def __init__(self, points: list[Coordinate, Position, VideoPosition], interpolation_formula: Callable):
        if not PythonValidator.is_list(points) or len(points) < 4 or any(not PythonValidator.is_instance(point, [Coordinate, Position, VideoPosition]) for point in points):
            raise Exception(f'The "points" parameter must be a list of Coordinate, Position or VideoPosition with a minimum of 4 elements.')
    
        if not PythonValidator.is_class_staticmethod(InterpolationFormula, interpolation_formula):
            raise Exception('The provided "interpolation_formula" is not a valid InterpolationFormula class method.')

        # TODO: Maybe if less than 4 elements: add 2 in between those 2
        # TODO: Should I allow this below (?) If I'm trying to obtain a
        # path I think yes... I will be using a 't' that is actually the
        # distance in the graph once it's been built, so I don't care if
        # I am going back or not, because it is like if just have two 
        # points in that moment and we want to know the value in one 
        # specific point of the graph between those 2 points, so I think
        # I should accept going towards or backwards
        # if not all(points[i].x < points[i + 1].x for i in range(len(points) - 1)):
        #     raise Exception('Points must be consecutive, so the "x" value of each point must be greater than the previous one. Please, check the provided "points" parameter.')

        # Turn all points to coordinates, normalize them and
        # obtain the normalized x,y in the format we need
        coords = []
        for point in points:
            coord = point
            if PythonValidator.is_instance(point, Position):
                coord = point.as_video_position().coordinate
            elif PythonValidator.is_instance(point, VideoPosition):
                coord = point.coordinate

            coord = coord.normalize()
            coords.append(coord)

        self.points = np.array([[coord[0], coord[1]] for coord in Coordinate.to_numpy(coords)])
        self.interpolation_formula = interpolation_formula

    def get_coord(self, t: float):
        """
        Evaluate the function for the provided 'x' value and
        return the graphic coordinate corresponding to that
        't' value, that must be a normalized value (between
        0 and 1, both inclusive) that represents the distance
        in the generated graphic.

        A graphic with 5 coordinates will generate 4 splines
        of the same length. The start of each of those splines
        will be [t = 0, t = 0.25, t = 0.5, t = 0.75]. So, if
        you provide t = 0.20, the returned coordinate will be
        contained in the first spline because it is below 0.25.
        """
        if not NumberValidator.is_number_between(t, 0.0, 1.0):
            raise Exception('The provided "t" parameter "{str(t)}" must be  between 0 and 1, both inclusive.')

        num_of_splines = len(self.points) - 1
        spline_size = 1 / num_of_splines

        if t == 1.0:
            spline_index = num_of_splines - 1
        else:
            # Check which spline we need to use
            spline_index = int(t // spline_size)

        # If we receive 0.28 => 0.28 - 0.25 = 0.03 / spline_size
        # A distance of 0.03 in the global graph is lower than the
        # real distance in any splice
        # 0.28 = 0.28 % (1 * 0.25) / 0.25 = 0.03 / 0.25 = 0.12
        previous_spline_size = spline_index * spline_size

        if previous_spline_size:
            t = t % (spline_index * spline_size) / spline_size
        else:
            t = t / spline_size

        if PythonValidator.is_class_staticmethod(InterpolationFormula, self.interpolation_formula, InterpolationFormula.catmull_rom_spline.__name__):
            if spline_index == 0: # First spline
                # We need to estimate the first point
                p0 = self.points[0] - (self.points[1] - self.points[0])
                p1 = self.points[0]
                p2 = self.points[1]
                p3 = self.points[2]
            elif spline_index == (num_of_splines - 1): # Last spline
                p0 = self.points[spline_index - 1]
                p1 = self.points[spline_index]
                p2 = self.points[spline_index + 1]
                # We need to estimate the last point
                p3 = self.points[spline_index + 1] + (self.points[spline_index + 1] - self.points[spline_index])
            else:
                p0 = self.points[spline_index - 1]
                p1 = self.points[spline_index]
                p2 = self.points[spline_index + 1]
                p3 = self.points[spline_index + 2]

            coord = self.interpolation_formula(t, p0, p1, p2, p3)
        elif PythonValidator.is_class_staticmethod(InterpolationFormula, self.interpolation_formula, InterpolationFormula.linear.__name__):
            p0 = self.points[spline_index]
            p1 = self.points[spline_index + 1]

            coord = self.interpolation_formula(t, p0, p1)
        
        # We want the 'y' value as we are representing
        # something in a graphic, but we get the whole
        # coord at this point
        return coord
    
    def get_y(self, t: float):
        """
        Evaluate the function for the provided 't' value and
        return the graphic coordinate 'y' value corresponding
        to that 't' value that represents the distance in the
        generated graphic.

        A graphic with 5 coordinates will generate 4 splines
        of the same length. The start of each of those splines
        will be [t = 0, t = 0.25, t = 0.5, t = 0.75]. So, if
        you provide t = 0.20, the returned coordinate will be
        contained in the first spline because it is below 0.25.
        """
        return self.get_coord(t)[1]

    def plot(self, is_path_movement: bool = False):
        """
        This method is just for testing and shows the graphic
        using the matplotlib library.

        If you are plotting a path movement along the screen,
        set the 'is_path_movement' as True to make the plot
        show the real movement the video will do through the
        scene. If you are plotting a graph used for any other
        type of effect, keep the value as False.
        """
        if is_path_movement:
            # I denormalize values to be able to watch them properly
            graph = []
            for t in np.linspace(0, 1, len(self.points) * 100):
                coord = self.get_coord(t)
                # TODO: These 'min' and 'max' values must be read from a consts file
                graph.append((Math.denormalize(coord[0], -10000, 10000), Math.denormalize(coord[1], -10000, 10000)))
            graph = np.array(graph)
        
            # TODO: These 'min' and 'max' values must be read from a consts file
            self.points = np.array([(Math.denormalize(point[0], -10000, 10000), Math.denormalize(point[1], -10000, 10000)) for point in self.points])

        plt.plot(graph[:, 0], graph[:, 1], label = 'Graphic representation', color = 'blue')
        plt.scatter(self.points[:, 0], self.points[:, 1], color = 'red', label = 'Control points')
        plt.legend()
        plt.title('Graphic representation')
        plt.xlabel('x')
        plt.ylabel('y')
        if is_path_movement:
            # I invert the axis to see the graph as the video movement
            plt.gca().invert_yaxis()
        plt.grid(True)
        plt.show()

    # TODO: If we want to apply one GraphicRateFunction to some
    # of our moviepy animations, we will be working with a 't'
    # value representing the time of the video, that can easily
    # be greater than 1, so we need to normalize it with the
    # video duration and use that normalized value to provide it
    # to this 'get_y()' or 'get_coord()' method.



from yta_general_utils.math.rate_functions import RateFunction





# TODO: I keep this code below because it was almost working
# but need refactor to be adapted to the way I want to use
# this interpolation functionality. I need to join pairs of
# points to build a Graph concept to be able to use it as the
# rate function definer
class BezierCurve:
    """
    Class to encapsulate and simplify the funcitonality
    related to bezier curves.
    """
    curve: bezier.Curve
    """
    The instance of the Curve from the bezier library.
    """

    def __init__(self, control_nodes: list[NormalizedCoordinate]):
        if not PythonValidator.is_list(control_nodes):
            if not PythonValidator.is_instance(control_nodes, NormalizedCoordinate):
                raise Exception('The provided "control_nodes" parameter is not a list of NormalizedCoordinate instances nor a single NormalizedCoordinate instance.')
            else:
                control_nodes = [control_nodes]

        if any(not PythonValidator.is_instance(control_node, NormalizedCoordinate) for control_node in control_nodes):
            raise Exception(f'At least one of the provided "control_nodes" parameter is not a NormalizedCoordinate instance.')
        
        nodes_np_array = [[control_node.x for control_node in control_nodes], [control_node.y for control_node in control_nodes]]
        degree = len(control_nodes) - 1

        self.curve = bezier.Curve(nodes_np_array, degree = degree)
        # TODO: Anything else (?)

    def get_curve_point_value(self, t: float):
        """
        Obtain the curve value for the provided 't' that must
        be a value between 0.0 and 1.0.
        """
        if not NumberValidator.is_number_between(t, 0.0, 1.0):
            raise Exception(f'The provided "t" parameter value "{str(t)}" is not a valid value. Must be between 0.0 and 1.0.')

        return self.curve.evaluate(t)

    def plot(self, do_show_control_nodes: bool = True):
        """
        Plot and show the bezier curve using matplotlib.
        """
        # Set 100 points of the curve to draw it
        curve_points = self.curve.evaluate_multi(np.linspace(0, 1, 100))
        nodes = self.curve.nodes

        plt.plot(curve_points[0], curve_points[1], label = "Bezier curve", color = 'b')

        if do_show_control_nodes:
            plt.scatter(nodes[0], nodes[1], color = 'r', label = "Control nodes")
            # Draw control nodes lines in-between
            for i in range(len(nodes[0]) - 1):
                plt.plot([nodes[0][i], nodes[0][i + 1]], [nodes[1][i], nodes[1][i + 1]], 'r--')

        plt.legend()
        plt.title(f'Bezier curve (degree = {str(len(nodes[0]) - 1)})')
        plt.grid(True)
        plt.axis('equal')
        plt.show()

    @staticmethod
    def generate_random():
        # TODO: This is the interpolation process
        points = NormalizedCoordinate.generate(8)
        points.insert(0, NormalizedCoordinate(0, 0))
        points.append(NormalizedCoordinate(1, 1))
        path = evaluate_bezier(points, 50)

        #points = np.array([point.to_array() for point in points])
        points = NormalizedCoordinate.to_numpy(points)
        # extract x & y coordinates of points
        x, y = points[:,0], points[:,1]
        px, py = path[:,0], path[:,1]

        # plot
        plt.figure(figsize=(11, 8))
        plt.plot(px, py, 'b-')
        plt.plot(x, y, 'ro')
        plt.show()

        return
        # TODO: I'm working with these below to be able to build
        # the BezierCurve instance by providing the path cooridnates
        # from which we interpolate and calculate the curve

        # A and B are the 2 control nodes for each 2 consecutive
        # points (it is a cubic interpolation)
        first_control_nodes, second_control_nodes = get_bezier_coeficient(points)

        curve_path = [
            get_cubic_bezier_formula(points[i], first_control_nodes[i], second_control_nodes[i], points[i + 1])
            for i in range(len(points) - 1)
        ]

        # TODO: This is to print the whole curve
        n = 100
        real_curve_path_with_100_points = np.array([fun(t) for fun in curve_path for t in np.linspace(0, 1, n)])

    @staticmethod
    def get_bezier_curve(points: list[NormalizedCoordinate]):
        points = NormalizedCoordinate.to_numpy(points)
        first_control_nodes, second_control_nodes = get_bezier_coeficient(points)

        return BezierCurve()
    
    @staticmethod
    def get_bezier_curve_from_points(points: list[NormalizedCoordinate]):
        # I obtain the control nodes (2, as cubic bezier function)
        # for each point
        first_control_nodes, second_control_nodes = get_bezier_coeficient(points)
        bezier_function = [
            get_cubic_bezier_formula(points[i], first_control_nodes[i], second_control_nodes[i], points[i + 1])
            for i in range(len(points) - 1)
        ]

        # I have many bezier curves concatenated

        # This generates 100 points for each bezier curve
        np.array([fun(t) for fun in bezier_function for t in np.linspace(0, 1, 100)])

def get_bezier_coeficient(points):
    """
    Find the A and B points. These are the control nodes for
    each bezier cubic curve point, as it is using two control
    nodes (A and B) that are the ones we are looking for.

    TODO: Is this ok (?)

    TODO: How to apply this to a non-cubic bezier curve (?)
    """
    # since the formulas work given that we have n+1 points
    # then n must be this:
    n = len(points) - 1

    # Build the coefficents matrix
    C = 4 * np.identity(n)
    np.fill_diagonal(C[1:], 1)
    np.fill_diagonal(C[:, 1:], 1)
    C[0, 0] = 2
    C[n - 1, n - 1] = 7
    C[n - 1, n - 2] = 2

    # Build the points vector
    P = [2 * (2 * points[i] + points[i + 1]) for i in range(n)]
    P[0] = points[0] + 2 * points[1]
    P[n - 1] = 8 * points[n - 1] + points[n]

    # Solve the system and find control nodes A and B
    A = np.linalg.solve(C, P)
    B = [0] * n
    for i in range(n - 1):
        B[i] = 2 * points[i + 1] - A[i + 1]
    B[n - 1] = (A[n - 1] + points[n]) / 2

    return A, B

# TODO: This below has not been checked
def get_lineal_bezier_formula(node1, node2):
    return lambda t: (1 - t) * np.array(node1) + t * np.array(node2)

# TODO: This below has not been checked
def get_cuadratic_bezier_formula(node1, node2, node3):
    return lambda t: (1 - t)**2 * np.array(node1) + 2 * (1 - t) * t * np.array(node2) + t**2 * np.array(node3)

# TODO: This is the only one that is working for sure
def get_cubic_bezier_formula(node1, node2, node3, node4):
    """
    Return the general Bezier cubic formula given 4 control
    nodes.
    """
    return lambda t: np.power(1 - t, 3) * node1 + 3 * np.power(1 - t, 2) * t * node2 + 3 * (1 - t) * np.power(t, 2) * node3 + np.power(t, 3) * node4

# TODO: This below has not been checked
def get_n_bezier_formula(nodes: list):
    def x(t):
        N = len(nodes)
        B_t = np.zeros_like(nodes[0])  # Inicializar el punto en 0 (misma dimensión que los puntos de control)
        
        for i in range(N):
            # Coeficiente binomial
            coef_binom = comb(N - 1, i)
            # Fórmula de Bézier general
            B_t += coef_binom * (1 - t)**(N - 1 - i) * t**i * np.array(nodes[i])

    return lambda t: x(t)

# return one cubic curve for each consecutive points
def get_bezier_cubic(points):
    """
    Return a cubir curve for each consecutive points.
    """
    A, B = get_bezier_coeficient(points)

    return [
        get_cubic_bezier_formula(points[i], A[i], B[i], points[i + 1])
        for i in range(len(points) - 1)
    ]

def evaluate_bezier(points: list[NormalizedCoordinate], n):
    """
    Evaluate each cubic curve on the range [0, 1]
    sliced in n points.

    TODO: Maybe rename to interpolate (?)
    """
    #points = [point.to_array() for point in points]
    # Transform BezierCoordinates to array
    points = NormalizedCoordinate.to_numpy(points)
    #points = np.array([point.to_array() for point in points])

    return np.array([fun(t) for fun in get_bezier_cubic(points) for t in np.linspace(0, 1, n)])



# TODO: This code below was working
"""
    points = BezierControlNode.generate(8)
    points.insert(0, BezierControlNode(0, 0))
    points.append(BezierControlNode(1, 1))
    path = evaluate_bezier(points, 50)


    points = np.array([point.to_array() for point in points])
    # extract x & y coordinates of points
    x, y = points[:,0], points[:,1]
    px, py = path[:,0], path[:,1]

    # plot
    plt.figure(figsize=(11, 8))
    plt.plot(px, py, 'b-')
    plt.plot(x, y, 'ro')
    plt.show()
"""
