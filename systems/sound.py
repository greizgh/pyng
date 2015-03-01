from lutes import System
import pyglet


class Sound(System):
    def __init__(self):
        super().__init__(20)
        self.bounce_wall = pyglet.resource.media(
            'data/bounce.wav',
            streaming=False
        )
        self.bounce_paddle = pyglet.resource.media(
            'data/paddle.wav',
            streaming=False
        )
        self.death = pyglet.resource.media(
            'data/death.wav',
            streaming=False
        )

    def init(self):
        self.manager.subscribe('collide_void_left', self.on_void)
        self.manager.subscribe('collide_void_right', self.on_void)
        self.manager.subscribe('collide_wall', self.on_wall)
        self.manager.subscribe('collide_paddle', self.on_paddle)

    def on_void(self, data):
        self.death.play()

    def on_paddle(self, data):
        self.bounce_paddle.play()

    def on_wall(self, data):
        self.bounce_wall.play()
