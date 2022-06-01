import sys
import pygame as pg
from pygame.math import Vector2
from data.constants import BACKGROUND_COLOR
from data.constants import BULLET_RADIUS
from data.constants import UI_FONT_COLOR
from data.constants import FONT_FILE
from data.constants import FONT_SIZES
from data.constants import FPS
from data.constants import GAME_OVER_FONT_COLOR
from data.constants import PAUSE_FONT_COLOR
from data.constants import PAUSE_OVERLAY_ALPHA
from data.constants import PAUSE_OVERLAY_COLOR
from data.constants import PLAYER_RADIUS
from data.constants import RESTART_FONT_COLOR
from data.constants import SURFACE_SIZE
from data.constants import TITLE
from data.constants import UI_BORDER_OFFSET
from data.game_object import Bullet
from data.game_object import Enemy
from data.game_object import Player

"""main game script"""


def create_text_surface(text, color, size_index=0):
    """returns a surface with colored text"""
    return font[size_index].render(text, False, color)


def reset_game():
    """resets game data"""
    global obj
    obj = {
        "player": Player(SURFACE_SIZE / 2),
        "bullets": [],
        "enemies": []}
    global stats
    stats = {
        "bullets": 10,
        "killed": 0}


# initialize pygame
pg.init()
pg.display.set_caption(TITLE)
# create fonts
font = [pg.font.Font(FONT_FILE, font_size) for font_size in FONT_SIZES]
# program info
clock = pg.time.Clock()
input = Vector2(0)
program = {
    "pause": False,
    "running": True}
# game data
obj = None
stats = None
# create surfaces
surface = {
    "main": pg.display.set_mode(SURFACE_SIZE),
    "fade": pg.Surface(SURFACE_SIZE),
    "text": {
        "pause": create_text_surface("Paused", PAUSE_FONT_COLOR),
        "game_over": create_text_surface("GAME OVER", GAME_OVER_FONT_COLOR, 1),
        "restart": create_text_surface("PreSURFACE_SIZE SPACE to restart", RESTART_FONT_COLOR)}}
surface["fade"].fill(PAUSE_OVERLAY_COLOR)
surface["fade"].set_alpha(PAUSE_OVERLAY_ALPHA)
# reset game
reset_game()


# loop
while program["running"]:

    # handle events
    for event in pg.event.get():
        match event.type:
            case pg.QUIT:
                # actions when window is closed
                program["running"] = False
            case pg.KEYDOWN:
                # actions for keydown events
                match event.key:
                    case pg.K_END:
                        program["running"] = False
                    case pg.K_PAGEDOWN:
                        pg.display.iconify()
                    # handle pause toggling
                    case pg.K_ESCAPE:
                        if obj["player"].is_alive():
                            program["pause"] = not program["pause"]
                            if program["pause"]:
                                # draw pausing overlay
                                surface["main"].blits([
                                    (surface["fade"], (0, 0)),
                                    (surface["text"]["pause"], ((SURFACE_SIZE - surface["text"]["pause"].get_size()) / 2))])
                     # restart game button
                    case pg.K_SPACE:
                        if not obj["player"].is_alive():
                            reset_game()
                # movement input
                match event.key:
                    case pg.K_w:
                        input.y -= 1
                    case pg.K_s:
                        input.y += 1
                    case pg.K_a:
                        input.x -= 1
                    case pg.K_d:
                        input.x += 1
            case pg.KEYUP:
                # movement input
                match event.key:
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
                        if not program["pause"] and stats["bullets"] > 0 and obj["player"].is_alive():
                            # Calculate direction of bullet from player to mouse
                            mouse_pos = pg.mouse.get_pos()
                            start_pos = obj["player"].pos.copy()
                            direction = (mouse_pos - start_pos).normalize()
                            # make bullet start in front of player
                            start_offset = direction.normalize() * (PLAYER_RADIUS + BULLET_RADIUS)
                            start_pos += start_offset
                            # Create new bullet object
                            obj["bullets"].append(
                                Bullet(start_pos, direction))
                            stats["bullets"] -= 1
                    # right mouse button click
                    # TODO remove, only for debugging
                    case 3:
                        if not program["pause"]:
                            # create new enemy
                            obj["enemies"].append(
                                Enemy(Vector2(pg.mouse.get_pos())))

    # check pause
    if not program["pause"]:

        # TODO spawn enemies naturally
        # reset screen
        surface["main"].fill(BACKGROUND_COLOR)
        # update game objects
        if obj["player"].is_alive():
            obj["player"].update(input)
        for enemy in obj["enemies"]:
            enemy.update(obj["player"])
        for bullet in obj["bullets"]:
            bullet.update()
            # check bullet collision
            for enemy in obj["enemies"]:
                # if bullet hits enemy
                if bullet.is_touching(enemy):
                    bullet.life = 0
                    enemy.life -= 1
                    # increment bullet and kill count
                    for stat in ["bullets", "killed"]:
                        stats[stat] += 1
        # remove dead game objects
        for obj_str in ["enemies", "bullets"]:
            obj[obj_str] = [go for go in obj[obj_str] if go.is_alive()]
        # draw game objects
        if obj["player"].is_alive():
            obj["player"].draw(surface["main"])
        for obj_str in ["enemies", "bullets"]:
            for go in obj[obj_str]:
                go.draw(surface["main"])
        # display appropriate ui
        if obj["player"].is_alive():
            ui = [f"{stat}: {stats[stat]}" for stat in ["bullets", "killed"]]
            ui.append(f"life: {obj['player'].life}")
            current_height = SURFACE_SIZE.y - UI_BORDER_OFFSET
            for i in range(len(ui)):
                # create text surface from string
                debug_surface = create_text_surface(ui[i], UI_FONT_COLOR)
                # move upwards from last height
                current_height -= debug_surface.get_height()
                # replace index with blit information
                ui[i] = (debug_surface, (UI_BORDER_OFFSET + 5, current_height))
            # blit surfaces
            surface["main"].blits(ui)
        else:
            # blit game over screen
            surface["main"].blit(surface["fade"], (0, 0))
            center = SURFACE_SIZE / 2
            surface["main"].blit(surface["text"]["game_over"],
                                 (center - (Vector2(surface["text"]["game_over"].get_size()) / 2)))
            center.y += surface["text"]["game_over"].get_height()
            surface["main"].blit(surface["text"]["restart"],
                                 (center - (Vector2(surface["text"]["restart"].get_size()) / 2)))

    # display surface
    pg.display.flip()
    # fps lock
    clock.tick(FPS)
    # end of game loop

# end of program
pg.quit()
sys.exit()
