import random
import numpy as np
import pygame as pg
from drawMap import DrawMap
from colisionClass import Collision
from playerClass import Player
from settings import Settings
from mapChooseClass import MapChoose


class ChangeMap:
    # first: start map; second: normal map; third: cave map
    map_list: list[[np.array, int, int, pg.Surface, tuple[list, list]]] = [None, None, None]
    cave_created = False
    player_in_cave = False
    index_of_current_map = 1

    @classmethod
    def _calculate_position_of_door(cls, edge_of_game_map: np.array) -> int:
        """
        this method calculate center of door in edge of map
        :param edge_of_game_map:
        :return: center_of_door
        """
        door_length = 0
        center_of_door = 0

        for index, value in enumerate(edge_of_game_map):
            if value in (28, 29, 30, 31):
                door_length += 1

            if door_length == 2:
                center_of_door = index

            elif door_length == 4:
                center_of_door = index - 1
                break

        return center_of_door

    @classmethod
    def _find_door_position(cls, game_map: np.array, number_of_door: int, x_move_screen: int, y_move_screen: int) -> \
            tuple[int, int]:
        """
        this method sets the player's new position based on previously found doors
        :param game_map:
        :param number_of_door:
        :param x_move_screen:
        :param y_move_screen:
        :return: new_player_x_coord, new_player_y_coord
        """

        match number_of_door:
            # looking for left edge door
            case 1:
                left_column = game_map[:, 0]
                door_center = cls._calculate_position_of_door(left_column)
                new_player_x_coord = 360
                new_player_y_coord = door_center * 30 + 60 - y_move_screen
                return new_player_x_coord, new_player_y_coord

            # looking for right edge door
            case 2:
                right_column = game_map[:, -1]
                door_center = cls._calculate_position_of_door(right_column)
                new_player_x_coord = 1530
                new_player_y_coord = door_center * 30 + 60

                if y_move_screen != 0:
                    new_player_y_coord -= y_move_screen

                return new_player_x_coord, new_player_y_coord

            # looking for top edge door
            case 3:
                top_column = game_map[0, :]
                door_center = cls._calculate_position_of_door(top_column)
                new_player_x_coord = door_center * 30 + 300 + x_move_screen
                new_player_y_coord = 120 + y_move_screen

                if x_move_screen != 0:
                    new_player_x_coord -= x_move_screen * 2

                return new_player_x_coord, new_player_y_coord - 180

            # looking for bottom edge door
            case 4:
                bottom_column = game_map[-1, :]
                door_center = cls._calculate_position_of_door(bottom_column)
                new_player_x_coord = door_center * 30 + 300 + x_move_screen
                new_player_y_coord = 1050 - y_move_screen

                if x_move_screen != 0:
                    new_player_x_coord -= x_move_screen * 2

                return new_player_x_coord, new_player_y_coord - 180

    @classmethod
    def _find_cave_door_position(cls, game_map: np.array, x_move_screen: int, y_move_screen: int) -> tuple[int, int]:
        """
        auxiliary method, searches for the position of the door on the indicated edge, and then,
        based on it, sets the position of the player who will appear at this door
        :param game_map:
        :param x_move_screen:
        :param y_move_screen:
        :return: new_player_x_coord, new_player_y_coord
        """
        game_map_width = len(game_map[0])
        game_map_height = len(game_map)

        for row in range(1, game_map_height - 1):
            for column in range(1, game_map_width - 1):
                if game_map[row][column] in {*range(28, 32)}:
                    new_player_x_coord = column * 30 + 300 + x_move_screen
                    new_player_y_coord = row * 30 + 120 + y_move_screen
                    return new_player_x_coord, new_player_y_coord

    @classmethod
    def add_new_map_into_map_list(cls, game_map: np.array, game_map_width: int, game_map_height: int,
                                  background_surface: pg.Surface, collision: tuple[list, list],
                                  index: int) -> None:
        """
        this method adds a new game map to a list storing all of them
        :param game_map:
        :param game_map_width:
        :param game_map_height:
        :param background_surface:
        :param collision:
        :param index:
        :return: None (adding a map to the list on a specific position)
        """
        cls.map_list[index] = [game_map, game_map_width, game_map_height, background_surface, collision]

    @classmethod
    def delete_map_from_map_list(cls, index_to_delete: int) -> None:
        """
        this method removes the selected map from the map list
        :param index_to_delete:
        :return: None (delete map from map list)
        """
        cls.map_list.pop(index_to_delete)

    @classmethod
    def check_collision_witch_door(cls, collision_with_door: bool, door_number_with_collision: int,
                                   move_screen: tuple[int, int], player: Player) -> None:
        """
        the method is used to create a new map in the event of a collision with a door,
        or it only changes the parameter responsible for selecting the map to be displayed
        :param collision_with_door:
        :param door_number_with_collision:
        :param move_screen:
        :param player:
        :return: None (creates a new map after passing through the door or selects the appropriate map)
        """
        if collision_with_door:
            # collision with cave door when cave not created
            if door_number_with_collision == 5 and not cls.cave_created:
                cls.index_of_current_map = 2
                cls.player_in_cave = True
                cls.cave_created = True

                game_map, game_map_width, game_map_height = MapChoose.create_cave_map()

                background_surface = DrawMap.draw_map(game_map[0], game_map_width, game_map_height,
                                                      Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT,
                                                      Player.x_move_screen, Player.y_move_screen)

                collisions = Collision.create_collision(game_map[0], Player.x_move_collision + Player.x_move_screen,
                                                        Player.y_move_collision + Player.y_move_screen)

                cls.add_new_map_into_map_list(game_map, game_map_width, game_map_height, background_surface,
                                              collisions, 2)

                player.x_cord, player.y_cord = cls._find_door_position(
                    cls.map_list[cls.index_of_current_map][0][0], 4,
                    move_screen[0], move_screen[1])

                player.y_cord -= 150
                player.x_cord += player.x_move_screen

                if move_screen[1] != 0:
                    player.y_cord += move_screen[1]

            # collision with cave door when cave created
            elif door_number_with_collision == 5 and cls.cave_created:
                cls.index_of_current_map = 2
                cls.player_in_cave = True

                game_map, game_map_width, game_map_height = (cls.map_list[cls.index_of_current_map][0],
                                                             cls.map_list[cls.index_of_current_map][1],
                                                             cls.map_list[cls.index_of_current_map][2])

                background_surface = DrawMap.draw_map(game_map[0], game_map_width, game_map_height,
                                                      Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT,
                                                      Player.x_move_screen, Player.y_move_screen)

                collisions = Collision.create_collision(game_map[0], Player.x_move_collision + Player.x_move_screen,
                                                        Player.y_move_collision + Player.y_move_screen)

                (cls.map_list[cls.index_of_current_map][3],
                 cls.map_list[cls.index_of_current_map][4]) = background_surface, collisions

                player.x_cord, player.y_cord = cls._find_door_position(
                    cls.map_list[cls.index_of_current_map][0][0], 4,
                    move_screen[0], move_screen[1])

                player.y_cord -= 150
                player.x_cord += player.x_move_screen

                if move_screen[1] != 0:
                    player.y_cord += move_screen[1]

            # collision with door in cave
            elif door_number_with_collision in {*range(1, 5)} and cls.player_in_cave:
                cls.index_of_current_map = 1
                cls.player_in_cave = False

                player.x_cord, player.y_cord = cls._find_cave_door_position(
                    cls.map_list[cls.index_of_current_map][0][0], move_screen[0], move_screen[1])

                player.x_cord -= player.x_move_screen * 2

                if move_screen[1] != 0:
                    player.y_cord -= move_screen[1] * 2

            # collision with other doors
            elif door_number_with_collision in {*range(1, 5)}:
                cls.index_of_current_map = 1
                cls.cave_created = False

                cave = True if random.randint(1, 10) <= 5 else False
                house = True if random.randint(1, 10) <= 3 else False
                additional_obstacles = True if not house and random.randint(1, 10) <= 3 else False

                if house:
                    game_map, game_map_width, game_map_height = (
                        MapChoose.create_map_with_house(cave, door_number_with_collision)
                    )
                elif additional_obstacles:
                    game_map, game_map_width, game_map_height = (
                        MapChoose.create_map_with_obstacles(cave)
                    )
                else:
                    game_map, game_map_width, game_map_height = MapChoose.create_map(cave, door_number_with_collision)

                background_surface = DrawMap.draw_map(game_map[0], game_map_width, game_map_height,
                                                      Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT)

                collisions = Collision.create_collision(game_map[0], Player.x_move_collision,
                                                        Player.y_move_collision)

                cls.add_new_map_into_map_list(game_map, game_map_width, game_map_height, background_surface,
                                              collisions, 1)

                player.x_cord, player.y_cord = cls._find_door_position(
                    cls.map_list[cls.index_of_current_map][0][0], door_number_with_collision,
                    move_screen[0], move_screen[1])
