from moviepy.editor import ColorClip


DEFAULT_BACKGROUND_VIDEO = ColorClip((1920, 1080), [0, 0, 0], duration = 1 / 60).set_fps(60)
"""
Default full opaque black background video that lasts
(1 / 60) seconds that represents our default moviepy
scenario of 1920x1080 dimensions and is used for the
basic position calculations.
"""