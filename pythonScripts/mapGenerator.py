import random
from time import time
import numpy as np
import ctypes


class MapGenerator:

    @classmethod
    def create_obstacle(cls, game_map: np.array, min_size_of_obstacle: int = 5, max_size_of_obstacle: int = 10,
                        number_of_obstacles: int = 0) -> None:
        """
        the method is responsible for creating obstacles on the map in a completely random way
        :param game_map:
        :param min_size_of_obstacle:
        :param max_size_of_obstacle:
        :param number_of_obstacles:
        :return: None (the operation modifies the game_map in-place)
        """

        if min_size_of_obstacle > max_size_of_obstacle:
            raise Exception('*** Maximum size should be greater than minimum size or equal ***')
        if not (5 <= min_size_of_obstacle <= 40):
            raise Exception('*** Minimum size of obstacle should be between <5, 40> ***')
        if not (5 <= max_size_of_obstacle <= 50):
            raise Exception('*** Maximum size of obstacle should be between <5, 50> ***')
        if not (0 <= number_of_obstacles <= 15):
            raise Exception('*** Number of obstacles should be between <0, 15>')

        for _ in range(number_of_obstacles):
            # chooses a random place where the obstacle appears
            start_x: int = random.randint(1, len(game_map[0]) - 2)
            start_y: int = random.randint(1, len(game_map) - 2)
            obstacle_size: int = random.randint(min_size_of_obstacle, max_size_of_obstacle)

            while obstacle_size > 0:
                # location of obstacle fragments
                if game_map[start_y][start_x] == 0 and 0 in game_map[start_y] and 0 in [x[start_x] for x in game_map]:
                    game_map[start_y][start_x] = 1
                    obstacle_size -= 1
                else:
                    change_direction = random.randint(1, 4)

                    match change_direction:
                        case 1:
                            if start_x - 1 >= 0:
                                start_x -= 1
                        case 2:
                            if start_x + 1 < len(game_map[0]):
                                start_x += 1
                        case 3:
                            if start_y - 1 >= 0:
                                start_y -= 1
                        case 4:
                            if start_y + 1 < len(game_map):
                                start_y += 1

    @classmethod
    def fill_holes_and_spaces_in_obstacle(cls, game_map: np.array, number_of_executions: int = 3) -> None:
        """
        the method is responsible for removing gaps between obstacles or terrain, it has been moved to C++
        :param game_map:
        :param number_of_executions:
        :return: None (the operation modifies the game_map in-place)
        """
        height_of_map: int = len(game_map)
        width_of_map: int = len(game_map[0])

        dll = ctypes.CDLL('./cppDLL/mapGeneratorCpp.dll')

        dll.fill_holes_and_spaces_in_obstacle.argtypes = [
            ctypes.POINTER(ctypes.POINTER(ctypes.c_int8)),
            ctypes.c_int,
            ctypes.c_int
        ]

        array_of_pointers = (ctypes.POINTER(ctypes.c_int8) * height_of_map)()

        for i in range(height_of_map):
            array_of_pointers[i] = ctypes.cast(game_map[i].ctypes.data, ctypes.POINTER(ctypes.c_int8))

        for _ in range(number_of_executions):
            dll.fill_holes_and_spaces_in_obstacle(array_of_pointers, width_of_map, height_of_map)

    @classmethod
    def fix_top_and_bottom_edge_of_game_map(cls, game_map: np.array) -> None:
        """
        the method is responsible for removing gaps between obstacles or terrain on the upper and lower edges of the map
        :param game_map:
        :return: None (the operation modifies the game_map in-place)
        """
        height_of_map: int = len(game_map)
        width_of_map: int = len(game_map[0])

        for i in range(1, width_of_map - 1):
            # inserting zeros at the top edge of map
            if game_map[0][i] != 0:
                if game_map[0][i - 1] == 0 and game_map[0][i + 1] == 0:
                    game_map[0][i] = 0

            # inserting zeros at the bottom edge of map
            if game_map[height_of_map - 1][i] != 0:
                if game_map[height_of_map - 1][i - 1] == 0 and game_map[height_of_map - 1][i + 1] == 0:
                    game_map[height_of_map - 1][i] = 0

            # inserting ones at the top edge of map
            if game_map[0][i] == 0:
                if game_map[0][i - 1] != 0 and game_map[0][i + 1] != 0:
                    game_map[0][i] = 1

            # inserting ones at the bottom edge of map
            if game_map[height_of_map - 1][i] == 0:
                if game_map[height_of_map - 1][i - 1] != 0 and game_map[height_of_map - 1][i + 1] != 0:
                    game_map[height_of_map - 1][i] = 1

    @classmethod
    def fix_top_left_and_right_edge_of_game_map(cls, game_map: np.array) -> None:
        """
        the method is responsible for removing gaps between obstacles or terrain on the left and right edges of the map
        :param game_map:
        :return: None (the operation modifies the game_map in-place)
        """
        height_of_map: int = len(game_map)
        width_of_map: int = len(game_map[0])

        for i in range(1, height_of_map - 1):
            # inserting zeros at the left edge of map
            if game_map[i][0] != 0:
                if game_map[i - 1][0] == 0 and game_map[i + 1][0] == 0:
                    game_map[i][0] = 0

            # inserting zeros at the right edge of map
            if game_map[i][width_of_map - 1] != 0:
                if game_map[i - 1][width_of_map - 1] == 0 and game_map[i + 1][width_of_map - 1] == 0:
                    game_map[i][width_of_map - 1] = 0

            # inserting ones at the left edge of map
            if game_map[i][0] == 0:
                if game_map[i - 1][0] != 0 and game_map[i + 1][0] != 0:
                    game_map[i][0] = 1

            # inserting ones at the right edge of map
            if game_map[i][width_of_map - 1] == 0:
                if game_map[i - 1][width_of_map - 1] != 0 and game_map[i + 1][width_of_map - 1] != 0:
                    game_map[i][width_of_map - 1] = 1

    @classmethod
    def delete_narrow_obstacles(cls, game_map: np.array, number_of_executions: int = 3) -> None:
        """
        the method is responsible for removing obstacles whose thickness is one
        :param game_map:
        :param number_of_executions:
        :return: None (the operation modifies the game_map in-place)
        """
        height_of_map: int = len(game_map)
        width_of_map: int = len(game_map[0])

        for _ in range(number_of_executions):
            for x in range(1, height_of_map - 1):
                for y in range(1, width_of_map - 1):
                    if game_map[x][y] == 1:
                        number_of_neighbours = 0

                        if game_map[x - 1][y] == 1:
                            number_of_neighbours += 1
                        if game_map[x + 1][y] == 1:
                            number_of_neighbours += 1
                        if game_map[x][y - 1] == 1:
                            number_of_neighbours += 1
                        if game_map[x][y + 1] == 1:
                            number_of_neighbours += 1
                        if number_of_neighbours <= 1:
                            game_map[x][y] = 0

    @classmethod
    def insert_doors_into_game_map(cls, game_map: np.array, number_of_doors: int, top_e: bool, right_e: bool,
                                   bottom_e: bool, left_e: bool, door_width: int = 5) -> int:
        """
        the method is responsible for creating doors on selected or all edges of the map
        :param game_map:
        :param number_of_doors:
        :param top_e:
        :param right_e:
        :param bottom_e:
        :param left_e:
        :param door_width:
        :return: created_doors
        """

        if number_of_doors > 4 or number_of_doors < 1:
            raise Exception('*** Nuber of doors should be between <2, 4> ***')
        if len(game_map) < 25:
            raise Exception('*** Y coord of game map should be greater than 20 ***')
        if len(game_map[0]) < 25:
            raise Exception('*** X coord of game map should be greater than 20 ***')
        if not (3 <= door_width <= 10):
            raise Exception('*** Door width should be between <3, 10> ***')

        used_edges: set = set()
        test_number: int = 0

        for edge, number in ((top_e, 1), (bottom_e, 2), (left_e, 3), (right_e, 4)):
            if edge:
                test_number += 1
            else:
                used_edges.add(number)

        if test_number != number_of_doors:
            raise Exception('*** Number of doors should correspond to the number of selected edges ***')

        created_doors: int = 0
        max_attempts: int = 50
        success: bool = False
        door_obstacle_dist_w: int = 20
        door_obstacle_dist_h: int = 15

        while created_doors != number_of_doors:
            while True:
                door_edge: int = random.randint(1, 4)

                if door_edge in used_edges:
                    continue
                else:
                    used_edges.add(door_edge)
                    break

            door_shift: int = random.randint(5, 10)

            match door_edge:
                # top edge
                case 1:
                    m_len: int = len(game_map)

                    for i in range(m_len // door_shift + m_len // 3, m_len - door_width):
                        if 1 not in game_map[0][i:i + door_width] and 1 not in game_map[1][i:i + door_width]:
                            if game_map[0][i - 1] == 0 and game_map[0][i + door_width] == 0:
                                if game_map[1][i - 1] == 0 and game_map[1][i + door_width] == 0:
                                    if 1 not in game_map[0:door_obstacle_dist_h, i + door_width // 2]:
                                        for x in range(door_width):
                                            game_map[0][i + x] = random.randint(28, 29)

                                        created_doors += 1
                                        success = True
                                        break

                # bottom edge
                case 2:
                    m_len: int = len(game_map)

                    for i in range(m_len // door_shift + m_len // 3, m_len - door_width):
                        if 1 not in game_map[m_len - 1][i:i + door_width]:
                            if 1 not in game_map[m_len - 2][i:i + door_width]:
                                if game_map[m_len - 1][i - 1] == 0 and game_map[m_len - 1][i + door_width] == 0:
                                    if game_map[m_len - 2][i - 1] == 0 and game_map[m_len - 2][i + door_width] == 0:
                                        if 1 not in game_map[-door_obstacle_dist_h:, i + door_width // 2]:
                                            for x in range(door_width):
                                                game_map[m_len - 1][i + x] = random.randint(28, 29)

                                            created_doors += 1
                                            success = True
                                            break

                # left edge
                case 3:
                    m_len: int = len(game_map)

                    for i in range(m_len // door_shift, m_len - door_width):
                        if 1 not in game_map[i:i + door_width, 0] and 1 not in game_map[i:i + door_width, 1]:
                            if game_map[i - 1][0] == 0 and game_map[i + door_width][0] == 0:
                                if game_map[i - 1][1] == 0 and game_map[i + door_width][1] == 0:
                                    if 1 not in game_map[i + door_width // 2, 0:door_obstacle_dist_w]:
                                        for x in range(door_width):
                                            game_map[i + x][0] = random.randint(28, 29)

                                        created_doors += 1
                                        success = True
                                        break

                # right edge
                case 4:
                    m_len: int = len(game_map[0])

                    for i in range(m_len // door_shift, len(game_map) - door_width):
                        if 1 not in game_map[i:i + door_width, m_len - 1]:
                            if 1 not in game_map[i:i + door_width, m_len - 2]:
                                if game_map[i - 1][m_len - 1] == 0 and game_map[i + door_width - 1][m_len - 1] == 0:
                                    if game_map[i - 1][m_len - 2] == 0 and game_map[i + door_width][m_len - 2] == 0:
                                        if 1 not in game_map[i + door_width // 2, -door_obstacle_dist_w:]:
                                            for x in range(door_width):
                                                game_map[i + x][m_len - 1] = random.randint(28, 29)

                                            created_doors += 1
                                            success = True
                                            break

            if not success:
                used_edges.remove(door_edge)
            success = False

            max_attempts -= 1
            if max_attempts < 0:
                if door_width == 5:
                    max_attempts = 50
                    door_width = 3
                    door_obstacle_dist_w -= 5
                    door_obstacle_dist_h -= 5
                else:
                    break

        return created_doors

    @classmethod
    def fill_holes_in_obstacle(cls, game_map: np.array, number_of_executions: int = 1) -> None:
        """
        the method is responsible for patching holes in obstacles with dimensions one by one,
        the method has been moved to C++
        :param game_map:
        :param number_of_executions:
        :return: None (the operation modifies the game_map in-place)
        """
        if not (1 <= number_of_executions <= 10):
            raise Exception('*** Number of executions should be between <1, 10> ***')

        height_of_map: int = len(game_map)
        width_of_map: int = len(game_map[0])

        # fill corners
        # left top corner
        if game_map[0][1] == 1 and game_map[1][0] == 1:
            game_map[0][0] = 1
        # right top corner
        if game_map[0][width_of_map - 2] == 1 and game_map[1][width_of_map - 1] == 1:
            game_map[0][width_of_map - 1] = 1
        # left bottom corner
        if game_map[height_of_map - 2][0] == 1 and game_map[height_of_map - 1][1] == 1:
            game_map[height_of_map - 1][0] = 1
        # right bottom corner
        if game_map[height_of_map - 1][len(game_map[height_of_map - 1]) - 2] == 1:
            if game_map[height_of_map - 2][len(game_map[height_of_map - 1]) - 1] == 1:
                game_map[height_of_map - 1][len(game_map[height_of_map - 1]) - 1] = 1

        dll = ctypes.CDLL('./cppDLL/mapGeneratorCpp.dll')

        dll.fill_holes_in_obstacle.argtypes = [
            ctypes.POINTER(ctypes.POINTER(ctypes.c_int8)),
            ctypes.c_int,
            ctypes.c_int
        ]

        array_of_pointers = (ctypes.POINTER(ctypes.c_int8) * height_of_map)()

        for i in range(height_of_map):
            array_of_pointers[i] = ctypes.cast(game_map[i].ctypes.data, ctypes.POINTER(ctypes.c_int8))

        # fill holes in obstacles
        for _ in range(number_of_executions):
            dll.fill_holes_in_obstacle(array_of_pointers, width_of_map, height_of_map)

    @classmethod
    def fill_squares_two_by_two_in_obstacles(cls, game_map: np.array, number_of_executions: int = 3) -> None:
        """
        the method is responsible for patching holes in obstacles with dimensions two by two,
        the method has been moved to C++
        :param game_map:
        :param number_of_executions:
        :return: None (the operation modifies the game_map in-place)
        """
        height_of_map: int = len(game_map)
        width_of_map: int = len(game_map[0])
        square: bool = False
        number_of_neighbors: int = 0

        dll = ctypes.CDLL('./cppDLL/mapGeneratorCpp.dll')

        dll.fill_squares_two_by_two_in_obstacles.argtypes = [
            ctypes.POINTER(ctypes.POINTER(ctypes.c_int8)),
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_bool,
            ctypes.c_int
        ]

        array_of_pointers = (ctypes.POINTER(ctypes.c_int8) * height_of_map)()

        for i in range(height_of_map):
            array_of_pointers[i] = ctypes.cast(game_map[i].ctypes.data, ctypes.POINTER(ctypes.c_int8))

        for _ in range(number_of_executions):
            dll.fill_squares_two_by_two_in_obstacles(array_of_pointers, width_of_map, height_of_map, square,
                                                     number_of_neighbors)

    @classmethod
    def fill_squares_three_by_three_in_obstacles(cls, game_map: np.array, number_of_executions: int = 1) -> None:
        """
        the method is responsible for patching holes in obstacles with dimensions three by three,
        the method has been moved to C++
        :param game_map:
        :param number_of_executions:
        :return: None (the operation modifies the game_map in-place)
        """
        height_of_map: int = len(game_map)
        width_of_map: int = len(game_map[0])
        square: bool = False
        number_of_neighbours: int = 0

        dll = ctypes.CDLL('./cppDLL/mapGeneratorCpp.dll')

        dll.fill_squares_three_by_three_in_obstacles.argtypes = [
            ctypes.POINTER(ctypes.POINTER(ctypes.c_int8)),
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_bool,
            ctypes.c_int
        ]

        array_of_pointers = (ctypes.POINTER(ctypes.c_int8) * height_of_map)()

        for i in range(height_of_map):
            array_of_pointers[i] = ctypes.cast(game_map[i].ctypes.data, ctypes.POINTER(ctypes.c_int8))

        for _ in range(number_of_executions):
            dll.fill_squares_three_by_three_in_obstacles(array_of_pointers, width_of_map, height_of_map, square,
                                                         number_of_neighbours)

    @classmethod
    def fill_rectangles_two_by_three_in_obstacles(cls, game_map: np.array, number_of_executions: int = 1) -> None:
        """
        the method is responsible for patching holes in obstacles with dimensions two by three,
        the method has been moved to C++
        :param game_map:
        :param number_of_executions:
        :return: None (the operation modifies the game_map in-place)
        """
        height_of_map: int = len(game_map)
        width_of_map: int = len(game_map[0])
        rectangle: bool = False
        number_of_neighbours: int = 0

        dll = ctypes.CDLL('./cppDLL/mapGeneratorCpp.dll')

        dll.fill_rectangles_two_by_three_in_obstacles.argtypes = [
            ctypes.POINTER(ctypes.POINTER(ctypes.c_int8)),
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_bool,
            ctypes.c_int
        ]

        array_of_pointers = (ctypes.POINTER(ctypes.c_int8) * height_of_map)()

        for i in range(height_of_map):
            array_of_pointers[i] = ctypes.cast(game_map[i].ctypes.data, ctypes.POINTER(ctypes.c_int8))

        for _ in range(number_of_executions):
            dll.fill_rectangles_two_by_three_in_obstacles(array_of_pointers, width_of_map, height_of_map, rectangle,
                                                          number_of_neighbours)

    @classmethod
    def fill_rectangles_three_by_two_in_obstacles(cls, game_map: np.array, number_of_executions: int = 1) -> None:
        """
        the method is responsible for patching holes in obstacles with dimensions three by two,
        the method has been moved to C++
        :param game_map:
        :param number_of_executions:
        :return: None (the operation modifies the game_map in-place)
        """
        height_of_map: int = len(game_map)
        width_of_map: int = len(game_map[0])
        rectangle: bool = False
        number_of_neighbours: int = 0

        dll = ctypes.CDLL('./cppDLL/mapGeneratorCpp.dll')

        dll.fill_rectangles_three_by_two_in_obstacles.argtypes = [
            ctypes.POINTER(ctypes.POINTER(ctypes.c_int8)),
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_bool,
            ctypes.c_int
        ]

        array_of_pointers = (ctypes.POINTER(ctypes.c_int8) * height_of_map)()

        for i in range(height_of_map):
            array_of_pointers[i] = ctypes.cast(game_map[i].ctypes.data, ctypes.POINTER(ctypes.c_int8))

        for _ in range(number_of_executions):
            dll.fill_rectangles_three_by_two_in_obstacles(array_of_pointers, width_of_map, height_of_map, rectangle,
                                                          number_of_neighbours)

    @classmethod
    def fill_edges_of_map(cls, game_map: np.array) -> None:
        """
        the method is responsible for filling holes in obstacles on the edges of the map
        :param game_map:
        :return: None (the operation modifies the game_map in-place)
        """
        height_of_map: int = len(game_map)
        width_of_map: int = len(game_map[0])

        # fill top and bottom edge
        for i in range(width_of_map):
            if game_map[0][i] == 0 and game_map[1][i] == 1:
                game_map[0][i] = 1
            if game_map[height_of_map - 1][i] == 0 and game_map[height_of_map - 2][i] == 1:
                game_map[height_of_map - 1][i] = 1

        # fill left and right edge
        for i in range(height_of_map):
            if game_map[i][0] == 0 and game_map[i][1] == 1:
                game_map[i][0] = 1
            if game_map[i][width_of_map - 1] == 0 and game_map[i][width_of_map - 2] == 1:
                game_map[i][width_of_map - 1] = 1

    @classmethod
    def fill_wide_holes_on_edges_of_map(cls, game_map: np.array) -> None:
        """
        the method is responsible for filling wide holes in obstacles on the edges of the map
        :param game_map:
        :return: None (the operation modifies the game_map in-place)
        """
        height_of_map: int = len(game_map)
        width_of_map: int = len(game_map[0])

        for i in range(width_of_map):
            # top edge of map
            if game_map[0][i] == 0 and game_map[3][i] == 1:
                for x in range(3):
                    game_map[x][i] = 1

            # bottom edge of map
            if game_map[height_of_map - 1][i] == 0 and game_map[height_of_map - 4][i] == 1:
                for x in range(1, 4):
                    game_map[height_of_map - x][i] = 1

        for i in range(height_of_map):
            # left edge of map
            if game_map[i][0] == 0 and game_map[i][3] == 1:
                for x in range(3):
                    game_map[i][x] = 1

            # right edge of map
            if game_map[i][width_of_map - 1] == 0 and game_map[i][width_of_map - 4]:
                for x in range(1, 4):
                    game_map[i][width_of_map - x] = 1

    @classmethod
    def delete_narrow_connections_between_obstacles(cls, game_map: np.array, number_of_executions: int = 3) -> None:
        """
        the method is responsible for removing connections between obstacles with a thickness of one by one
        :param game_map:
        :param number_of_executions:
        :return: (the operation modifies the game_map in-place)
        """
        height_of_map: int = len(game_map)
        width_of_map: int = len(game_map[0])

        for _ in range(number_of_executions):
            for y in range(1, height_of_map - 1):
                for x in range(1, width_of_map - 1):
                    if game_map[y][x] == 1:
                        # delete horizontal connections
                        if game_map[y][x - 1] == 1 and game_map[y][x + 1] == 1:
                            if game_map[y - 1][x] == 0 and game_map[y + 1][x] == 0:
                                game_map[y][x] = 0

                        # delete vertical connections
                        if game_map[y - 1][x] == 1 and game_map[y + 1][x] == 1:
                            if game_map[y][x - 1] == 0 and game_map[y][x + 1] == 0:
                                game_map[y][x] = 0

    @classmethod
    def create_building(cls, game_map: np.array) -> bool:
        """
        the method is responsible for finding a place for the house and creating it;
        if it is not created, it returns false
        :param game_map:
        :return: True or False
        """
        height_of_map: int = len(game_map)
        width_of_map: int = len(game_map[0])

        for y in range(14, height_of_map - 14):
            for x in range(14, width_of_map - 14):
                # find place to create building
                if 1 not in game_map[y, x:x + 10] and 1 not in game_map[y + 10, x:x + 10]:
                    if 1 not in game_map[y:y + 10, x] and 1 not in game_map[y:y + 10, x + 10]:
                        # draw floor
                        for dy in range(y + 2, y + 9):
                            for dx in range(x + 2, x + 9):
                                game_map[dy][dx] = 27

                        # draw left and right wall
                        for dy in range(y + 2, y + 9):
                            game_map[dy][x + 1] = 22
                            game_map[dy][x + 9] = 22

                        # draw top and bottom wall
                        for dx in range(x + 2, x + 9):
                            game_map[y + 1][dx] = 21
                            game_map[y + 9][dx] = 21

                        # draw corners
                        game_map[y + 1][x + 1] = 23
                        game_map[y + 1][x + 9] = 24
                        game_map[y + 9][x + 1] = 25
                        game_map[y + 9][x + 9] = 26

                        # draw door
                        match random.randint(1, 4):
                            # top edge
                            case 1:
                                for i in range(4, 7):
                                    game_map[y + 1][x + i] = 27
                            # bottom edge
                            case 2:
                                for i in range(4, 7):
                                    game_map[y + 9][x + i] = 27
                            # left edge
                            case 3:
                                for i in range(4, 7):
                                    game_map[y + i][x + 1] = 27
                            # right edge
                            case 4:
                                for i in range(4, 7):
                                    game_map[y + i][x + 9] = 27

                        return True
        return False

    @classmethod
    def change_grass_graphics(cls, game_map: np.array) -> None:
        """
        method replaces the zeros representing the basic grass graphic with other numbers
        that allow you to select other graphics to draw
        :param game_map:
        :return: None (the operation modifies the game_map in-place)
        """
        for y in range(len(game_map)):
            for x in range(len(game_map[0])):
                if game_map[y][x] == 0:
                    if random.randint(0, 100) > 60:
                        game_map[y][x] = random.randint(5, 8)
                    else:
                        game_map[y][x] = 4

    @classmethod
    def change_stone_graphics(cls, game_map: np.array) -> None:
        """
        the method replaces the edges of obstacles with other numbers to make the game map look better
        :param game_map:
        :return: None (the operation modifies the game_map in-place)
        """
        width_of_map: int = len(game_map[0])
        height_of_map: int = len(game_map)

        for y in range(1, height_of_map - 1):
            for x in range(1, width_of_map - 1):
                if game_map[y][x] == 1:
                    # check two connections
                    if game_map[y][x - 1] == 0 and game_map[y - 1][x] == 0:
                        game_map[y][x] = 13
                    elif game_map[y][x + 1] == 0 and game_map[y - 1][x] == 0:
                        game_map[y][x] = 14
                    elif game_map[y][x + 1] == 0 and game_map[y + 1][x] == 0:
                        game_map[y][x] = 15
                    elif game_map[y][x - 1] == 0 and game_map[y + 1][x] == 0:
                        game_map[y][x] = 16

                    # check one connection
                    elif game_map[y][x - 1] == 0:
                        game_map[y][x] = 9
                    elif game_map[y - 1][x] == 0:
                        game_map[y][x] = 10
                    elif game_map[y][x + 1] == 0:
                        game_map[y][x] = 11
                    elif game_map[y + 1][x] == 0:
                        game_map[y][x] = 12

                    # check corners
                    elif game_map[y - 1][x + 1] == 0:
                        game_map[y][x] = 17
                    elif game_map[y - 1][x - 1] == 0:
                        game_map[y][x] = 18
                    elif game_map[y + 1][x - 1] == 0:
                        game_map[y][x] = 19
                    elif game_map[y + 1][x + 1] == 0:
                        game_map[y][x] = 20
                    else:
                        continue

        # top edge of map
        for i in range(1, width_of_map - 1):
            if game_map[0][i] == 1:
                if game_map[0][i - 1] == 0 and game_map[1][i] == 0:
                    game_map[0][i] = 16
                elif game_map[0][i + 1] == 0 and game_map[1][i] == 0:
                    game_map[0][i] = 15
                elif game_map[0][i - 1] == 0:
                    game_map[0][i] = 9
                elif game_map[0][i + 1] == 0:
                    game_map[0][i] = 11
                elif game_map[1][i - 1] == 0:
                    game_map[0][i] = 19
                elif game_map[1][i + 1] == 0:
                    game_map[0][i] = 20
                else:
                    continue

        # bottom edge of map
        for i in range(1, width_of_map - 1):
            if game_map[height_of_map - 1][i] == 1:
                if game_map[height_of_map - 1][i - 1] == 0 and game_map[height_of_map - 2][i] == 0:
                    game_map[height_of_map - 1][i] = 13
                elif game_map[height_of_map - 1][i + 1] == 0 and game_map[height_of_map - 2][i] == 0:
                    game_map[height_of_map - 1][i] = 14
                elif game_map[height_of_map - 1][i - 1] == 0:
                    game_map[height_of_map - 1][i] = 9
                elif game_map[height_of_map - 1][i + 1] == 0:
                    game_map[height_of_map - 1][i] = 11
                elif game_map[height_of_map - 2][i + 1] == 0:
                    game_map[height_of_map - 1][i] = 17
                elif game_map[height_of_map - 2][i - 1] == 0:
                    game_map[height_of_map - 1][i] = 18
                else:
                    continue

        # left edge of map
        for i in range(1, height_of_map - 1):
            if game_map[i][0] == 1:
                if game_map[i - 1][0] == 0 and game_map[i][1] == 0:
                    game_map[i][0] = 14
                elif game_map[i + 1][0] == 0 and game_map[i][1] == 0:
                    game_map[i][0] = 15
                elif game_map[i - 1][0] == 0:
                    game_map[i][0] = 10
                elif game_map[i + 1][0] == 0:
                    game_map[i][0] = 12
                elif game_map[i - 1][1] == 0:
                    game_map[i][0] = 17
                elif game_map[i + 1][1] == 0:
                    game_map[i][0] = 20
                else:
                    continue

        # right edge of map
        for i in range(1, height_of_map - 1):
            if game_map[i][width_of_map - 1] == 1:
                if game_map[i - 1][width_of_map - 1] == 0 and game_map[i][width_of_map - 2] == 0:
                    game_map[i][width_of_map - 1] = 13
                elif game_map[i + 1][width_of_map - 1] == 0 and game_map[i][width_of_map - 2] == 0:
                    game_map[i][width_of_map - 1] = 16
                elif game_map[i - 1][width_of_map - 1] == 0:
                    game_map[i][width_of_map - 1] = 10
                elif game_map[i + 1][width_of_map - 1] == 0:
                    game_map[i][width_of_map - 1] = 12
                elif game_map[i - 1][width_of_map - 2] == 0:
                    game_map[i][width_of_map - 1] = 18
                elif game_map[i + 1][width_of_map - 2] == 0:
                    game_map[i][width_of_map - 1] = 19
                else:
                    continue

    @classmethod
    def create_cave_entrance(cls, game_map: np.array) -> None:
        """
        the method is used to create an entrance to a cave that is located on the edge of an obstacle
        :param game_map:
        :return: None (the operation modifies the game_map in-place)
        """
        width_of_map: int = len(game_map[0])
        height_of_map: int = len(game_map)

        for y in range(1, height_of_map - 1):
            for x in range(1, width_of_map - 2):
                if game_map[y][x] == 12 and game_map[y][x + 1] == 12:
                    if game_map[y - 1][x] == 1 and game_map[y - 1][x + 1] == 1:
                        game_map[y][x] = 2
                        game_map[y][x + 1] = 3
                        game_map[y + 1][x] = 29
                        game_map[y + 1][x + 1] = 28
                        return None

    @classmethod
    def change_grass_into_cave_ground(cls, game_map: np.array) -> None:
        """
        the method is responsible for replacing the numbers responsible for
        drawing grass with those drawing the floor in the cave
        :param game_map:
        :return: None (the operation modifies the game_map in-place)
        """
        width_of_map: int = len(game_map[0])
        height_of_map: int = len(game_map)

        for row in range(height_of_map):
            for column in range(width_of_map):
                if game_map[row][column] in [*range(4, 9)]:
                    if random.randint(0, 4) <= 2:
                        game_map[row][column] = 34
                    else:
                        if random.randint(1, 2) == 1:
                            game_map[row][column] = 32
                        else:
                            game_map[row][column] = 33

    @classmethod
    def change_door_into_cave_door(cls, game_map: np.array) -> None:
        """
        the method is responsible for replacing the numbers responsible for
        drawing the basic door with those in the cave version
        :param game_map:
        :return: None (the operation modifies the game_map in-place)
        """
        width_of_map: int = len(game_map[0])
        height_of_map: int = len(game_map)

        for column in range(width_of_map):
            if game_map[height_of_map - 1][column] in (range(28, 30)):
                game_map[height_of_map - 1][column] = random.randint(30, 31)

    @classmethod
    def change_stone_into_cave_stone(cls, game_map: np.array) -> None:
        """
        the method is responsible for replacing the edges of obstacles with those suitable for the cave
        :param game_map:
        :return: None (the operation modifies the game_map in-place)
        """
        width_of_map: int = len(game_map[0])
        height_of_map: int = len(game_map)

        for row in range(height_of_map):
            for column in range(width_of_map):
                if game_map[row][column] in (range(9, 21)):
                    game_map[row][column] += 26

    @staticmethod
    def generate_map(
            map_height: int = 30, map_width: int = 44, house: bool = False, cave: bool = False, num_doors: int = 2,
            top_e: bool = False, right_e: bool = True, bottom_e: bool = False, left_e: bool = True,
            min_size_of_obstacle: int = 40, max_size_of_obstacle: int = 50, number_of_obstacles: int = 9,
            cave_mode: bool = False, small_map: bool = False) \
            -> tuple[np.array, np.array, bool, bool]:
        """
        the method is responsible for creating the game map array using helper methods,
        which is necessary to draw the background graphics
        :param map_height:
        :param map_width:
        :param house:
        :param cave:
        :param num_doors:
        :param top_e:
        :param right_e:
        :param bottom_e:
        :param left_e:
        :param min_size_of_obstacle:
        :param max_size_of_obstacle:
        :param number_of_obstacles:
        :param cave_mode:
        :param small_map:
        :return: game_map, raw_game_map, cave_mode, small_map
        """
        if cave_mode:
            if num_doors != 1:
                raise Exception('*** Number of doors in cave mode should be equal one ***')
            if map_height != 30:
                raise Exception('*** Map height in cave mode should be equal 30 ***')
            if map_width != 44:
                raise Exception('*** Map width in cave mode should be equal 44 ***')
            if house:
                raise Exception('*** There should be no house in cave mode ***')
            if not bottom_e:
                raise Exception('*** In cave mode door should be at bottom edge of map ***')

        start_time = time()
        number_of_doors: int = 0
        house_creation: bool = False

        game_map: np.array = np.zeros(1)

        while True:
            if num_doors != number_of_doors:
                game_map = np.zeros((map_height, map_width), dtype=np.int8)
            else:
                break

            MapGenerator.create_obstacle(game_map, min_size_of_obstacle, max_size_of_obstacle, number_of_obstacles)
            MapGenerator.fill_wide_holes_on_edges_of_map(game_map)

            for _ in range(3):
                MapGenerator.fill_holes_and_spaces_in_obstacle(game_map, 5)
                MapGenerator.fill_holes_in_obstacle(game_map, 4)
                MapGenerator.fill_rectangles_two_by_three_in_obstacles(game_map, 1)
                MapGenerator.fill_rectangles_three_by_two_in_obstacles(game_map, 1)
                MapGenerator.fill_squares_three_by_three_in_obstacles(game_map, 2)
                MapGenerator.fill_squares_two_by_two_in_obstacles(game_map, 1)

            MapGenerator.fill_wide_holes_on_edges_of_map(game_map)
            MapGenerator.delete_narrow_connections_between_obstacles(game_map, 2)
            MapGenerator.delete_narrow_obstacles(game_map, 6)
            MapGenerator.fix_top_and_bottom_edge_of_game_map(game_map)
            MapGenerator.fix_top_left_and_right_edge_of_game_map(game_map)
            MapGenerator.fill_edges_of_map(game_map)
            number_of_doors = MapGenerator.insert_doors_into_game_map(
                game_map, num_doors, top_e, right_e, bottom_e, left_e, 5)

            if house:
                house_creation = MapGenerator.create_building(game_map)

            if house and not house_creation:
                number_of_doors = 0

        raw_game_map: np.array = game_map.copy()

        MapGenerator.change_stone_graphics(game_map)
        MapGenerator.change_grass_graphics(game_map)

        if cave:
            MapGenerator.create_cave_entrance(game_map)

        end_time = time()

        print(f'Time required to create a map: {round((end_time - start_time) * 1000, 2)} ms')

        return game_map, raw_game_map, cave_mode, small_map
