import numpy as np
import pygame as pg
from pythonScripts.playerClass import Player


class Collision:
    previous_x: int = 0
    previous_y: int = 0

    @classmethod
    def create_collision(cls, game_map: np.array, shift_x: int, shift_y: int) -> tuple[list[pg.Rect], list[pg.Rect]]:
        """
        the method creates collisions on the map based on the game map
        :param game_map:
        :param shift_x:
        :param shift_y:
        :return: stone_collisions, door_collisions
        """
        allowed_stone_values: set[range] = {1, 2, 3, *range(9, 27), *range(35, 47)}
        allowed_door_values: set[range] = {*range(28, 32)}

        stone_collisions: list[pg.Rect] = []
        door_collisions: list[pg.Rect] = []

        # create collisions from stones
        for row_index, row in enumerate(game_map):
            for col_index, col in enumerate(row):
                if col in allowed_stone_values:
                    rect = pg.Rect(col_index * 30 + 300 + shift_x, row_index * 30 + 90 + shift_y, 30, 30)
                    stone_collisions.append(rect)

        # create collisions from doors
        for row in range(len(game_map)):
            for column in range(len(game_map[0])):
                if game_map[row][column] in allowed_door_values:
                    rect = pg.Rect(column * 30 + 300 + shift_x, row * 30 + 90 + shift_y, 30, 30)
                    door_collisions.append(rect)

        return stone_collisions, door_collisions

    @classmethod
    def move_all_collisions(cls, move_screen_x: int, move_screen_y: int,
                            collisions: tuple[list[pg.Rect], list[pg.Rect]]) -> None:
        """
        the method shifts collisions based on the shift of the game window, for which the player is responsible
        :param move_screen_x:
        :param move_screen_y:
        :param collisions:
        :return: None
        """

        if cls.previous_x != move_screen_x or cls.previous_y != move_screen_y:
            # stone collision
            for i in range(len(collisions[0])):
                collisions[0][i] = collisions[0][i].move(move_screen_x - cls.previous_x,
                                                         move_screen_y - cls.previous_y)
            # door collision
            for i in range(len(collisions[1])):
                collisions[1][i] = collisions[1][i].move(move_screen_x - cls.previous_x,
                                                         move_screen_y - cls.previous_y)

        cls.previous_x = move_screen_x
        cls.previous_y = move_screen_y

    @classmethod
    def player_collision_with_door(cls, player: Player, door_hit_box: list[pg.Rect],
                                   small_map: bool = False) -> tuple[bool, int]:
        """
        the method informs which door the collision occurred with,
        transmits this information and sets the camera and player positions
        :param player:
        :param door_hit_box:
        :param small_map:
        :return: True / False, number_of_door
        """
        if any(player.movement_hit_box.colliderect(i) for i in door_hit_box):
            # collision with right edge door
            if (1650 > player.x_cord > 1550) and (940 > player.y_cord > 140):
                if small_map:
                    Player.x_move_collision = -Player.x_move_screen
                    Player.x_move_screen = 0
                else:
                    Player.x_move_screen = 0
                    Player.x_move_collision = -600

                number_of_door = 1

            # collision with left edge door
            elif (330 > player.x_cord > 270) and (940 > player.y_cord > 140):
                if small_map:
                    Player.x_move_screen = -Player.x_move_collision
                    Player.x_move_collision = 0
                else:
                    Player.x_move_screen = 600
                    Player.x_move_collision = 0

                number_of_door = 2

            # collision with top edge door
            elif (1570 > player.x_cord > 300) and (120 > player.y_cord > 60):
                if small_map:
                    Player.y_move_screen = -Player.y_move_collision
                    Player.y_move_collision = 0
                else:
                    Player.y_move_screen = 180
                    Player.y_move_collision = 0

                number_of_door = 4

            # collision with bottom edge door
            elif (1570 > player.x_cord > 300) and (1020 > player.y_cord > 910):
                if small_map:
                    Player.y_move_collision = -Player.y_move_screen
                    Player.y_move_screen = 0
                else:
                    Player.y_move_screen = 0
                    Player.y_move_collision = -180

                number_of_door = 3

            # collision with cave door
            else:
                number_of_door = 5

            return True, number_of_door

        return False, 0
