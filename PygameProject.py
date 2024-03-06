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
portals = pygame.sprite.Group()
close_combat_enemies = pygame.sprite.Group()
rooms = pygame.sprite.Group()
heal_c = pygame.sprite.Group()
transition_killable = pygame.sprite.Group()


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
classes = {"warrior": {"speed": 360, "hp": 800, "protection": 0.5},
           "mage": {"speed": 300, "hp": 600, "protection": 0.5},
           "ranger": {"speed": 360, "hp": 450, "protection": 0.5}}

fon_set = None

attacks = {"blade_default": "stag_blade"}

game_enemies = {"close_combat":
                    {"ghast":
                         {"speed": 150, "ats": 1, "hp": 1000, "contact_dmg": 100, "ats_add": 0.05,
                          "hp_add": 100, "contact_dmg_add": 10, "speed_add": 4, "coeff": 0.1},
                     "demon_ghast":
                         {"speed": 90, "ats": 0.6, "hp": 4000, "contact_dmg": 300, "ats_add": 0.03,
                          "hp_add": 400, "contact_dmg_add": 35, "speed_add": 2, "coeff": 0.08}}}

game_weapons = {"ranks":
                    {"D":
                         {"warrior":
                              {"swords":
                                   {"stag_blade":
                                        {"size": 1.1, "dmg": 250, "ats": 2.1, "AoE": 135}}}},
                     "C": {"warrior":
                               {"swords":
                                    {"stag_blade":
                                         {"size": 1.3, "dmg": 280, "ats": 2.2, "AoE": 135}}}},
                     "B": {"warrior":
                               {"swords":
                                    {"stag_blade":
                                         {"size": 1.4, "dmg": 310, "ats": 2.3, "AoE": 135}}}},
                     "A": {"warrior":
                               {"swords":
                                    {"stag_blade":
                                         {"size": 1.5, "dmg": 350, "ats": 2.5, "AoE": 135}}}},
                     "S": {"warrior":
                               {"swords":
                                    {"stag_blade":
                                         {"size": 1.6, "dmg": 400, "ats": 2.7, "AoE": 135}}}},
                     "SS": {"warrior":
                                {"swords":
                                     {"stag_blade":
                                          {"size": 1.8, "dmg": 450, "ats": 3.1, "AoE": 135}}}}}}

damage_col = {"weapons":
                  {"warrior": "orange"},
              "close_combat": "red"}

spawn_const = 200

levels_size = {
    1: (7 * sizes["stand_room"][0] + 6 * sizes["corridor"][0] + spawn_const,
        7 * sizes["stand_room"][1] + 6 * sizes["corridor"][0] + spawn_const),
    2: (7 * sizes["stand_room"][0] + 6 * sizes["corridor"][0] + spawn_const,
        7 * sizes["stand_room"][1] + 6 * sizes["corridor"][0] + spawn_const),
    3: (9 * sizes["stand_room"][0] + 8 * sizes["corridor"][0] + spawn_const,
        9 * sizes["stand_room"][1] + 8 * sizes["corridor"][0] + spawn_const)
}

levels = {1: {"size": (7, 7), "iters": [[2], [2, 2], [3, 4]]},
          2: {"size": (7, 7), "iters": [[2, 2], [2, 3], [2, 3, 4]]},
          3: {"size": (9, 9), "iters":[[2], [2, 2, 3], [2, 2, 3, 4], [2, 4]]}}

