import pygame
import pytmx
import pyscroll

from player import Player


class Game:

    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Pygamon")

        tmx_data = pytmx.util_pygame.load_pygame("carte.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)

        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        enter_house = tmx_data.get_object_by_name("enter_house")
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)
        self.map = 1

    def handling_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation("up")
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation("down")
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation("left")
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation("right")

    def switch_house(self):
        tmx_data = pytmx.util_pygame.load_pygame("house.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        player_position = tmx_data.get_object_by_name("spawn_house")
        self.player = Player(player_position.x, player_position.y)

        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        enter_house = tmx_data.get_object_by_name("exit_house")
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        spawn_house_point = tmx_data.get_object_by_name("spawn_house")
        self.player.position[0] = spawn_house_point.x - 20
        self.player.position[1] = spawn_house_point.y

    def switch_world(self):
        tmx_data = pytmx.util_pygame.load_pygame("carte.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        enter_house = tmx_data.get_object_by_name("enter_house")
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        spawn_house_point = tmx_data.get_object_by_name("enter_house_exit")
        self.player.position[0] = spawn_house_point.x - 20
        self.player.position[1] = spawn_house_point.y

    def update(self):
        self.group.update()
        if self.map == 1 and self.player.feet.colliderect(self.enter_house_rect):
            self.map = 2
            self.switch_house()

        if self.map == 2 and self.player.feet.colliderect(self.enter_house_rect):
            self.map = 1
            self.switch_world()

        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def run(self):

        clock = pygame.time.Clock()

        running = True

        while running:

            self.player.save_location()
            self.handling_input()
            self.update()
            self.group.center(self.player.rect)
            self.group.draw(self.screen)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick((60))

        pygame.quit()