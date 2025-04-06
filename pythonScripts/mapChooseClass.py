from pythonScripts.mapGenerator import *


class MapChoose:
    @classmethod
    def _choose_door_place(cls, required_door_edge: int) -> tuple[list[bool], int]:
        """
        the method is responsible for randomly selecting the number of doors and their location on the map
        :return: doors_edge, number_of_doors
        """
        number_of_doors: int = random.randint(2, 4)
        doors_edge: list[bool] = [True] * number_of_doors

        while len(doors_edge) != 4:
            doors_edge.append(False)

        random.shuffle(doors_edge)

        # creates a door where play appears after passing through another door
        if required_door_edge != 0 and required_door_edge != 5:
            if required_door_edge == 1:
                doors_edge[3] = True
            elif required_door_edge == 2:
                doors_edge[1] = True
            elif required_door_edge == 3:
                doors_edge[0] = True
            else:
                doors_edge[2] = True

        number_of_doors = 0
        for door in doors_edge:
            if door:
                number_of_doors += 1

        return doors_edge, number_of_doors

    @classmethod
    def create_small_map(cls, cave: bool = False, required_door_edge: int = 0) -> (
            tuple)[tuple[np.array, np.array, bool, bool], int, int]:
        """
        method creates a small game map
        :param cave:
        :param required_door_edge:
        :return: game_map, 44, 30
        """
        doors: tuple[list[bool], int] = cls._choose_door_place(required_door_edge)

        game_map: tuple[np.array, np.array, bool, bool] = MapGenerator.generate_map(
            map_height=30,
            map_width=44,
            house=False, cave=cave,
            num_doors=doors[1],
            top_e=doors[0][0], right_e=doors[0][1], bottom_e=doors[0][2], left_e=doors[0][3],
            min_size_of_obstacle=random.randint(25, 35), max_size_of_obstacle=random.randint(35, 50),
            number_of_obstacles=5,
            cave_mode=False, small_map=True
        )
        return game_map, 44, 30

    @classmethod
    def create_small_map_with_house(cls, cave: bool = False, required_door_edge: int = 0) -> (
            tuple)[tuple[np.array, np.array, bool, bool], int, int]:
        """
        method creates a small game map with house
        :param cave:
        :param required_door_edge:
        :return: game_map, 44, 30
        """
        doors: tuple[list[bool], int] = cls._choose_door_place(required_door_edge)

        game_map: tuple[np.array, np.array, bool, bool] = MapGenerator.generate_map(
            map_height=30,
            map_width=44,
            house=True, cave=cave,
            num_doors=doors[1],
            top_e=doors[0][0], right_e=doors[0][1], bottom_e=doors[0][2], left_e=doors[0][3],
            min_size_of_obstacle=random.randint(15, 25), max_size_of_obstacle=random.randint(25, 35),
            number_of_obstacles=5,
            cave_mode=False, small_map=True
        )
        return game_map, 44, 30

    @classmethod
    def create_map(cls, cave: bool = False, required_door_edge: int = 0) -> (
            tuple)[tuple[np.array, np.array, bool, bool], int, int]:
        """
        method creates a basic version of the game map
        :param cave:
        :param required_door_edge:
        :return: game_map, 64, 36
        """
        doors: tuple[list[bool], int] = cls._choose_door_place(required_door_edge)

        game_map: tuple[np.array, np.array, bool, bool] = MapGenerator.generate_map(
            map_height=36,
            map_width=64,
            house=False, cave=cave,
            num_doors=doors[1],
            top_e=doors[0][0], right_e=doors[0][1], bottom_e=doors[0][2], left_e=doors[0][3],
            min_size_of_obstacle=random.randint(30, 40), max_size_of_obstacle=random.randint(40, 50),
            number_of_obstacles=9,
            cave_mode=False, small_map=False
        )
        return game_map, 64, 36

    @classmethod
    def create_map_with_house(cls, cave: bool = False, required_door_edge: int = 0) -> (
            tuple)[tuple[np.array, np.array, bool, bool], int, int]:
        """
        method creates a basic version of the game map with house
        :param cave:
        :param required_door_edge:
        :return: game_map, 64, 36
        """
        doors: tuple[list[bool], int] = cls._choose_door_place(required_door_edge)

        game_map: tuple[np.array, np.array, bool, bool] = MapGenerator.generate_map(
            map_height=36,
            map_width=64,
            house=True, cave=cave,
            num_doors=doors[1],
            top_e=doors[0][0], right_e=doors[0][1], bottom_e=doors[0][2], left_e=doors[0][3],
            min_size_of_obstacle=random.randint(30, 40), max_size_of_obstacle=random.randint(40, 50),
            number_of_obstacles=9,
            cave_mode=False, small_map=False
        )
        return game_map, 64, 36

    @classmethod
    def create_map_with_obstacles(cls, cave: bool = False) -> tuple[tuple[np.array, np.array, bool, bool], int, int]:
        """
        the method creates a basic version of the game map with an increased number of obstacles
        :param cave:
        :return: game_map, 64, 36
        """
        doors: tuple[list[bool], int] = ([True, True, True, True], 4)

        game_map: tuple[np.array, np.array, bool, bool] = MapGenerator.generate_map(
            map_height=36,
            map_width=64,
            house=False, cave=cave,
            num_doors=doors[1],
            top_e=doors[0][0], right_e=doors[0][1], bottom_e=doors[0][2], left_e=doors[0][3],
            min_size_of_obstacle=random.randint(35, 40), max_size_of_obstacle=random.randint(45, 50),
            number_of_obstacles=15,
            cave_mode=False, small_map=False
        )
        return game_map, 64, 36

    @classmethod
    def create_cave_map(cls) -> tuple[tuple[np.array, np.array, bool, bool], int, int]:
        """
        the method creates a map of the cave, which is a small map with changed graphics,
        one door and the mechanics of obscuring the surroundings
        :return: game_map, 44, 30
        """
        doors: tuple[list[bool], int] = ([False, False, True, False], 1)

        game_map: tuple[np.array, np.array, bool, bool] = MapGenerator.generate_map(
            map_height=30,
            map_width=44,
            house=False, cave=False,
            num_doors=doors[1],
            top_e=doors[0][0], right_e=doors[0][1], bottom_e=doors[0][2], left_e=doors[0][3],
            min_size_of_obstacle=random.randint(15, 25), max_size_of_obstacle=random.randint(25, 35),
            number_of_obstacles=5,
            cave_mode=True, small_map=True
        )

        MapGenerator.change_grass_into_cave_ground(game_map[0])
        MapGenerator.change_door_into_cave_door(game_map[0])
        MapGenerator.change_stone_into_cave_stone(game_map[0])

        return game_map, 44, 30
