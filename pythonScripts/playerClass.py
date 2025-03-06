import pygame as pg


class Player:
    x_move_screen: int = 0
    y_move_screen: int = 0
    x_move_collision: int = 0
    y_move_collision: int = 0
    previous_move: int = 1

    def __init__(self, x_cord: int, y_cord: int) -> None:
        self.x_cord: int = x_cord
        self.y_cord: int = y_cord
        self.image: pg.image = pg.image.load('./player_images/player.png').convert_alpha()
        self.width: int = self.image.get_width()
        self.height: int = self.image.get_height()
        self.battle_hit_box: pg.Rect = pg.Rect(self.x_cord, self.y_cord, self.width, self.height)
        self.movement_hit_box: pg.Rect = pg.Rect(self.x_cord, self.y_cord + 20, self.width, self.height - 20)
        self.speed: int = 5

    def move_player_to_next_square(self, collision_rects: list[pg.rect]) -> None:
        """
        the method is responsible for equalizing the player's position in relation to the square playing fields,
        which makes it easier to pass through tight gaps on the map
        :param collision_rects:
        :return: None (the method modifies the player's parameters)
        """
        if Player.previous_move == 1 and self.x_cord % 30 != 0:
            if self.x_cord % 30 + self.speed > 30:
                self.x_cord = (self.x_cord + self.x_cord % 30) - 30
            else:
                if not any(self.movement_hit_box.colliderect(i.move(self.speed, 0)) for i in collision_rects):
                    self.x_cord -= self.speed

        if Player.previous_move == 2 and self.x_cord % 30 != 0:
            if self.x_cord % 30 + self.speed > 30:
                self.x_cord = (self.x_cord - self.x_cord % 30) + 30
            else:
                if not any(self.movement_hit_box.colliderect(i.move(-self.speed, 0)) for i in collision_rects):
                    self.x_cord += self.speed

        if Player.previous_move == 3 and (self.y_cord + 20) % 30 != 0:
            if (self.y_cord + 20) % 30 + self.speed > 30:
                self.y_cord = ((self.y_cord + 20) + (self.y_cord - 20) % 30) - 30
            else:
                if self.y_cord > 90 and not any(
                        self.movement_hit_box.colliderect(i.move(0, self.speed)) for i in collision_rects):
                    self.y_cord -= self.speed

        if Player.previous_move == 4 and (self.y_cord + 20) % 30 != 0:
            if (self.y_cord + 20) % 30 + self.speed > 30:
                self.y_cord = ((self.y_cord + 20) - (self.y_cord + 20) % 30) + 30
            else:
                if not any(self.movement_hit_box.colliderect(i.move(0, -self.speed)) for i in collision_rects):
                    self.y_cord += self.speed

    def player_make_move(self, keys: pg.key, collision_rects: list[pg.rect], small_map: bool) \
            -> tuple[int, int, int, int]:
        """
        the method is responsible for moving the player, it also allows moving the game window
        and collisions occurring in it
        :param keys:
        :param collision_rects:
        :param small_map:
        :return: Player.x_move_screen, Player.y_move_screen, Player.x_move_collision, Player.y_move_collision
        """
        Player.x_move_collision, Player.y_move_collision = -Player.x_move_screen, -Player.y_move_screen

        if keys[pg.K_a]:
            if not small_map and self.x_cord - self.speed < 500 and Player.x_move_screen > 0:
                if not any(self.movement_hit_box.colliderect(i.move(self.speed, 0)) for i in collision_rects):
                    Player.x_move_screen -= self.speed
                    Player.x_move_collision += self.speed
            else:
                if self.x_cord - self.speed > 300:
                    if not any(self.movement_hit_box.colliderect(i.move(self.speed, 0)) for i in collision_rects):
                        self.x_cord -= self.speed
                else:
                    self.x_cord = 300

            Player.previous_move = 1

        if keys[pg.K_d]:
            if not small_map and self.x_cord + self.width + self.speed > 1420 and Player.x_move_screen < 600:
                if not any(
                        self.movement_hit_box.colliderect(i.move(-self.speed, 0)) for i in collision_rects):
                    Player.x_move_screen += self.speed
                    Player.x_move_collision -= self.speed
            else:
                if self.x_cord + self.speed < 1620 - self.width:
                    if not any(
                            self.movement_hit_box.colliderect(i.move(-self.speed, 0)) for i in collision_rects):
                        self.x_cord += self.speed
                else:
                    self.x_cord = 1620 - self.width

            Player.previous_move = 2

        if keys[pg.K_w]:
            if not small_map and self.y_cord - self.speed < 290 and Player.y_move_screen > 0:
                if not any(self.movement_hit_box.colliderect(i.move(0, self.speed)) for i in collision_rects):
                    Player.y_move_screen -= self.speed
                    Player.y_move_collision += self.speed
            else:
                if self.y_cord - self.speed > 90:
                    if not any(self.movement_hit_box.colliderect(i.move(0, self.speed)) for i in collision_rects):
                        self.y_cord -= self.speed
                else:
                    self.y_cord = 90

            Player.previous_move = 3

        if keys[pg.K_s]:
            if not small_map and self.y_cord + self.width + self.speed > 790 and Player.y_move_screen < 180:
                if not any(self.movement_hit_box.colliderect(i.move(0, -self.speed)) for i in collision_rects):
                    Player.y_move_screen += self.speed
                    Player.y_move_collision -= self.speed
            else:
                if self.y_cord + self.speed < 990 - self.height:
                    if not any(self.movement_hit_box.colliderect(i.move(0, -self.speed)) for i in collision_rects):
                        self.y_cord += self.speed
                else:
                    self.y_cord = 990 - self.height

            Player.previous_move = 4

        if not any(keys):
            self.move_player_to_next_square(collision_rects)

        self.movement_hit_box = pg.Rect(self.x_cord, self.y_cord + 20, self.width, self.height - 20)
        return Player.x_move_screen, Player.y_move_screen, Player.x_move_collision, Player.y_move_collision

    def player_draw(self, screen: pg.Surface) -> None:
        """
        the method is responsible for drawing the player on the screen
        :param screen:
        :return: None
        """
        screen.blit(self.image, (self.x_cord, self.y_cord))