enemiy_spawn = {1: {"close_combat":
                        {"standart":
                             {"ghast": {2: (2, 3), 3: (3, 4)}}}},
                2: {"close_combat":
                        {"standart":
                             {"ghast": {2: (3, 4), 3: (2, 3), 4: (5, 7), "demon_ghast": {2: (0, 0), 3: (1, 1), 4: (0, 0)}}}}},
                3: {"close_combat":
                        {"standart":
                             {"ghast": {2: (3, 5), 3: (3, 3), 4: (5, 6), 5: (0, 0)}, "demon_ghast": {2: (0, 0), 3: (1, 2), 4: (0, 0), 5: (2, 3)}}}}
                    }

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
        super().__init__(rooms, alls, transition_killable)
        self.cx = cx
        self.cy = cy
        self.lvl = lvl
        self.typer = typer
        self.num = num
        self.was = False
        self.rect = pygame.Rect(cx - sizes["stand_room"][0] // 2 + 50, cy - sizes["stand_room"][1] // 2 + 50,
                                sizes["stand_room"][0] - 50, sizes["stand_room"][1] - 50)
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

        if typer == "portal":
            Portal(cx, cy, "room_transition")

        elif typer == "unusual":
            Heals_consumable(0.4, sprite_images['heals_consumable'], self.cx, self.cy)

    def inf(self):
        return {"centre": (self.cx, self.cy), "type": self.typer}

    def doors(self):
        if self.empty:
            return self.empty

    def check(self):
        if not self.was and self.typer == "stand" and self.rect.colliderect(*player.inf().rect):
            self.was = True
            for k, v in enemiy_spawn[self.lvl]["close_combat"]["standart"].items():
                for _ in range(randint(*v[self.num])):
                    Close_Combat_Enemy(k, "close_combat", self.cx, self.cy, "stand_room", self.num, self.lvl)


class Wall(pygame.sprite.Sprite):
    def __init__(self, d_x, d_y, wall_type, centre_x, centre_y):
        super().__init__(walls[wall_type], alls, transition_killable)
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


def anihillation():
    global fon_set
    fon_set = "death"


