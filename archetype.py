"""Define archetypes used in Pyng"""
import pymunk as pm
import constants


class BaseArchetype:
    """
    An archetype is a factory to create multiple components associated
    with an entity
    """
    def __init__(self, manager, space):
        self.manager = manager
        self.space = space


class PaddleArchetype(BaseArchetype):
    """
    A paddle is controlled by a player and is used to bounce the ball
    toward the opponent.
    """
    def create_entity(self, x, y, pos):
        entity = self.manager.create_entity()
        inertia = pm.moment_for_box(constants.PADDLE_MASS, x, y)
        body = pm.Body(constants.PADDLE_MASS, inertia)
        body.position.x = pos[0]
        body.position.y = pos[1]
        body.angular_velocity_limit = 0
        self.manager.add_component(entity, body)
        shape = pm.Poly.create_box(body, (x, y))
        shape.elasticity = 1.3
        shape.friction = 0
        shape.collision_type = constants.PADDLE_COLLISION_TYPE
        self.manager.add_component(entity, shape)
        self.space.add(body, shape)
        return entity


class BallArchetype(BaseArchetype):
    """A ball bounces against obstacles and fall into the void"""
    def create_entity(self, x, y, v):
        entity = self.manager.create_entity()
        inertia = pm.moment_for_circle(constants.BALL_MASS, 0, 15)
        body = pm.Body(constants.BALL_MASS, inertia)
        body.position.x = x
        body.position.y = y
        body.apply_impulse(v)
        body.velocity_limit = 300
        self.manager.add_component(entity, body)
        shape = pm.Circle(body, constants.BALL_RADIUS)
        shape.elasticity = 1
        shape.friction = 0
        shape.collision_type = constants.BALL_COLLISION_TYPE
        self.manager.add_component(entity, pm.Circle(body, 15))
        self.manager.add_component(entity, shape)
        self.space.add(body, shape)
        return entity


class FieldArchetype(BaseArchetype):
    """A field has two walls and two deadly voids"""
    def create_entity(self, width, height):
        body = pm.Body()
        bottom_wall = pm.Segment(
            body,
            (0, -constants.WALL_THICKNESS),
            (width, -constants.WALL_THICKNESS),
            constants.WALL_THICKNESS
        )
        bottom_wall.elasticity = 1
        bottom_wall.friction = 0
        bottom_wall.collision_type = constants.WALL_COLLISION_TYPE
        top_wall = pm.Segment(
            body,
            (0, height+constants.WALL_THICKNESS),
            (width, height+constants.WALL_THICKNESS),
            constants.WALL_THICKNESS
        )
        top_wall.elasticity = 1
        top_wall.friction = 0
        top_wall.collision_type = constants.WALL_COLLISION_TYPE
        self.space.add(bottom_wall)
        self.space.add(top_wall)
        left_void = pm.Segment(
            body,
            (-constants.WALL_THICKNESS, 0),
            (-constants.WALL_THICKNESS, height),
            constants.WALL_THICKNESS
        )
        left_void.collision_type = constants.VOID_LEFT_COLLISION_TYPE
        right_void = pm.Segment(
            body,
            (width+constants.WALL_THICKNESS, 0),
            (width+constants.WALL_THICKNESS, height),
            constants.WALL_THICKNESS
        )
        right_void.collision_type = constants.VOID_RIGHT_COLLISION_TYPE
        self.space.add(left_void)
        self.space.add(right_void)
