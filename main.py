import sys
import pygame as pg
from pygame.math import Vector2
from data.constants import BACKGROUND_COLOR
from data.constants import BULLET_RADIUS
from data.constants import DEBUG_FONT_COLOR
from data.constants import FONT_FILE
from data.constants import FONT_SIZE
from data.constants import FPS
from data.constants import PAUSE_FONT_COLOR
from data.constants import PAUSE_OVERLAY_ALPHA
from data.constants import PAUSE_OVERLAY_COLOR
from data.constants import PLAYER_RADIUS
from data.constants import SURFACE_SIZE as SS
from data.constants import TITLE
from data.game_object import Bullet
from data.game_object import Enemy
from data.game_object import Player

"""main game script"""

# initialize pygame
pg.init()
# create main window with title
surface = pg.display.set_mode(SS)
pg.display.set_caption(TITLE)
# create font
font = pg.font.Font(FONT_FILE, FONT_SIZE)


def create_text_surface(text, color):
    """returns a surface with colored text"""
    return font.render(text, False, color)


# create pause overlay
surface_pause = pg.Surface(SS)
surface_pause.fill(PAUSE_OVERLAY_COLOR)
surface_pause.set_alpha(PAUSE_OVERLAY_ALPHA)
surface_pause_text = create_text_surface("Paused", PAUSE_FONT_COLOR)
# create game clock
clock = pg.time.Clock()
# create player
player = Player(SS / 2)
# create list of current game objects
game_objects = []
# movement input variables
input = Vector2(0)
# program running and pause states
running, pause = True, False

# loop
while running:

    # handle events
    for event in pg.event.get():
        match event.type:
            case pg.QUIT:
                # actions when window is closed
                running = False
            case pg.KEYDOWN:
                # actions for keydown events
                match event.key:
                    case pg.K_END:
                        running = False
                    case pg.K_PAGEDOWN:
                        pg.display.iconify()
                    # handle pause toggling
                    case pg.K_ESCAPE:
                        pause = not pause
                        if pause:
                            # draw pausing overlay
                            surface.blits([
                                (surface_pause, (0, 0)),
                                (surface_pause_text, ((
                                    SS.x / 2) - (surface_pause_text.get_width() / 2), (
                                    SS.y / 2) - (surface_pause_text.get_height() / 2)))])
                    # movement input
                    case pg.K_w:
                        input.y -= 1
                    case pg.K_s:
                        input.y += 1
                    case pg.K_a:
                        input.x -= 1
                    case pg.K_d:
                        input.x += 1
            case pg.KEYUP:
                # actions for keyup events
                match event.key:
                    # movement input
                    case pg.K_w:
                        input.y += 1
                    case pg.K_s:
                        input.y -= 1
                    case pg.K_a:
                        input.x += 1
                    case pg.K_d:
                        input.x -= 1
            case pg.MOUSEBUTTONDOWN:
                # actions for mouse button down events
                match event.button:
                    # left mouse button click
                    case 1:
                        if not pause:
                            # Calculate direction of bullet from player to mouse
                            mouse_pos = pg.mouse.get_pos()
                            start_pos = player.pos.copy()
                            direction = (mouse_pos - start_pos).normalize()
                            # make bullet start in front of player
                            start_offset = direction.normalize() * (PLAYER_RADIUS + BULLET_RADIUS)
                            start_pos += start_offset
                            # Create new bullet object
                            game_objects.append(Bullet(start_pos, direction))
                    # right mouse button click
                    # TODO remove, only for debugging
                    case 3:
                        if not pause:
                            # create new enemy
                            game_objects.append(Enemy(Vector2(0, 0)))

    # check pause
    if not pause:

        # TODO spawn enemies
        # reset screen
        surface.fill(BACKGROUND_COLOR)
        # update game objects
        player.update(input)
        player.draw(surface)
        for go in game_objects:
            go.update(player.pos)
            go.draw(surface)
        # remove dead game objects
        game_objects = [go for go in game_objects if go.is_alive()]
        # draw game objects
        debug_prints = [
            f"move_x: {input.x}",
            f"move_y: {input.y}",
            f"pos_x: {player.pos.x:.2f}",
            f"pos_y: {player.pos.y:.2f}",
            f"objs: {len(game_objects)}"]
        # get current screen height
        current_height = SS.y
        # use each string in the array to create a surface
        for i in range(len(debug_prints)):
            # create text surface from string
            debug_surface = create_text_surface(
                debug_prints[i], DEBUG_FONT_COLOR)
            # move upwards from last height
            current_height -= debug_surface.get_height()
            # replace index with blit information
            debug_prints[i] = (debug_surface, Vector2(2, current_height))
        # blit surfaces
        surface.blits(debug_prints)

    # display surface
    pg.display.flip()
    # fps lock
    clock.tick(FPS)

# exit code
pg.quit()
sys.exit()
