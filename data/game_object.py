from pygame import Color
from pygame import Surface
from pygame.draw import circle as draw_circle
from pygame.math import Vector2
from abc import ABC
from abc import abstractmethod
from .constants import BULLET_COLOR
from .constants import BULLET_LIFE
from .constants import BULLET_RADIUS
from .constants import BULLET_SPEED
from .constants import ENEMY_COLOR
from .constants import ENEMY_LIFE
from .constants import ENEMY_RADIUS
from .constants import ENEMY_SPEED
from .constants import FPS
from .constants import PLAYER_COLOR
from .constants import PLAYER_I_FRAMES
from .constants import PLAYER_LIFE
from .constants import PLAYER_RADIUS
from .constants import PLAYER_SPEED


# abstract class
class GameObject(ABC):
    """in-game objects"""

    @abstractmethod
    def __init__(self, pos: Vector2, radius: float, speed: float, color: Color, life: float = None):
        self.pos = pos
        self.radius = radius
        self.speed = speed
        self.color = color
        self.life = life
        self.direction = Vector2(0)

    def is_alive(self) -> bool:
        """returns if the game object has life remaining"""
        return self.life > 0.0

    def update(self) -> None:
        """moves the game object with its direction"""
        self.pos += (self.direction * self.speed) / FPS

    def draw(self, surface: Surface, camera_offset: Vector2) -> None:
        """draws the object to the surface"""
        draw_circle(surface, self.color, self.pos -
                    camera_offset, self.radius)

    def is_touching(self, other: 'GameObject') -> bool:
        return (self.pos - other.pos).magnitude() < self.radius + other.radius


class Player(GameObject):
    """player game object"""

    def __init__(self, pos: Vector2):
        super().__init__(pos, PLAYER_RADIUS, PLAYER_SPEED, PLAYER_COLOR, PLAYER_LIFE)
        self.i_frames = 0

    def is_vulnerable(self) -> bool:
        """returns if the player can take damage"""
        return self.i_frames == 0

    def damage(self) -> None:
        """reduces the player's life and starts i-frames"""
        if self.is_vulnerable():
            self.life -= 1
            self.i_frames = PLAYER_I_FRAMES

    def update(self, input: Vector2) -> None:
        """used to handle movement input"""
        # handle i-frames
        if not self.is_vulnerable():
            self.i_frames -= 1
        # normalize input vector
        self.direction = input
        if self.direction.length() != 0.0 and not self.direction.is_normalized():
            self.direction = self.direction.normalize()
        # update movement this frame
        super().update()

    def draw(self, surface: Surface, camera_offset: Vector2) -> None:
        """draws the player. if damaged, draw every other frame"""
        if self.i_frames % 2 == 0:
            super().draw(surface, camera_offset)


class Bullet(GameObject):
    """bullet game object"""

    def __init__(self, pos: Vector2, direction: Vector2):
        super().__init__(pos, BULLET_RADIUS, BULLET_SPEED, BULLET_COLOR, BULLET_LIFE)
        self.direction = direction

    def update(self) -> None:
        # tick life
        self.life -= 1
        # update movement this frame
        super().update()


class Enemy(GameObject):
    """enemy game object"""

    def __init__(self, pos: Vector2):
        super().__init__(pos, ENEMY_RADIUS, ENEMY_SPEED, ENEMY_COLOR, ENEMY_LIFE)

    def update(self, player: Player) -> None:
        """moves the enemy towards the player"""
        # move towards player position
        self.direction = (player.pos - self.pos).normalize()
        # check player collision
        if test_collision(self, player):
            player.damage()
        # update movement this frame
        super().update()


def test_collision(obj_1: GameObject, obj_2: GameObject) -> bool:
    """if objects collide, reposition. returns if collided"""
    if obj_1 is not obj_2 and obj_1.is_touching(obj_2):
        # reposition self
        obj_1.pos = obj_2.pos - \
            (obj_2.pos - obj_1.pos).normalize() * (obj_1.radius + obj_2.radius)
        return True
    return False
