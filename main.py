import pygame as pg
from pythonScripts.colisionClass import Collision
from pythonScripts.drawMap import DrawMap
from pythonScripts.mapChooseClass import MapChoose
from pythonScripts.playerClass import Player
from pythonScripts.settings import Settings
from pythonScripts.changeMap import ChangeMap

# pygame initialization
pg.init()

# main window set up
screen_width = Settings.SCREEN_WIDTH
screen_height = Settings.SCREEN_HEIGHT
screen = pg.display.set_mode((screen_width, screen_height))

# create map
game_map, game_map_width, game_map_height = MapChoose.create_map(True)
background_surface = DrawMap.draw_map(game_map[0], game_map_width, game_map_height, screen_width, screen_height)
collision = Collision.create_collision(game_map[0], 0, 0)
ChangeMap.add_new_map_into_map_list(game_map, game_map_width, game_map_height, background_surface, collision, 1)

player = Player(910, 500)

# font initialization
font = pg.font.Font(None, 36)

# clock initialization
clock = pg.time.Clock()

# read images
left_image = pg.image.load('./interface_images/left.jpeg').convert_alpha()
top_image = pg.image.load('./interface_images/top.jpeg').convert_alpha()

# main game loop
running = True
while running:
    # check events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

    # player movement control
    keys = pg.key.get_pressed()

    # the function moves the player, collisions and, if necessary, the game window
    move_screen = player.player_make_move(keys, ChangeMap.map_list[ChangeMap.index_of_current_map][4][0],
                                          ChangeMap.map_list[ChangeMap.index_of_current_map][0][3])

    # if the function above returns the appropriate parameter, the collisions move along with the game window
    Collision.move_all_collisions(move_screen[2], move_screen[3],
                                  (ChangeMap.map_list[ChangeMap.index_of_current_map][4][0],
                                   ChangeMap.map_list[ChangeMap.index_of_current_map][4][1]))

    # the function is responsible for drawing only the fragment of the game window that is displayed at the beginning
    fragment_of_background = pg.Rect(move_screen[0], move_screen[1], 1320, 900)
    screen.blit(ChangeMap.map_list[ChangeMap.index_of_current_map][3], (300, 90), fragment_of_background)

    # the function informs whether the player collided with a door and which one it was
    collision_with_door, door_number_with_collision = Collision.player_collision_with_door(player, ChangeMap.map_list[
        ChangeMap.index_of_current_map][4][1])

    # temporary code to create another map when going through a door and setting collision
    ChangeMap.check_collision_witch_door(collision_with_door, door_number_with_collision,
                                         (move_screen[0], move_screen[1]), player)

    # a piece of code responsible for drawing collisions
    # for i in ChangeMap.map_list[ChangeMap.index_of_current_map][4][1]:
    #     pg.draw.rect(screen, (255, 255, 255), i)

    # drawing blackout for cave mode
    if ChangeMap.map_list[ChangeMap.index_of_current_map][0][2]:
        pg.draw.rect(screen, (128, 128, 128), (300, 90, player.x_cord - 500, 900))
        pg.draw.rect(screen, (128, 128, 128), (player.x_cord + 230, 90, 1200, 900))
        pg.draw.rect(screen, (128, 128, 128), (player.x_cord - 200, 90, 430, player.y_cord - 280))
        pg.draw.rect(screen, (128, 128, 128), (player.x_cord - 200, player.y_cord + 230, 430, player.y_cord + 600))

    # player drawing
    player.player_draw(screen)

    # Displaying the number of frames per second
    fps = clock.get_fps()
    fps_text = font.render(f'FPS: {fps:.2f}', True, (255, 255, 255))
    screen.blit(fps_text, (310, 100))

    # Drawing the interface
    screen.blit(left_image, (0, 0))
    screen.blit(left_image, (1620, 0))
    screen.blit(top_image, (300, 0))
    screen.blit(top_image, (300, 990))

    # Screen update
    pg.display.update()

    # Frame rate setting
    clock.tick(65)

# game quit
pg.quit()
