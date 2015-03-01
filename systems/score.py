from lutes import System
import constants
import random
import pyglet
from archetype import BallArchetype


class Score(System):
    def __init__(self, ball, window):
        super().__init__(10)
        self.ball = ball
        self.window = window
        self.left = 0
        self.right = 0

    def init(self):
        pyglet.font.add_file('data/VCR_OSD_MONO.ttf')
        self.manager.subscribe('collide_void_left', self.on_void_left)
        self.manager.subscribe('collide_void_right', self.on_void_right)

    def on_void_left(self, data):
        self.right += 1
        self.respawn(data['space'], data['arbiter'])

    def on_void_right(self, data):
        self.left += 1
        self.respawn(data['space'], data['arbiter'])

    def update(self, delta):
        score_left = pyglet.text.Label(str(self.left),
                                       font_name='VCR OSD Mono',
                                       font_size=36,
                                       x=20, y=self.window.get_size()[1]-20,
                                       anchor_x='left', anchor_y='top')
        score_right = pyglet.text.Label(str(self.right),
                                        font_name='VCR OSD Mono',
                                        font_size=36,
                                        x=self.window.get_size()[0]-20,
                                        y=self.window.get_size()[1]-20,
                                        anchor_x='right', anchor_y='top')
        score_left.draw()
        score_right.draw()

    def respawn(self, space, arbiter):
        random.seed()
        ball_shape, _ = arbiter.shapes
        space.remove(ball_shape)
        space.remove(ball_shape.body)
        self.manager.remove_entity(self.ball)
        self.ball = BallArchetype(self.manager, space).create_entity(
            constants.FIELD_WIDTH/2,
            constants.FIELD_HEIGHT/2,
            (random.randrange(-300, 300), random.randrange(-300, 300))
        )
