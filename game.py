from lutes import Manager
from archetype import PaddleArchetype, BallArchetype, FieldArchetype
from components import Control
import constants
import random
from systems.renderer import RectangleRenderer, CircleRenderer
from systems.movement import Movement
from systems.physics import Physics
from systems.sound import Sound
from systems.score import Score
import pyglet
import pyglet.window.key as keys
import pymunk as pm


class Game:
    def __init__(self):
        self.manager = Manager()
        self.window = pyglet.window.Window(1900, 1280, 'Pyng', resizable=True)
        self.space = pm.Space()
        paddle_left = PaddleArchetype(self.manager, self.space).create_entity(
            constants.PADDLE_WIDTH,
            constants.PADDLE_HEIGHT,
            (constants.PADDLE_MARGIN, constants.FIELD_HEIGHT/2)
        )
        self.manager.add_component(paddle_left, Control(keys.UP, keys.DOWN))
        paddle_right = PaddleArchetype(self.manager, self.space).create_entity(
            constants.PADDLE_WIDTH,
            constants.PADDLE_HEIGHT,
            (constants.FIELD_WIDTH - constants.PADDLE_MARGIN,
             constants.FIELD_HEIGHT/2)
        )
        self.manager.add_component(paddle_right, Control(keys.Z, keys.S))
        self.ball = BallArchetype(self.manager, self.space).create_entity(
            constants.FIELD_WIDTH/2,
            constants.FIELD_HEIGHT/2,
            (random.randrange(-300, 300), random.randrange(-300, 300))
        )
        FieldArchetype(
            self.manager, self.space
        ).create_entity(
            constants.FIELD_WIDTH, constants.FIELD_HEIGHT
        )

        self.init_joints(paddle_left, paddle_right)

        self.manager.add_system(Movement(self.window))
        self.manager.add_system(Physics(self.space))
        self.manager.add_system(RectangleRenderer(self.window))
        self.manager.add_system(CircleRenderer(self.window))
        self.manager.add_system(Sound())
        self.manager.add_system(Score(self.ball, self.window))

        self.manager.init()

    def run(self):
        pyglet.clock.schedule_interval(self.update, 1/60)
        pyglet.app.run()

    def update(self, dt):
        self.window.clear()
        self.manager.update(dt)

    def init_joints(self, paddle_left, paddle_right):
        left_anchor = pm.Body()
        left_anchor.position = (10, 0)
        left_slide1 = pm.constraint.GrooveJoint(
            left_anchor,
            self.manager.get_component(paddle_left, pm.Body),
            (0, 0),
            (0, constants.FIELD_HEIGHT),
            (0, constants.PADDLE_HEIGHT/2)
        )
        left_slide2 = pm.constraint.GrooveJoint(
            left_anchor,
            self.manager.get_component(paddle_left, pm.Body),
            (0, 0),
            (0, constants.FIELD_HEIGHT),
            (0, -constants.PADDLE_HEIGHT/2)
        )
        right_anchor = pm.Body()
        right_anchor.position = (790, 0)
        right_slide1 = pm.constraint.GrooveJoint(
            right_anchor,
            self.manager.get_component(paddle_right, pm.Body),
            (0, 0),
            (0, constants.FIELD_HEIGHT),
            (0, constants.PADDLE_HEIGHT/2)
        )
        right_slide2 = pm.constraint.GrooveJoint(
            right_anchor,
            self.manager.get_component(paddle_right, pm.Body),
            (0, 0),
            (0, constants.FIELD_HEIGHT),
            (0, -constants.PADDLE_HEIGHT/2)
        )

        self.space.add(left_slide1, left_slide2, right_slide1, right_slide2)
