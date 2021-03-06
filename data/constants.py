import random
from math import cos
from math import pi
from math import sin
from pygame import Color
from pygame import Vector2
from pygame.font import Font

""" constant game values """

def seconds_to_frames(seconds: float) -> int:
    """returns the amount of frames in the given amount of seconds"""
    return int(FPS * seconds)

def make_framerate_independent(value: float) -> float:
    """returns the value in frames per second"""
    return value / FPS

def random_vector() -> Vector2:
    """returns a unit vector with a random direction"""
    random_angle = random.uniform(0, 2 * pi)
    return Vector2(cos(random_angle), sin(random_angle))

def create_font(size: int) -> Font:
    """creates a font object of specified size"""
    return Font(FONT_FILE, size)

# window properties
TITLE = "Python Game"
FPS = 65.0

# camera
_CAMERA_SPEED = 0.05  # [0.0 - 1.0]
CAMERA_SPEED = (FPS * _CAMERA_SPEED) / FPS

# text
TEXT_DEBUG = "DEBUG INFO:"
TEXT_GAME_OVER = "GAME OVER"
TEXT_PAUSE = "Paused"
TEXT_RESTART = "Press SPACE to restart..."

# ui
AIM_LINE_LENGTH = 40
AIM_LINE_WIDTH = 3
DEBUG_LINE_WIDTH = 2
UI_BORDER_OFFSET = 15
UI_WEAPON_WIDTH = 10

# font file
FONT_FILE = "data/upheavtt.ttf"

# colors
AIM_LINE_COLOR = Color(255, 255, 255)
BULLET_COLOR = Color(0, 128, 255)
DEBUG_LINE_COLOR = Color(255, 64, 128)
ENEMY_COLORS = [Color(64, 255, 16),
                Color(192, 128, 16),
                Color(255, 32, 0)]
PAUSE_OVERLAY_COLOR = Color(0, 0, 0, 192)
PLAYER_COLOR = Color(0, 255, 255)
WEAPON_COOLDOWN_COLOR = Color(255, 224, 64)
WEAPON_RELOAD_COLOR = Color(255, 128, 96)

# player
PLAYER_I_FRAMES = seconds_to_frames(3)
PLAYER_LIFE = 3
PLAYER_RADIUS = 16
PLAYER_SPEED = 200.0

# bullet
BULLET_LIFE = seconds_to_frames(0.75)
BULLET_RADIUS = 8
BULLET_SPEED = 550.0

# enemy
ENEMY_LIFE = len(ENEMY_COLORS)
ENEMY_RADIUS = 24
ENEMY_DESPAWN_RATE = seconds_to_frames(15)
ENEMY_SPAWN_RATE = seconds_to_frames(1.25)
ENEMY_SPEED = 150.0
ENEMY_TRACKING = make_framerate_independent(1.5)
