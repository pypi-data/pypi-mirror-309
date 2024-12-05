from yta_multimedia.video.audio import set_audio_in_video
from yta_general_utils.file.checker import FileValidator
from numba import njit
from moviepy.editor import VideoFileClip

import pygame as pg
import numpy as np
import pygame.gfxdraw
import cv2

# This awesome tool comes from here: https://www.youtube.com/watch?v=eLfRSAgXNZU
# Hey, maybe take a look ? (https://github.com/sedthh/pyxelate)

@njit(fastmath = True)
def accelerate_conversion(image, width, height, color_coeff, step):
    array_of_values = []
    for x in range(0, width, step):
        for y in range(0, height, step):
            r, g, b = image[x, y] // color_coeff
            if r + g + b:
                array_of_values.append(((r, g, b), (x, y)))
    return array_of_values


class PixelatedVideo:
    def __init__(self, input_filename, output_filename, pixel_size = 7, color_lvl = 8):
        pg.init()
        self.path = input_filename
        self.capture = cv2.VideoCapture(input_filename)
        self.PIXEL_SIZE = pixel_size
        self.COLOR_LVL = color_lvl
        self.image = self.get_image()
        self.RES = self.WIDTH, self.HEIGHT = self.image.shape[0], self.image.shape[1]
        self.surface = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.PALETTE, self.COLOR_COEFF = self.create_palette()

        self.rec_fps = self.capture.get(cv2.CAP_PROP_FPS)
        self.record = True
        self.recorder = cv2.VideoWriter(output_filename, cv2.VideoWriter_fourcc(*'mp4v'), self.rec_fps, self.RES)

    def get_frame(self):
        frame = pg.surfarray.array3d(self.surface)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return cv2.transpose(frame)

    def record_frame(self):
        if self.record:
            frame = self.get_frame()
            self.recorder.write(frame)
            #cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                self.record = not self.record
                cv2.destroyAllWindows()

    def draw_converted_image(self):
        self.image = self.get_image()
        # Here is where the magic happens
        array_of_values = accelerate_conversion(self.image, self.WIDTH, self.HEIGHT, self.COLOR_COEFF, self.PIXEL_SIZE)
        for color_key, (x, y) in array_of_values:
            color = self.PALETTE[color_key]
            pygame.gfxdraw.box(self.surface, (x, y, self.PIXEL_SIZE, self.PIXEL_SIZE), color)

    def create_palette(self):
        colors, color_coeff = np.linspace(0, 255, num=self.COLOR_LVL, dtype=int, retstep=True)
        color_palette = [np.array([r, g, b]) for r in colors for g in colors for b in colors]
        palette = {}
        color_coeff = int(color_coeff)
        for color in color_palette:
            color_key = tuple(color // color_coeff)
            palette[color_key] = color
        return palette, color_coeff

    def get_image(self):
        ret, self.cv2_image = self.capture.read()
        if not ret:
            exit()
        transposed_image = cv2.transpose(self.cv2_image)
        image = cv2.cvtColor(transposed_image, cv2.COLOR_BGR2RGB)
        return image

    def draw_cv2_image(self):
        resized_cv2_image = cv2.resize(self.cv2_image, (640, 360), interpolation=cv2.INTER_AREA)
        cv2.imshow('img', resized_cv2_image)

    def draw(self):
        self.surface.fill('black')
        self.draw_converted_image()
        #self.draw_cv2_image()

    def save_image(self):
        pygame_image = pg.surfarray.array3d(self.surface)
        cv2_img = cv2.transpose(pygame_image)
        cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_RGB2BGR)
        cv2.imwrite('output/pixel_art_image.jpg', cv2_img)

    def run(self):
        while True:
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    exit()
                elif i.type == pg.KEYDOWN:
                    if i.key == pg.K_s:
                        self.save_image()
                    if i.key == pg.K_r:
                        self.record = not self.record
            self.record_frame()
            self.draw()
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick()

def to_pixelated(video_filename: str, output_filename: str, kwargs = {'pixel_size': 7, 'color_level': 8}):
    """
    Gets the provided 'input_filename' video, pixelates it and stores the result
    in a new video as 'output_filename'.

    Optional parameters are 'pixel_size' (default value is 7) and 
    'color_level' (default value is 8).
    """
    if not video_filename:
        return None
    
    if not FileValidator.file_is_video_file(video_filename):
        return None
    
    if not output_filename:
        return None

    pixel_size = kwargs.get('pixel_size', 7)
    color_level = kwargs.get('color_level', 8)

    app = PixelatedVideo(video_filename, output_filename, pixel_size, color_level)
    app.run()

    output_videoclip = VideoFileClip(video_filename)
    output_videoclip_with_sound = set_audio_in_video(output_filename, output_videoclip.audio)
    output_videoclip_with_sound.write_videofile(output_filename)