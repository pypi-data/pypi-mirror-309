from yta_general_utils.file.checker import FileValidator
from yta_multimedia.video.audio import set_audio_in_video
from moviepy.editor import VideoFileClip
from numba import njit

import pygame as pg
import cv2


@njit(fastmath=True)
def accelerate_conversion(image, width, height, ascii_coeff, step):
    array_of_values = []
    for x in range(0, width, step):
        for y in range(0, height, step):
            char_index = image[x, y] // ascii_coeff
            if char_index:
                array_of_values.append((char_index, (x, y)))
    return array_of_values

class AsciiFilteredVideo:
    def __init__(self, input_filename, output_filename, font_size = 12):
        pg.init()
        self.path = input_filename
        self.capture = cv2.VideoCapture(input_filename)
        self.image = self.get_image()
        self.RES = self.WIDTH, self.HEIGHT = self.image.shape[0], self.image.shape[1]
        self.surface = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()

        self.ASCII_CHARS = ' .",:;!~+-xmo*#W&8@'
        self.ASCII_COEFF = 255 // (len(self.ASCII_CHARS) - 1)

        self.font = pg.font.SysFont('Courier', font_size, bold = True)
        self.CHAR_STEP = int(font_size * 0.6)
        self.RENDERED_ASCII_CHARS = [self.font.render(char, False, 'white') for char in self.ASCII_CHARS]

        self.rec_fps = self.capture.get(cv2.CAP_PROP_FPS)
        self.record = True
        self.recorder = cv2.VideoWriter(output_filename, cv2.VideoWriter_fourcc(*'mp4v'), self.rec_fps, self.RES)

    def get_frame(self):
        frame = pg.surfarray.array3d(self.surface)
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
        array_of_values = accelerate_conversion(self.image, self.WIDTH, self.HEIGHT, self.ASCII_COEFF, self.CHAR_STEP)
        for char_index, pos in array_of_values:
            self.surface.blit(self.RENDERED_ASCII_CHARS[char_index], pos)

    def get_image(self):
        # self.cv2_image = cv2.imread(self.path)
        ret, self.cv2_image = self.capture.read()
        if not ret:
            exit()
        transposed_image = cv2.transpose(self.cv2_image)
        gray_image = cv2.cvtColor(transposed_image, cv2.COLOR_BGR2GRAY)
        return gray_image

    def draw_cv2_image(self):
        resized_cv2_image = cv2.resize(self.cv2_image, (640, 360), interpolation=cv2.INTER_AREA)
        cv2.imshow('img', resized_cv2_image)

    def draw(self):
        self.surface.fill('black')
        self.draw_converted_image()
        # self.draw_cv2_image()

    def save_image(self):
        pygame_image = pg.surfarray.array3d(self.surface)
        cv2_img = cv2.transpose(pygame_image)
        cv2.imwrite('ascii_image.jpg', cv2_img)

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

def to_ascii(video_filename: str, output_filename: str, kwargs):
    """
    Gets the provided 'input_filename' video, turns it into ascii
    video and stores the result in a new video as 'output_filename'.

    Optional parameter is 'font_size' (default value is 12).
    """
    if not video_filename:
        return None
    
    if not FileValidator.file_is_video_file(video_filename):
        return None
    
    if not output_filename:
        return None
    
    font_size = kwargs.get('font_size', 12)

    app = AsciiFilteredVideo(video_filename, output_filename, font_size)
    app.run()

    output_videoclip = VideoFileClip(video_filename)
    output_videoclip_with_sound = set_audio_in_video(output_filename, output_videoclip.audio)
    output_videoclip_with_sound.write_videofile(output_filename)

