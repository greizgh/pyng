from lutes import System
from components import Control
import pymunk as pm
import pyglet.window.key as keys
import constants


class Movement(System):
    def __init__(self, window):
        super().__init__(5)
        self.window = window
        self.key_state = keys.KeyStateHandler()
        self.window.push_handlers(self.key_state)
        self.handled_components = [pm.Body, Control]

    def update(self, delta):
        for entity in self.entities:
            control = self.manager.get_component(entity, Control)
            body = self.manager.get_component(entity, pm.Body)
            if self.key_state[control.up]:
                body.apply_impulse((0, constants.PADDLE_CONTROL_FORCE))
            elif self.key_state[control.down]:
                body.apply_impulse((0, -constants.PADDLE_CONTROL_FORCE))
            else:
                body.apply_impulse((0, -body.velocity[1]*0.8))
