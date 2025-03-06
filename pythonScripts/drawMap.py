from time import time
import pygame as pg
from settings import Settings


class DrawMap:

    @classmethod
    def read_images(cls) -> tuple[dict, dict, dict, dict, dict, dict]:
        """
        method loads game graphics
        :return: cave_images, grass_images, door_images, rock_images, house_images, cave_ground_images
        """
        cave_images: dict = {f'cave_{i}': pg.image.load(f'./cave_and_door_images/cave{i}.png').convert_alpha() for i in
                             range(1, 3)}
        grass_images: dict = {f'grass_{i}': pg.image.load(f'./grass_images/grass{i}.png').convert_alpha() for i in
                              range(1, 6)}
        rock_images: dict = {f'rock_{i}': pg.image.load(f'./rock_images/rock{i}.png').convert_alpha() for i in
                             range(1, 14)}
        house_images: dict = {f'house_{i}': pg.image.load(f'./house_images/house{i}.png').convert_alpha() for i in
                              range(1, 8)}
        door_images: dict = {f'door_{i}': pg.image.load(f'./cave_and_door_images/door{i}.png').convert_alpha() for i in
                             range(1, 5)}
        cave_ground_images: dict = {
            f'cave_ground_{i}': pg.image.load(f'./cave_ground_images/cave_ground{i}.png').convert_alpha() for i in
            range(1, 16)}
        return cave_images, grass_images, door_images, rock_images, house_images, cave_ground_images

    @classmethod
    def change_all_images_into_directory(cls, cave_images: dict, door_images: dict, rock_images: dict,
                                         grass_images: dict, house_images: dict, cave_ground_images: dict) -> dict:
        """
        the method is responsible for turning multiple image dictionaries into one for easier management
        :param cave_images:
        :param door_images:
        :param rock_images:
        :param grass_images:
        :param house_images:
        :param cave_ground_images:
        :return: image_mapping
        """
        # cave <2, 3>, grass <4, 8>, rock <9, 20>, house <21, 27>, door <28, 31>, cave_ground <32, 46>
        image_mapping: dict = {
            1: rock_images['rock_1'],
            **{i + 2: cave_images[f'cave_{i + 1}'] for i in range(2)},
            **{i + 4: grass_images[f'grass_{i + 1}'] for i in range(5)},
            **{i + 9: rock_images[f'rock_{i + 2}'] for i in range(12)},
            **{i + 21: house_images[f'house_{i + 1}'] for i in range(7)},
            **{i + 28: door_images[f'door_{i + 1}'] for i in range(4)},
            **{i + 32: cave_ground_images[f'cave_ground_{i + 1}'] for i in range(15)}
        }
        return image_mapping

    @classmethod
    def calculate_shift(cls, game_map_width: int, game_map_height: int) -> tuple[int, int]:
        """
        the method is responsible for centering the map when creating a smaller version
        :param game_map_width:
        :param game_map_height:
        :return: center_map_by_width, center_map_by_height
        """
        if game_map_width * Settings.SQUARE_SIZE < Settings.SCREEN_WIDTH:
            center_map_by_width = int((Settings.SCREEN_WIDTH - (game_map_width * Settings.SQUARE_SIZE)) / 2 - 300)
        else:
            center_map_by_width = 0

        if game_map_height * Settings.SQUARE_SIZE < Settings.SCREEN_HEIGHT:
            center_map_by_height = int((Settings.SCREEN_HEIGHT - (game_map_height * Settings.SQUARE_SIZE)) / 2 - 90)
        else:
            center_map_by_height = 0

        return center_map_by_width, center_map_by_height

    @staticmethod
    def draw_map(game_map, game_map_width: int, game_map_height: int, screen_width: int,
                 screen_height: int, width_shift: int = 0, height_shift: int = 0) -> pg.Surface:
        """
        the method is responsible for changing many fragments of graphics into one game background
        :param game_map:
        :param game_map_width:
        :param game_map_height:
        :param screen_width:
        :param screen_height:
        :param width_shift:
        :param height_shift:
        :return: background_surface
        """
        start = time()
        center_map_by_width, center_map_by_height = DrawMap.calculate_shift(game_map_width, game_map_height)
        cave_images, grass_images, door_images, rock_images, house_images, cave_ground_images = DrawMap.read_images()
        images = DrawMap.change_all_images_into_directory(cave_images, door_images, rock_images, grass_images,
                                                          house_images, cave_ground_images)
        background_surface = pg.Surface((screen_width, screen_height))

        column_shift = -30 + center_map_by_height + height_shift

        for row in range(game_map_height):
            row_shift = center_map_by_width + width_shift
            column_shift += 30

            for column in range(game_map_width):
                number = game_map[row][column]
                background_surface.blit(images[number], (row_shift, column_shift))
                row_shift += 30

        end = time()
        print(f'Time required to draw a map: {round((end - start) * 1000, 2)} ms')
        return background_surface
