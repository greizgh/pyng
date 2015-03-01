from lutes import System
import constants
import pyglet
import pymunk as pm


class BaseRenderer(System):
    def __init__(self, window):
        super().__init__(10)
        self.window = window

    def convert_pos_to_window(self, vec):
        (win_x, win_y) = self.window.get_size()
        x_coef = win_x/constants.FIELD_WIDTH
        y_coef = win_y/constants.FIELD_HEIGHT
        return (vec[0]*x_coef, vec[1]*y_coef)


class RectangleRenderer(BaseRenderer):
    def __init__(self, window):
        super().__init__(window)
        self.handled_components = [pm.Poly]

    def update(self, delta):
        for entity in self.entities:
            rectangle = self.manager.get_component(entity, pm.Poly)
            points = []
            for vec in rectangle.get_vertices():
                (x, y) = self.convert_pos_to_window((vec.x, vec.y))
                points.append(x)
                points.append(y)
            pyglet.graphics.draw(
                4,
                pyglet.gl.GL_QUADS,
                ('v2f', points)
            )


class CircleRenderer(BaseRenderer):
    def __init__(self, window):
        super().__init__(window)
        self.handled_components = [pm.Body, pm.Circle]

    def update(self, delta):
        for entity in self.entities:
            position = self.manager.get_component(entity, pm.Body).position
            circle = self.manager.get_component(entity, pm.Circle)
            # 1.41 is an approximation of sqrt(2)
            (a_x, a_y) = self.convert_pos_to_window(
                (position.x - circle.radius*1.41/2,
                 position.y - circle.radius*1.41/2)
            )
            (b_x, b_y) = self.convert_pos_to_window(
                (position.x - circle.radius*1.41/2,
                 position.y + circle.radius*1.41/2)
            )
            (c_x, c_y) = self.convert_pos_to_window(
                (position.x + circle.radius*1.41/2,
                 position.y + circle.radius*1.41/2)
            )
            (d_x, d_y) = self.convert_pos_to_window(
                (position.x + circle.radius*1.41/2,
                 position.y - circle.radius*1.41/2)
            )
            pyglet.graphics.draw(
                4,
                pyglet.gl.GL_QUADS,
                ('v2f', [a_x, a_y, b_x, b_y, c_x, c_y, d_x, d_y])
            )
