from lutes import System
import constants


class Physics(System):
    def __init__(self, space):
        super().__init__(1)
        self.space = space
        self.space.add_collision_handler(
            constants.BALL_COLLISION_TYPE,
            constants.VOID_LEFT_COLLISION_TYPE,
            post_solve=self.emit_left_void
        )
        self.space.add_collision_handler(
            constants.BALL_COLLISION_TYPE,
            constants.VOID_RIGHT_COLLISION_TYPE,
            post_solve=self.emit_right_void
        )
        self.space.add_collision_handler(
            constants.BALL_COLLISION_TYPE,
            constants.PADDLE_COLLISION_TYPE,
            post_solve=self.emit_paddle
        )
        self.space.add_collision_handler(
            constants.BALL_COLLISION_TYPE,
            constants.WALL_COLLISION_TYPE,
            post_solve=self.emit_wall
        )

    def update(self, delta):
        self.space.step(delta)

    def emit_left_void(self, space, arbiter):
        self.manager.dispatch_event(
            'collide_void_left',
            {
                'space': space,
                'arbiter': arbiter
            }
        )

    def emit_right_void(self, space, arbiter):
        self.manager.dispatch_event(
            'collide_void_right',
            {
                'space': space,
                'arbiter': arbiter
            }
        )

    def emit_wall(self, space, arbiter):
        self.manager.dispatch_event(
            'collide_wall',
            {
                'space': space,
                'arbiter': arbiter
            }
        )

    def emit_paddle(self, space, arbiter):
        self.manager.dispatch_event(
            'collide_paddle',
            {
                'space': space,
                'arbiter': arbiter
            }
        )
