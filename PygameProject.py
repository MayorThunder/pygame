import os, pygame
import sys
from random import randint, choice

SX, SY = 1920, 1080
alls = pygame.sprite.Group()
walls = {"vl": pygame.sprite.Group(), "vr": pygame.sprite.Group(), "hu": pygame.sprite.Group(),
         "hd": pygame.sprite.Group()}
player_gr = pygame.sprite.Group()
weapon_gr = pygame.sprite.Group()
floor_bricks = pygame.sprite.Group()
form_rects = pygame.sprite.Group()
enemies = pygame.sprite.Group()
rooms = pygame.sprite.Group()


def get_image(name, k):
    fullname = os.path.join('./SpritesProject', name)
    image = pygame.image.load(fullname)
    colorkey = image.get_at((0, 0))
    if k:
        if colorkey is not None:
            image = image.convert()
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
    return image


sizes = {"wall": (24, 60), "floor": (12, 12), "stand_room": (900, 900), "corridor": (600, 300)}
wall_count = {"stand_room": sizes["stand_room"][0] // sizes["wall"][1],
              "corridor_width": sizes["corridor"][0] // sizes["wall"][1]}  # пока что все комнаты одного размера
floor_count = {"stand_room": sizes["stand_room"][0] // sizes["floor"][1],
               "corridor_height": sizes["corridor"][1] // sizes["floor"][1],
               "corridor_width": sizes["corridor"][0] // sizes["floor"][1]}
button_inf = {"w": 565, "h": 78, "x": 676, "y": [384, 535]}
classes = {"warrior": {"speed": 360, "hp": 800},
           "mage": {"speed": 240, "hp": 600},
           "ranger": {"speed": 300, "hp": 450}}

attacks = {"blade_default": "stag_blade"}

game_enemies = {"close_combat":
                    {"base_enemy":
                         {"speed": 120, "ats": 1, "dmg": 200, "ats_add": 0.05, "dmg_add": 20, "speed_add": 4, "coeff": 0.1}}}

game_weapons = {"ranks":
                    {"D":
                         {"warrior":
                              {"swords":
                                   {"stag_blade":
                                        {"size": 1, "dmg": 300, "ats": 2, "AoE": 135}}}},
                     "C": {"warrior":
                               {"swords":
                                    {"stag_blade":
                                         {"size": 1.2, "dmg": 350, "ats": 2, "AoE": 135}}}},
                     "B": {"warrior":
                               {"swords":
                                    {"stag_blade":
                                         {"size": 1.3, "dmg": 400, "ats": 2.2, "AoE": 155}}}},
                     "A": {"warrior":
                               {"swords":
                                    {"stag_blade":
                                         {"size": 1.5, "dmg": 420, "ats": 2.5, "AoE": 155}}}},
                     "S": {"warrior":
                               {"swords":
                                    {"stag_blade":
                                         {"size": 1.7, "dmg": 440, "ats": 2.8, "AoE": 155}}}},
                     "SS": {"warrior":
                                {"swords":
                                     {"stag_blade":
                                          {"size": 1.8, "dmg": 550, "ats": 3.1, "AoE": 180}}}}}}

levels_size = {
    1: (7 * sizes["stand_room"][0] + 6 * sizes["corridor"][0] + 100,
        7 * sizes["stand_room"][1] + 6 * sizes["corridor"][0] + 100)}

levels = {1: {"size": (7, 7), "iters": [[2], [2, 2], [3, 4]]}}

enemiy_spawn = {1: {"close_combat":
                   {"standart":
                       {"base_enemy": (3, 4)}}}}

doors = {(0, -1): "hu", (-1, 0): "vl", (1, 0): "vr", (0, 1): "hd"}

cur_weap = None
cur_rank = None
cur_class = "warrior"
fps = 60


def iff(n):
    return ((wall_count["stand_room"] + sizes["corridor"][1] // sizes["wall"][1]) // 2 > n
            >= (wall_count["stand_room"] - sizes["corridor"][1] // sizes["wall"][1]) // 2)


class Room(pygame.sprite.Sprite):
    def __init__(self, typer, cx, cy, lvl, num=None, empty=None):
        super().__init__(rooms, alls)
        self.cx = cx
        self.cy = cy
        self.lvl = lvl
        self.typer = typer
        self.num = num
        self.was = False
        self.rect = pygame.Rect(cx - sizes["stand_room"][0] // 2, cy - sizes["stand_room"][1] // 2,
                                sizes["stand_room"][0], sizes["stand_room"][1])
        if empty:
            self.empty = empty
        if typer == "start" or typer == "stand" or typer == "portal" or typer == "unusual":
            d = wall_count["stand_room"] / 2
            for i in range(floor_count["stand_room"]):
                for j in range(floor_count["stand_room"]):
                    Floor((i - (floor_count["stand_room"] // 2) - 1 / 2) * sizes["floor"][1],
                          (j - (floor_count["stand_room"] // 2) - 1 / 2) * sizes["floor"][1], randint(1, 3), cx, cy)
            for i in range(wall_count["stand_room"]):
                ans = iff(i)
                if not ans or (ans and "hd" not in empty):
                    Wall((i - d) * sizes["wall"][1],
                         d * sizes["wall"][1],
                         "hd", cx, cy)
                if not ans or (ans and "hu" not in empty):
                    Wall((i - d) * sizes["wall"][1],
                         -d * sizes["wall"][1] - sizes["wall"][0],
                         "hu", cx, cy)
                if not ans or (ans and "vl" not in empty):
                    Wall(-d * sizes["wall"][1] - sizes["wall"][0],
                         (i - d) * sizes["wall"][1],
                         "vl", cx, cy)
                if not ans or (ans and "vr" not in empty):
                    Wall(d * sizes["wall"][1],
                         (i - d) * sizes["wall"][1],
                         "vr", cx, cy)
        if typer == (-1, 0) or typer == (1, 0):
            d = wall_count["corridor_width"] / 2
            for i in range(floor_count["corridor_width"]):
                for j in range(floor_count["corridor_height"]):
                    Floor((i - (floor_count["corridor_width"] // 2) + (1 if typer[0] < 0 else 0)) * sizes["floor"][1] *
                          typer[0],
                          (j - (floor_count["corridor_height"] // 2) - 1 / 2) * sizes["floor"][1], randint(1, 3), cx,
                          cy)
            for i in range(wall_count["corridor_width"]):
                Wall((i - d) * sizes["wall"][1],
                     -sizes["corridor"][1] // 2,
                     "hu", cx, cy)
                Wall((i - d) * sizes["wall"][1],
                     sizes["corridor"][1] // 2,
                     "hd", cx, cy)
        if typer == (0, -1) or typer == (0, 1):
            d = wall_count["corridor_width"] / 2
            for i in range(floor_count["corridor_height"]):
                for j in range(floor_count["corridor_width"]):
                    Floor((i - (floor_count["corridor_height"] // 2) - 1 / 2) * sizes["floor"][1],
                          (j - (floor_count["corridor_width"] // 2) + (1 if typer[1] < 0 else 0)) * sizes["floor"][1] *
                          typer[1], randint(1, 3), cx, cy)
            for i in range(wall_count["corridor_width"]):
                Wall(-sizes["corridor"][1] // 2 - sizes["wall"][0],
                     (i - d) * sizes["wall"][1],
                     "vl", cx, cy)
                Wall(sizes["corridor"][1] // 2,
                     (i - d) * sizes["wall"][1],
                     "vr", cx, cy)

    def inf(self):
        return {"centre": (self.cx, self.cy), "type": self.typer}

    def doors(self):
        if self.empty:
            return self.empty

    def check(self):
        if not self.was and self.typer == "stand" and self.rect.colliderect(*player.inf().rect):
            self.was = True
            for k, v in enemiy_spawn[self.lvl]["close_combat"]["standart"].items():
                for _ in range(randint(*v)):
                    print("...")
                    Enemy(k, "close_combat", self.cx, self.cy, "stand_room", self.num, self.lvl)


class Wall(pygame.sprite.Sprite):
    def __init__(self, d_x, d_y, wall_type, centre_x, centre_y):
        super().__init__(walls[wall_type], alls)
        self.image = sprite_images["walls"][wall_type]
        self.rect = self.image.get_rect().move(centre_x + d_x, centre_y + d_y)


class Floor():
    def __init__(self, x, y, brick_type, centre_x, centre_y):
        self.image = sprite_images["floor"][brick_type]
        self.rect = self.image.get_rect().move(centre_x + x, centre_y + y)
        screen_add.blit(self.image, (self.rect.x, self.rect.y))


class FormalRect(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__(form_rects, alls)
        self.rect = pygame.Rect(x, y, w, h)


class Player(pygame.sprite.Sprite):
    def __init__(self, pl_class):
        super().__init__(player_gr, alls)
        self.image = sprite_images['player'][pl_class][0]
        k = self.image.get_rect()
        self.cl = pl_class
        self.v = classes[self.cl]["speed"]
        self.cur_hp = classes[self.cl]["hp"]
        self.rect = k.move(SX // 2 - k.w // 2, SY // 2 - k.h // 2)
        self.turn = False
        self.wall_collidable_sprite = FormalRect(levels_size[1][0] // 2 - k.w // 2, levels_size[1][1] // 2 - k.h // 2,
                                                 k.w, k.h)

    def move(self, x, y):
        ret = self.on_col(x, y)
        if ret[0]:
            self.wall_collidable_sprite.rect.x += (classes[cur_class]["speed"] / fps) * x
        if ret[1]:
            self.wall_collidable_sprite.rect.y += (classes[cur_class]["speed"] / fps) * y
        if self.turn and x > 0:
            self.turn = not self.turn
            self.image = sprite_images['player'][self.cl][0]
        elif not self.turn and x < 0:
            self.turn = not self.turn
            self.image = sprite_images['player'][self.cl][1]
        weapon.apply(self.rect.x, self.rect.y, self.turn)

    def on_col(self, x, y):
        ans_x, ans_y = True, True
        if x > 0 and pygame.sprite.spritecollideany(self.wall_collidable_sprite, walls["vr"]):
            ans_x = False
        elif x < 0 and pygame.sprite.spritecollideany(self.wall_collidable_sprite, walls["vl"]):
            ans_x = False
        if y > 0 and pygame.sprite.spritecollideany(self.wall_collidable_sprite, walls["hd"]):
            ans_y = False
        elif y < 0 and pygame.sprite.spritecollideany(self.wall_collidable_sprite, walls["hu"]):
            ans_y = False
        return ans_x, ans_y

    def inf(self):
        return self.wall_collidable_sprite


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_class, entype, cx, cy, spawn, roomn, lvl):
        super().__init__(enemies, alls)
        self.image = sprite_images['enemies'][entype][enemy_class][0]
        k = self.image.get_rect()
        self.cl = enemy_class
        self.v = ((game_enemies[entype][self.cl]["speed"] + game_enemies[entype][self.cl]["speed_add"] * (roomn - 2))
                  * (1 + game_enemies[entype][self.cl]["coeff"] * (lvl - 1)))
        print(self.v)
        self.dmg = ((game_enemies[entype][self.cl]["dmg"] + game_enemies[entype][self.cl]["dmg_add"] * (roomn - 2))
                  * (1 + game_enemies[entype][self.cl]["coeff"] * (lvl - 1)))
        self.dmg = ((game_enemies[entype][self.cl]["ats"] + game_enemies[entype][self.cl]["ats_add"] * (roomn - 2))
                    * (1 + game_enemies[entype][self.cl]["coeff"] * (lvl - 1)))
        dx = randint(-(sizes[spawn][0] - k.w) // 2, (sizes[spawn][0] - k.w) // 2)
        dy = (((sizes[spawn][0] - k.w) // 2) ** 2 - dx ** 2) ** 0.5
        print(f"dx:{dx}, dy:{dy}, cx:{cx}, cy:{cy}, rect:{player.inf().rect}")
        dy = choice([dy, -dy])
        self.formspr = FormalRect(cx + dx, cy + dy, k.w, k.h)
        self.rect = k.move(cx + dx - player.inf().rect.x + SX // 2 - 50, cy + dy - player.inf().rect.y + SY // 2 - 50)
        self.turn = False
        self.timer = 0

    def apply(self, x, y):
        self.rect.x -= x
        self.rect.y -= y

        delta = (player.inf().rect.x - self.formspr.rect.x, player.inf().rect.y - self.formspr.rect.y)
        self.rect.x += self.v * (delta[0] // (delta[0] + delta[1] if delta[0] and delta[1] else 2 ** 0.5))
        self.rect.y += self.v * (delta[1] // (delta[0] + delta[1] if delta[0] and delta[1] else 2 ** 0.5))

        self.formspr.rect.x += self.v * (delta[0] // (delta[0] + delta[1] if delta[0] and delta[1] else 2 ** 0.5))
        self.formspr.rect.y += self.v * (delta[1] // (delta[0] + delta[1] if delta[0] and delta[1] else 2 ** 0.5))


def generate_level(n):
    s = levels[n]["size"]
    itr = levels[n]["iters"]
    data = [[0 for _ in range(s[1])] for _ in range(s[0])]
    types = [[0 for _ in range(s[1])] for _ in range(s[0])]
    types[s[0] // 2][s[1] // 2] = 1
    data[s[0] // 2][s[1] // 2] = 1
    coords = [(s[0] // 2, s[1] // 2)]
    generator = set()
    for i in range(len(itr)):
        for a, b in coords:
            for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if not data[a + x][b + y]:
                    generator.add((a + x, b + y))
        coords.clear()
        for _ in range(len(itr[i])):
            t = choice(list(generator))
            generator -= {t}
            coords.append(t)
        generator.clear()
        for a in range(len(coords)):
            data[coords[a][0]][coords[a][1]] = i + 2
            types[coords[a][0]][coords[a][1]] = itr[i][a]
    emptiness = []
    print("data:")
    for i in data:
        print(*i)
    print("types:")
    for i in types:
        print(*i)
    for a in range(len(data)):
        for b in range(len(data[0])):
            if data[a][b]:
                for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    if 0 <= a + x < len(data) and 0 <= b + y < len(data):
                        if data[a + x][b + y] and abs(data[a + x][b + y] - data[a][b]) == 1:
                            emptiness.append(doors[(y, x)])
                            Room((y, x),
                                 (b + 0.5 + y * 0.5) * sizes["stand_room"][0] + (b + 0.5 * y) * sizes["corridor"][0],
                                 (a + 0.5 + x * 0.5) * sizes["stand_room"][1] + (a + 0.5 * x) * sizes["corridor"][0], n)
                name = None
                if types[a][b] == 1:
                    name = "start"
                elif types[a][b] == 2:
                    name = "stand"
                elif types[a][b] == 3:
                    name = "unusual"
                elif types[a][b] == 4:
                    name = "portal"
                Room(name, (b + 0.5) * sizes["stand_room"][0] + b * sizes["corridor"][0],
                     (a + 0.5) * sizes["stand_room"][1] + a * sizes["corridor"][0], n, num=data[a][b], empty=emptiness)
                emptiness.clear()


class Warrior_weapon(pygame.sprite.Sprite):
    def __init__(self, rank, weap, weap_cl):
        super().__init__(weapon_gr, alls)
        self.position = "hold"
        self.is_attacking = False
        self.side = False
        self.rank = rank
        self.weapon = weap
        self.weapon_class = weap_cl
        self.image = sprite_images["war_weapons"][self.position][self.weapon][0]
        self.size = game_weapons["ranks"][self.rank]["warrior"][self.weapon_class][self.weapon]["size"]
        self.image = pygame.transform.scale_by(self.image, self.size)
        self.rect = self.image.get_rect().move(0, 0)
        self.dmg = game_weapons["ranks"][self.rank]["warrior"][self.weapon_class][self.weapon]["dmg"]
        self.AoE = game_weapons["ranks"][self.rank]["warrior"][self.weapon_class][self.weapon]["AoE"]
        self.ats = game_weapons["ranks"][self.rank]["warrior"][self.weapon_class][self.weapon]["ats"]
        self.timer = 0
        self.cox1 = 154 * self.size ** 1.15
        self.cox2 = -65 * self.size ** 1.05
        self.coy = -121 * self.size ** 0.6

    def apply(self, x, y, side):
        self.side = side
        formx = (-self.rect.w + self.cox1 if not side else self.rect.w + self.cox2)
        formy = self.rect.h + self.coy
        if not self.is_attacking:
            self.image = pygame.transform.scale_by(
                sprite_images['war_weapons'][self.position][self.weapon][1 if self.side else 0], self.size)
            self.rect.x = x - formx
            self.rect.y = y - formy
        elif self.timer < fps / self.ats:
            self.timer += 1
            self.image = pygame.transform.rotate(pygame.transform.scale_by(
                sprite_images["war_weapons"][self.position][self.weapon][1 if self.side else 0], self.size),
                                                 self.AoE / (fps / self.ats) * self.timer * (1 if self.side else -1))
            self.rect.x = x - formx - 25
            self.rect.y = y - formy - 15
        else:
            self.timer = 0
            self.is_attacking = False
            self.position = "hold"
            self.image = pygame.transform.scale_by(
                sprite_images["war_weapons"][self.position][self.weapon][1 if self.side else 0], self.size)
            self.rect.x = x - formx
            self.rect.y = y - formy

    def attack(self):
        if not self.is_attacking:
            self.position = "attack"
            self.image = sprite_images["war_weapons"][self.position][self.weapon][1 if self.side else 0]
            self.is_attacking = True


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    pygame.init()
    w, h = SX, SY
    screen_add = pygame.Surface((levels_size[1][0], levels_size[1][1]))
    screen = pygame.display.set_mode((w, h))
    data_fon = {"start": {0: get_image('Fon_start_1.png', False), 1: get_image('Fon_start_2.png', False),
                          2: get_image('Fon_start_3.png', False)}}
    fon_set = "start"
    pygame.display.set_caption("Soul fight")
    clock = pygame.time.Clock()
    player = None
    weapon = None

    sprite_images = {'walls': {"hu": get_image('Wall_brick_horizontal.png', False),
                               "hd": pygame.transform.rotate(get_image('Wall_brick_horizontal.png', False), 180),
                               "vl": get_image('Wall_brick_vertical.png', False),
                               "vr": pygame.transform.rotate(get_image('Wall_brick_vertical.png', False), 180)},
                     'floor': {1: get_image('Floor_brick_1.png', False),
                               2: get_image('Floor_brick_2.png', False),
                               3: get_image('Floor_brick_3.png', False)},
                     'player': {"warrior": [get_image('Warrior_armor.png', True),
                                            pygame.transform.flip(get_image('Warrior_armor.png', True), 1, 0)],
                                "ranger": [get_image('Ranger_armor.png', True),
                                           pygame.transform.flip(get_image('Ranger_armor.png', True), 1, 0)]},
                     'enemies': {"close_combat":
                                     {"base_enemy": [get_image('Base_enemy.png', True),
                                                     pygame.transform.flip(get_image('Warrior_armor.png', True), 1,
                                                                           0)]}},
                     'war_weapons': {"default":
                                         {"stag_blade": [get_image("Stagnum_blade.png", True),
                                                         pygame.transform.flip(get_image("Stagnum_blade.png", True), 1,
                                                                               0)]},
                                     "hold":
                                         {"stag_blade": [get_image("Stagnum_blade_handed.png", True),
                                                         pygame.transform.flip(
                                                             get_image("Stagnum_blade_handed.png", True), 1, 0)]},
                                     "attack":
                                         {"stag_blade": [get_image("Stagnum_blade_attack.png", True),
                                                         pygame.transform.flip(
                                                             get_image("Stagnum_blade_attack.png", True), 1, 0)]}}}
    screen_x = -levels_size[1][0] // 2 + SX // 2
    screen_y = -levels_size[1][1] // 2 + SY // 2
    count = 0
    dx = 0
    dy = 0
    while True:
        count += 1
        if count == fps:
            count -= fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            elif event.type == pygame.KEYDOWN:
                if fon_set == "game":
                    if event.key == pygame.K_a:
                        dx -= 1
                    elif event.key == pygame.K_d:
                        dx += 1
                    elif event.key == pygame.K_s:
                        dy += 1
                    elif event.key == pygame.K_w:
                        dy -= 1

            elif event.type == pygame.KEYUP:
                if fon_set == "game":
                    if event.key == pygame.K_a:
                        dx += 1
                    elif event.key == pygame.K_d:
                        dx -= 1
                    elif event.key == pygame.K_w:
                        dy += 1
                    elif event.key == pygame.K_s:
                        dy -= 1

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if fon_set == "start":
                    if (button_inf["x"] <= event.pos[0] <= button_inf["x"] + button_inf["w"]
                            and button_inf["y"][0] <= event.pos[1] <= button_inf["y"][0] + button_inf["h"]):
                        screen.fill("black")
                        cur_lvl = 1
                        generate_level(cur_lvl)
                        fon_set = "game"

                        if cur_class == "warrior":
                            cur_weap = "stag_blade"
                            weapon_class = "swords"
                            cur_rank = "SS"
                            player = Player("warrior")
                            for i in walls:
                                walls[i].draw(screen_add)
                            weapon = Warrior_weapon(cur_rank, cur_weap, weapon_class)
                elif fon_set == "game" and event.button == pygame.BUTTON_LEFT:
                    weapon.attack()

        if fon_set == "start" and count % 6:
            screen.blit(data_fon["start"][(count // 6) % 3], (0, 0))
        if fon_set == "game":
            res = player.on_col(dx, dy)
            if res[0]:
                screen_x -= (classes[cur_class]["speed"] / fps) * dx
            if res[1]:
                screen_y -= (classes[cur_class]["speed"] / fps) * dy
            screen.blit(screen_add, (screen_x, screen_y))
            player.move(dx, dy)
            player_gr.draw(screen)
            weapon_gr.draw(screen)
            for i in rooms:
                i.check()
            for i in enemies:
                i.apply(((classes[cur_class]["speed"] / fps) * dx if res[0] else 0),
                ((classes[cur_class]["speed"] / fps) * dy if res[1] else 0))
            enemies.draw(screen)
        pygame.display.flip()
        clock.tick(fps)