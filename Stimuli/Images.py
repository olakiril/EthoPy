from core.Stimulus import *
from time import sleep
import os, imageio, cv2
import numpy as np
from utils.Presenter import *


@stimulus.schema
class Images(Stimulus, dj.Manual):
    definition = """
    # images conditions
    -> StimCondition
    ---
    -> Image
    pre_blank_period     : int                        # (ms) off duration
    presentation_time    : int                        # (ms) image duration

    """

    default_key = dict(pre_blank_period=200, presentation_time=1000)
    required_fields = ['pre_blank_period', 'presentation_time']
    cond_tables = ['Images']

    def __init__(self):
        super().__init__()
        self.fill_colors.set({'background': (128, 128, 128)})

    def setup(self):
        # setup parameters
        self.path = os.path.dirname(os.path.abspath(__file__)) + '/images/'
        self.size = (self.monitor['resolution_x'], self.monitor['resolution_y'])     # window size

        # setup screen
        self.Presenter = Presenter((self.monitor['resolution_x'], self.monitor['resolution_y']))
        self.timer = Timer()

    def prepare(self, curr_cond, stim_period=''):
        self.frame_idx = 0
        self.curr_cond = curr_cond
        self.clock = pygame.time.Clock()
        curr_img = self._get_image_info(self.curr_cond, 'Image', 'image')
        image_height, image_width = self._get_image_info(self.curr_cond, 'ImageClass.Info', 'image_height',
                                                         'image_width')
        self.imsize = (image_width, image_height)
        curr_img = curr_img[0]
        self.upscale = self.size[0] / self.imsize[0]
        self.y_pos = int((self.size[1] - self.imsize[1]*self.upscale)/2)
        if self.upscale != 1:
            curr_img = cv2.resize(curr_img, dsize=(self.size), interpolation=cv2.INTER_CUBIC)
        img_rgb = curr_img[..., None].repeat(3, -1).astype(np.int32)
        self.curr_img = self.Presenter.make_surface(img_rgb.swapaxes(0, 1))

        self.isrunning = True
        self.timer.start()

    def present(self):
        if self.curr_cond['pre_blank_period'] > 0 and self.timer.elapsed_time() < self.curr_cond['pre_blank_period']:
            #blank the screen
            self.fill()
            self.clock.tick(self.curr_cond['pre_blank_period'])
        elif self.timer.elapsed_time() < (self.curr_cond['pre_blank_period'] + self.curr_cond['presentation_time']):
            #show image
            if self.frame_idx == 0:
                self.Presenter.render(self.curr_img)
            self.frame_idx += 1
        else:
            self.isrunning = False

    def fill(self, color=False):
        if not color:
            color = self.fill_colors.background
        if self.fill_colors.background: self.Presenter.fill(color)

    def exit(self):
        self.Presenter.quit()

    def _get_image_info(self, key, table, *fields):
        return self.exp.logger.get(schema='stimulus', table=table, key=key, fields=fields)



