import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame
import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d
import shapely.geometry as sg
import cv2
import importlib

from .pymunk_override import DrawOptions


OBJECT_NAME_LIST = [
    't', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'ellipse', 'rectangle', 'reg3', 'reg4', 'reg5', 'reg6', 'reg7', 'reg8', 'reg9', 'reg10'
]

def pymunk_to_shapely(body, shapes):
    geoms = []
    for shape in shapes:
        if isinstance(shape, pymunk.shapes.Poly):
            verts = [body.local_to_world(v) for v in shape.get_vertices()]
            verts.append(verts[0])
            geoms.append(sg.Polygon(verts))
        else:
            raise RuntimeError(f'Unsupported shape type {type(shape)}')
    return sg.MultiPolygon(geoms)

class PushAnyEnv(gym.Env):
    metadata = {"render_modes": ['human', 'rgb_array'], "render_fps": 10}
    reward_range = (0., 1.)

    def __init__(
        self,
        legacy=False, 
        block_cog=None, damping=None,
        render_mode="rgb_array",
        render_action=True,
        render_size=96,
        window_size=384,
        reset_to_state=None,
        object_name='t',
        use_obstacles=True
    ):
        super().__init__()
        self.legacy = legacy
        self.block_cog = block_cog
        self.damping = damping
        self.render_mode = render_mode
        self.render_action = render_action
        self.render_size = render_size
        self.window_size = window_size
        self.reset_to_state = reset_to_state
        self.object_name = object_name
        self.use_obstacles = use_obstacles
        self._seed = None
        self.seed()

        self.sim_hz = 100
        self.k_p, self.k_v = 100, 20
        self.control_hz = self.metadata['render_fps']

        self.observation_space = spaces.Dict({
            "pixels": spaces.Box(
                low=0, high=255, shape=(self.render_size, self.render_size, 3), dtype=np.uint8
            ),
            "agent_pos": spaces.Box(
                low=np.array([0, 0]), high=np.array([512, 512]), dtype=np.float64
            )
        })

        self.action_space = spaces.Box(
            low=np.array([0, 0], dtype=np.float64),
            high=np.array([self.window_size, self.window_size], dtype=np.float64),
            shape=(2,),
            dtype=np.float64
        )

        self.window = None
        self.clock = None
        self.space = None
        self.latest_action = None
        self.obstacles = []
        self.n_contact_points = 0 

    def seed(self, seed=None):
        if seed is None:
            seed = np.random.randint(0,25536)
        self._seed = seed
        self.np_random = np.random.default_rng(seed)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self._setup_environment()
        state = self.reset_to_state or self._generate_random_state(seed)
        self._set_state(state)
        return self.get_obs(), self._get_info(is_success=False)

    def step(self, action):
        self.latest_action = action
        self._apply_action(action)
        coverage = self._calculate_coverage()
        reward = np.clip(coverage / self.success_threshold, 0, 1)
        is_success = coverage > self.success_threshold
        return self.get_obs(), reward, is_success, False, self._get_info(is_success)

    def render(self):
        return self._render_frame(self.render_mode, visualize=True)

    def get_obs(self):
        return {
            "pixels": self._render_frame(self.render_mode),
            "agent_pos": np.array(self.agent.position)
        }

    def _setup_environment(self):
        self.space = pymunk.Space()
        self.space.gravity = (0, 0)
        self.space.damping = self.damping or 0
        self._add_walls()
        self.agent = self._add_circle((256, 400), 15)
        self.block = self._add_object((256, 300), 0, self.object_name)
        self.goal_pose = self._generate_random_goal_pose()
        if self.use_obstacles:
            self._add_obstacles()
        self._setup_collision_handler()
        self.n_contact_points = 0
        self.success_threshold = 0.95

    def _generate_random_state(self, seed):
        rs = np.random.RandomState(seed=seed)
        return np.array([
            rs.randint(50, 450), rs.randint(50, 450),
            rs.randint(100, 400), rs.randint(100, 400),
            rs.uniform(-np.pi, np.pi)
        ])

    def _generate_random_goal_pose(self):
        rs = np.random.RandomState(seed=self._seed)
        return np.array([
            rs.randint(80, 420), rs.randint(80, 420),
            rs.uniform(-np.pi, np.pi)
        ])

    def _apply_action(self, action):
        dt = 1.0 / self.sim_hz
        n_steps = self.sim_hz // self.control_hz
        for _ in range(n_steps):
            acceleration = self.k_p * (action - self.agent.position) + self.k_v * (-self.agent.velocity)
            self.agent.velocity += acceleration * dt
            self.space.step(dt)

    def _calculate_coverage(self):
        goal_geom = pymunk_to_shapely(self._get_goal_pose_body(self.goal_pose), self.block.shapes)
        block_geom = pymunk_to_shapely(self.block, self.block.shapes)
        intersection_area = goal_geom.intersection(block_geom).area
        return intersection_area / goal_geom.area

    def _get_goal_pose_body(self, pose):
        mass = 1
        inertia = pymunk.moment_for_box(mass, (50, 100))
        body = pymunk.Body(mass, inertia)
        body.position = tuple(pose[:2])
        body.angle = pose[2]
        return body

    def _get_info(self, is_success):
        return {
            'pos_agent': np.array(self.agent.position),
            'vel_agent': np.array(self.agent.velocity),
            'block_pose': np.array(list(self.block.position) + [self.block.angle]),
            'goal_pose': self.goal_pose,
            'is_success': is_success
        }

    def _render_frame(self, mode, visualize=False):
        width, height = (self.window_size, self.window_size) if visualize else (self.render_size, self.render_size)
        if self.window is None and mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.window_size, self.window_size))
        if self.clock is None and mode == "human":
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface((512, 512))
        canvas.fill((255, 255, 255))
        draw_options = DrawOptions(canvas)

        goal_body = self._get_goal_pose_body(self.goal_pose)
        for shape in self.block.shapes:
            goal_points = [pymunk.pygame_util.to_pygame(goal_body.local_to_world(v), draw_options.surface) for v in shape.get_vertices()]
            goal_points += [goal_points[0]]
            pygame.draw.polygon(canvas, pygame.Color('LightGreen'), goal_points)

        self.space.debug_draw(draw_options)

        if mode == "human":
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

        img = np.transpose(np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2))
        img = cv2.resize(img, (width, height))
        if self.render_action and self.latest_action is not None:
            coord = (np.array(self.latest_action) / 512 * [width, height]).astype(np.int32)
            cv2.drawMarker(img, coord, color=(255, 0, 0), markerType=cv2.MARKER_CROSS, markerSize=8, thickness=1)
        return img

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()

    def _add_walls(self):
        walls = [
            self._add_segment((5, 506), (5, 5), 2),
            self._add_segment((5, 5), (506, 5), 2),
            self._add_segment((506, 5), (506, 506), 2),
            self._add_segment((5, 506), (506, 506), 2)
        ]
        self.space.add(*walls)

    def _add_segment(self, a, b, radius):
        shape = pymunk.Segment(self.space.static_body, a, b, radius)
        shape.friction = 0.1
        shape.color = pygame.Color('LightGray')
        return shape

    def _add_circle(self, position, radius):
        body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        body.position = position
        shape = pymunk.Circle(body, radius)
        shape.color = pygame.Color('RoyalBlue')
        self.space.add(body, shape)
        return body
    

    def _add_object(self, position, angle, object_name='t', scale=30, color='LightSlateGray', mask=pymunk.ShapeFilter.ALL_MASKS(), body_type=pymunk.Body.DYNAMIC):
        module_name = "gym_pushany.envs.objects"
        function_name = f"add_{object_name.upper()}"
        if object_name.isdigit():
            function_name = "add_digit"
            digit = int(object_name)
        elif object_name in ['ellipse', 'rectangle'] or 'reg' in object_name:
            function_name = "add_shape"

        try:
            module = importlib.import_module(module_name)
            add_function = getattr(module, function_name)
        except ImportError:
            raise ImportError(f"Failed to import module {module_name} or function {function_name}")

        # digit
        if object_name.isdigit():
            body = add_function(self, digit, position, angle, scale, color, mask, body_type)
        # shape  
        elif object_name in ['ellipse', 'rectangle'] or 'reg' in object_name:
            body = add_function(self, object_name, position, angle, scale, color, mask, body_type)
        # alphabet
        else:
            body = add_function(self, position, angle, scale, color, mask, body_type)
        return body

    def _add_obstacles(self):
        rs = np.random.RandomState(seed=self._seed)
        num_obstacles = rs.randint(0, 5)
        object_names = rs.choice(OBJECT_NAME_LIST, num_obstacles)
        object_scales = rs.randint(10, 30, num_obstacles)

        for i in range(num_obstacles):
            pos = (rs.randint(80, 420), rs.randint(80, 420))
            rot = rs.uniform(-np.pi, np.pi)
            while np.linalg.norm(np.array(pos) - self.goal_pose[:2]) < 150:
                pos = (rs.randint(80, 420), rs.randint(80, 420))
            obstacle = self._add_object(pos, rot, object_name=object_names[i], scale=object_scales[i], color='Red')
            self.obstacles.append(obstacle)

    def _setup_collision_handler(self):
        self.handler = self.space.add_collision_handler(0, 0)
        self.handler.post_solve = self._handle_collision

    def _handle_collision(self, arbiter, space, data):
        self.n_contact_points += len(arbiter.contact_point_set.points)

    def _set_state(self, state):
        self.agent.position = tuple(state[:2])
        if self.legacy:
            self.block.position = tuple(state[2:4])
            self.block.angle = state[4]
        else:
            self.block.angle = state[4]
            self.block.position = tuple(state[2:4])
        self.space.step(1.0 / self.sim_hz)