class Player(pygame.sprite.Sprite):
    def __init__(self, pl_class):
        super().__init__(player_gr, alls)
        self.image = sprite_images['player'][pl_class][0]
        self.mask = pygame.mask.from_surface(self.image)
        k = self.image.get_rect()
        self.cl = pl_class
        self.v = classes[self.cl]["speed"]
        self.cur_hp = classes[self.cl]["hp"]
        self.max_hp = self.cur_hp
        self.rect = k.move(SX // 2 - k.w // 2, SY // 2 - k.h // 2)
        self.turn = False
        self.protection = classes[self.cl]["protection"] * fps
        self.timer = 0
        self.wall_collidable_sprite = FormalRect(levels_size[1][0] // 2 - k.w // 2, levels_size[1][1] // 2 - k.h // 2,
                                                 k.w, k.h)

    def move(self, x, y):
        if self.cur_hp < 0:
            anihillation()
        if self.timer:
            self.timer -= 1
        ret = pygame.sprite.spritecollideany(self.wall_collidable_sprite, heal_c)
        if ret:
            hp = ret.used()
            if hp < 1:
                self.cur_hp = (self.cur_hp + self.max_hp * hp if self.cur_hp + self.max_hp * hp < self.max_hp else self.max_hp)
            else:
                self.cur_hp = (self.cur_hp + hp if self.cur_hp + hp < self.max_hp else self.max_hp)
        ret = self.on_col(x, y)
        if ret[0]:
            self.wall_collidable_sprite.rect.x += (classes[cur_class]["speed"] / fps) * x
        if ret[1]:
            self.wall_collidable_sprite.rect.y += (classes[cur_class]["speed"] / fps) * y
        if weapon.ans_attacking():
            if pygame.mouse.get_pos()[0] > self.rect.x and self.turn:
                self.turn = not self.turn
                self.image = sprite_images['player'][self.cl][0]
            elif pygame.mouse.get_pos()[0] < self.rect.x and not self.turn:
                self.turn = not self.turn
                self.image = sprite_images['player'][self.cl][1]
        else:
            if self.turn and x > 0:
                self.turn = not self.turn
                self.image = sprite_images['player'][self.cl][0]
            elif not self.turn and x < 0:
                self.turn = not self.turn
                self.image = sprite_images['player'][self.cl][1]
        player_health_bar.apply(self.cur_hp)
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

    def get_damage(self, amount, entype):
        if not self.timer:
            real_dmg = randint(int(0.9 * amount), int(1.1 * amount))
            damage.add_to_showlist(damage_col[entype],
                                   self.rect.x, self.rect.y - 1.5 * self.rect.h, real_dmg)
            self.cur_hp -= real_dmg
            self.timer += 30

    def transition(self, x, y):
        self.wall_collidable_sprite.rect.x = levels_size[cur_lvl][0] // 2 - self.rect.w // 2
        self.wall_collidable_sprite.rect.y = levels_size[cur_lvl][1] // 2 - self.rect.h // 2

    def kill(self):
        self.wall_collidable_sprite.kill()
        super().kill()


class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, port_type):
        super().__init__(alls, portals, transition_killable)
        self.image = sprite_images['portals'][port_type]
        k = self.image.get_rect()
        self.rect = pygame.Rect(x - k.w // 2, y - k.h // 2, k.w, k.h)

    def check(self):
        return player.inf().rect.colliderect(self.rect)


class Heals_consumable(pygame.sprite.Sprite):
    def __init__(self, hp, im_path, x, y):
        super().__init__(alls, transition_killable, heal_c)
        self.heal = hp
        self.im_path = im_path
        self.image = self.im_path["healing_heart"]
        k = self.image.get_rect()
        self.rect = pygame.Rect(x - k.w // 2, y - k.h // 2, k.w, k.h)

    def used(self):
        self.image = self.im_path["healing_heart_used"]
        heal_c.draw(screen_add)
        self.kill()
        return self.heal


class PlayerHealthBar():
    def __init__(self, x, y, hp):
        self.max_hp = hp
        self.x = x
        self.y = y
        self.health_bar_size = (46, 28)
        self.left_bar = sprite_images['bars']["player"]["left"]
        self.left_bar_rect = self.left_bar.get_rect()
        self.medium_bar = sprite_images['bars']["player"]["medium"]
        self.medium_bar_rect = self.medium_bar.get_rect()
        self.right_bar = sprite_images['bars']["player"]["right"]
        self.right_bar_rect = self.right_bar.get_rect()

    def apply(self, hp):
        screen.blit(self.left_bar, (self.x, self.y))
        pygame.draw.rect(screen, "black",
                         (self.x + 3, self.y + 3, *self.health_bar_size))
        pygame.draw.rect(screen, (146, 0, 10),
                         (self.x + 3, self.y + 3, self.health_bar_size[0] * (1 if hp >= 50 else hp / 50),
                          self.health_bar_size[1]))
        for i in range(self.max_hp // 50 - 2):
            screen.blit(self.medium_bar, (self.x + i * self.medium_bar_rect.w + self.left_bar_rect.w, self.y))
            pygame.draw.rect(screen, "black",
                             (self.x + i * self.medium_bar_rect.w + self.left_bar_rect.w + 1,
                              self.y + 3, *self.health_bar_size))
            if hp > (i + 1) * 50:
                pygame.draw.rect(screen, (146, 0, 10), (self.x + i * self.medium_bar_rect.w + self.left_bar_rect.w + 1,
                              self.y + 3, self.health_bar_size[0] * (1 if hp > (i + 2) * 50 else (hp - (i + 1) * 50) / 50),
                              self.health_bar_size[1]))
        screen.blit(self.right_bar, (self.x + (self.max_hp // 50 - 2) * self.medium_bar_rect.w + self.left_bar_rect.w, self.y))
        pygame.draw.rect(screen, "black",
                         (self.x + (self.max_hp // 50 - 2) * self.medium_bar_rect.w + self.left_bar_rect.w + 1,
                          self.y + 3, *self.health_bar_size))
        if hp > self.max_hp - 50:
            pygame.draw.rect(screen, (146, 0, 10),
                             (self.x + (self.max_hp // 50 - 2) * self.medium_bar_rect.w + self.left_bar_rect.w + 1,
                              self.y + 3, self.health_bar_size[0] * (1 if hp == self.max_hp else (self.max_hp - hp) / 50),
                              self.health_bar_size[1]))

    def change(self, hp):
        self.max_hp = hp


class Close_Combat_Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_class, entype, cx, cy, spawn, roomn, lvl):
        super().__init__(enemies, close_combat_enemies, transition_killable)
        self.cl = enemy_class
        self.entype = entype
        self.cur_hp = ((game_enemies[entype][self.cl]["hp"] + game_enemies[entype][self.cl]["hp_add"] * (roomn - 2))
                       * (1 + game_enemies[entype][self.cl]["coeff"] * (lvl - 1)))
        self.v = ((game_enemies[entype][self.cl]["speed"] + game_enemies[entype][self.cl]["speed_add"] * (roomn - 2))
                  * (1 + game_enemies[entype][self.cl]["coeff"] * (lvl - 1)))
        self.dmg = ((game_enemies[entype][self.cl]["contact_dmg"] + game_enemies[entype][self.cl]["contact_dmg_add"] * (
                    roomn - 2))
                    * (1 + game_enemies[entype][self.cl]["coeff"] * (lvl - 1)))
        self.ats = ((game_enemies[entype][self.cl]["ats"] + game_enemies[entype][self.cl]["ats_add"] * (roomn - 2))
                    * (1 + game_enemies[entype][self.cl]["coeff"] * (lvl - 1)))
        self.image = pygame.transform.scale_by(sprite_images['enemies'][entype][enemy_class],
                                               (1 + game_enemies[entype][self.cl]["coeff"] * (lvl - 1)))
        self.mask = pygame.mask.from_surface(self.image)
        k = self.image.get_rect()
        dx = randint(-(sizes[spawn][0] - k.w) // 2, (sizes[spawn][0] - k.w) // 2)
        dy = (((sizes[spawn][0] - k.w) // 2) ** 2 - dx ** 2) ** 0.5
        dy = choice([dy, -dy])
        self.formspr = FormalRect(cx + dx, cy + dy, k.w, k.h)
        self.rect = k.move(cx + dx - player.inf().rect.x + SX // 2 - 50, cy + dy - player.inf().rect.y + SY // 2 - 50)
        self.turn = False
        self.dmg_timer = 0
        self.attack_timer = 0

    def apply(self, x, y):
        if self.cur_hp <= 0:
            self.kill()
        ret = pygame.sprite.spritecollideany(self, player_gr)
        if ret and not self.attack_timer:
            self.attack_timer = fps // self.ats + 1
            ret.get_damage(self.dmg, self.entype)
        elif self.attack_timer:
            self.attack_timer -= 1
        self.rect.x -= x
        self.rect.y -= y
        if self.dmg_timer:
            self.dmg_timer -= 1

        deltax = player.inf().rect.x - self.formspr.rect.x
        deltay = player.inf().rect.y - self.formspr.rect.y
        delta = (deltax ** 2 + deltay ** 2) ** 0.5
        if deltax or deltay:
            self.rect.x += (self.v / fps) * (deltax / delta)
            self.formspr.rect.x += (self.v / fps) * (deltax / delta)
            self.rect.y += (self.v / fps) * (deltay / delta)
            self.formspr.rect.y += (self.v / fps) * (deltay / delta)

    def get_damage(self, amount, time, weap_connected_to_class):
        if not self.dmg_timer:
            real_dmg = randint(int(0.9 * amount), int(1.1 * amount))
            damage.add_to_showlist(damage_col["weapons"][weap_connected_to_class],
                                   self.rect.x, self.rect.y - self.rect.h, real_dmg)
            self.cur_hp -= real_dmg
            self.dmg_timer += time

    def kill(self):
        self.formspr.kill()
        super().kill()


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
                                 (b + 0.5 + y * 0.5) * sizes["stand_room"][0] + (b + 0.5 * y) * sizes["corridor"][0] + spawn_const // 2,
                                 (a + 0.5 + x * 0.5) * sizes["stand_room"][1] + (a + 0.5 * x) * sizes["corridor"][0] + spawn_const // 2, n)
                name = None
                if types[a][b] == 1:
                    name = "start"
                elif types[a][b] == 2:
                    name = "stand"
                elif types[a][b] == 3:
                    name = "unusual"
                elif types[a][b] == 4:
                    name = "portal"
                Room(name, (b + 0.5) * sizes["stand_room"][0] + b * sizes["corridor"][0] + spawn_const // 2,
                     (a + 0.5) * sizes["stand_room"][1] + a * sizes["corridor"][0] + spawn_const // 2, n, num=data[a][b], empty=emptiness)
                emptiness.clear()
    for i in walls:
        walls[i].draw(screen_add)
    portals.draw(screen_add)
    heal_c.draw(screen_add)


class Warrior_weapon(pygame.sprite.Sprite):
    def __init__(self, rank, weap, weap_cl):
        super().__init__(weapon_gr, alls)
        self.position = "hold"
        self.is_attacking = False
        self.side = False
        self.rank = rank
        self.connect_to_class = "warrior"
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
            ret = pygame.sprite.spritecollideany(self, enemies)
            if ret:
                ret.get_damage(self.dmg, (fps // self.ats - self.timer) + 2, self.connect_to_class)
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

    def ans_attacking(self):
        return self.is_attacking


class Damage():
    def __init__(self):
        self.damage_show_list = []
        self.max_time = 60

    def add_to_showlist(self, col, x, y, n):
        font = pygame.font.Font(None, 40)
        text = font.render(str(n), True, col)
        self.damage_show_list.append([text, (x, y), self.max_time])

    def apply(self):
        x = self.damage_show_list
        deleting = []
        for i in range(len(x)):
            if x[i][2]:
                screen.blit(x[i][0], x[i][1])
                x[i][2] -= 1
            else:
                deleting.append(i)
        for i in deleting:
            self.damage_show_list.pop(i)


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
                     'portals': {"room_transition": get_image("Portal.png", True)},
                     'heals_consumable': {"healing_heart": get_image("Healing_heart.png", True),
                                          "healing_heart_used": get_image("Healing_heart_used.png", True)},
                     'bars': {"player":
                                  {"left": get_image("Health_bar_left.png", True),
                                   "medium": get_image("Health_bar_medium.png", True),
                                   "right": get_image("Health_bar_right.png", True)}},
                     'floor': {1: get_image('Floor_brick_1.png', False),
                               2: get_image('Floor_brick_2.png', False),
                               3: get_image('Floor_brick_3.png', False)},
                     'player': {"warrior": [get_image('Warrior_armor.png', True),
                                            pygame.transform.flip(get_image('Warrior_armor.png', True), 1, 0)],
                                "ranger": [get_image('Ranger_armor.png', True),
                                           pygame.transform.flip(get_image('Ranger_armor.png', True), 1, 0)]},
                     'enemies': {"close_combat":
                                     {"ghast": get_image('Ghast.png', True),
                                      "demon_ghast": get_image('Demon_ghast.png', True)}},
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
    damage = Damage()
    screen_x = -levels_size[1][0] // 2 + SX // 2
    screen_y = -levels_size[1][1] // 2 + SY // 2
    count = 0
    cur_lvl = None
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
                    elif fon_set == "game" and event.key == pygame.K_t:
                        for portal in portals:
                            if portal.check():
                                cur_lvl += 1
                                screen_x = -levels_size[cur_lvl][0] // 2 + SX // 2
                                screen_y = -levels_size[cur_lvl][1] // 2 + SY // 2
                                screen_add = pygame.Surface((levels_size[cur_lvl][0], levels_size[cur_lvl][1]))
                                player.transition(levels_size[cur_lvl][0] // 2, levels_size[cur_lvl][0] // 2)
                                for i in transition_killable:
                                    i.kill()
                                screen_add.fill("black")
                                generate_level(cur_lvl)
                                break

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
                        screen_x = -levels_size[1][0] // 2 + SX // 2
                        screen_y = -levels_size[1][1] // 2 + SY // 2
                        generate_level(cur_lvl)
                        fon_set = "game"

                        if cur_class == "warrior":
                            cur_weap = "stag_blade"
                            weapon_class = "swords"
                            cur_rank = "SS"
                            player = Player("warrior")
                            weapon = Warrior_weapon(cur_rank, cur_weap, weapon_class)
                        player_health_bar = PlayerHealthBar(200, 150, classes[cur_class]["hp"])
                elif fon_set == "game" and event.button == pygame.BUTTON_LEFT:
                    weapon.attack()
        if fon_set == "death":
            for i in alls:
                i.kill()
            screen.fill("black")
            screen_add.fill("black")
            font = pygame.font.Font(None, 200)
            text = font.render("You died", True, (255, 100, 100))
            screen.blit(text, (SX // 2 - 300, SY // 2 - 100))
        elif fon_set == "start" and count % 6:
            screen.blit(data_fon["start"][(count // 6) % 3], (0, 0))
        elif fon_set == "game":
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
            damage.apply()
        pygame.display.flip()
        clock.tick(fps)
