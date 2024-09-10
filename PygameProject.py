import os, pygame
import sys
from math import sin, cos, radians
from random import randint, choice
from Weapon_work_list import Stagnum_blade, Handgun, Volcano, Moon_blessing, Planetar_bomber, Rail_minigun, Shotgun, \
    Plasma_flow

SX, SY = 1920, 1080
alls = pygame.sprite.Group()
walls = {"vl": pygame.sprite.Group(), "vr": pygame.sprite.Group(), "hu": pygame.sprite.Group(),
         "hd": pygame.sprite.Group()}
player_gr = pygame.sprite.Group()
weapon_gr = pygame.sprite.Group()
proj_gr = pygame.sprite.Group()
floor_bricks = pygame.sprite.Group()
form_rects = pygame.sprite.Group()
enemies = pygame.sprite.Group()
portals = pygame.sprite.Group()
close_combat_enemies = pygame.sprite.Group()
rooms = pygame.sprite.Group()
heal_c = pygame.sprite.Group()
animations = pygame.sprite.Group()
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
classes = {"warrior": {"speed": 240, "hp": 800, "protection": 0.5},
           "mage": {"speed": 300, "hp": 600, "protection": 0.5},
           "ranger": {"speed": 360, "hp": 450, "protection": 0.5}}

fon_set = None
splash_lifetime_const = 0.25
attacks = {"blade_default": "stag_blade"}

game_enemies = {"close_combat":
                    {"ghast":
                         {"speed": 180, "ats": 1, "hp": 1000, "contact_dmg": 100, "ats_add": 0.05,
                          "hp_add": 100, "contact_dmg_add": 10, "speed_add": 4, "coeff": 0.1},
                     "demon_ghast":
                         {"speed": 60, "ats": 0.6, "hp": 4000, "contact_dmg": 300, "ats_add": 0.05,
                          "hp_add": 400, "contact_dmg_add": 45, "speed_add": 1, "coeff": 0.05},
                     "spider":
                         {"speed": 360, "ats": 2, "hp": 150, "contact_dmg": 30, "ats_add": 0.05,
                          "hp_add": 7, "contact_dmg_add": 2, "speed_add": 4, "coeff": 0.05}
                     }}

effect_list = {"electrified":
                   {"tier_1": {"dmg_get_coeff": 1.1, "dmg_dealt_coeff": 0.95, "speed_coeff": 0.92, "hp_reduction_per_sec": 50},
                    "tier_2": {"dmg_get_coeff": 1.175, "dmg_dealt_coeff": 0.9, "speed_coeff": 0.84, "hp_reduction_per_sec": 100},
                    "tier_3": {"dmg_get_coeff": 1.25, "dmg_dealt_coeff": 0.85, "speed_coeff": 0.76, "hp_reduction_per_sec": 150},
                    "tier_4": {"dmg_get_coeff": 1.325, "dmg_dealt_coeff": 0.8, "speed_coeff": 0.68, "hp_reduction_per_sec": 200},
                    "tier_5": {"dmg_get_coeff": 1.4, "dmg_dealt_coeff": 0.75, "speed_coeff": 0.6, "hp_reduction_per_sec": 250}},
               "blinded":
                   {"no_tier": {"dmg_dealt_coeff": 0.5, "speed_coeff": 0.4}},
               "stuned":
                   {"no_tier": {"dmg_dealt_coeff": 0.6, "speed_coeff": 0.8, "dmg_get_coeff": 1.5}},
               "flamed":
                   {"tier_1": {"dmg_get_coeff": 0.94, "dmg_dealt_coeff": 0.94, "hp_reduction_per_sec": 150},
                    "tier_2": {"dmg_get_coeff": 0.91, "dmg_dealt_coeff": 0.91, "hp_reduction_per_sec": 500},
                    "tier_3": {"dmg_get_coeff": 0.88, "dmg_dealt_coeff": 0.88, "hp_reduction_per_sec": 850},
                    "tier_4": {"dmg_get_coeff": 0.85, "dmg_dealt_coeff": 0.85, "hp_reduction_per_sec": 1200},
                    "tier_5": {"dmg_get_coeff": 0.82, "dmg_dealt_coeff": 0.82, "hp_reduction_per_sec": 1550}},
               "timed":
                   {"tier_1": {"ats_coeff": 0.85, "speed_coeff": 0.85},
                    "tier_2": {"ats_coeff": 0.7, "speed_coeff": 0.7},
                    "tier_3": {"ats_coeff": 0.55, "speed_coeff": 0.55},
                    "tier_4": {"ats_coeff": 0.4, "speed_coeff": 0.4},
                    "tier_5": {"ats_coeff": 0.25, "speed_coeff": 0.25}},
               "penetrated":
                   {"tier_1": {"dmg_get_coeff": 1.25, "speed_coeff": 1.05},
                    "tier_2": {"dmg_get_coeff": 1.5, "speed_coeff": 1.1},
                    "tier_3": {"dmg_get_coeff": 1.75, "speed_coeff": 1.15},
                    "tier_4": {"dmg_get_coeff": 2, "speed_coeff": 1.2},
                    "tier_5": {"dmg_get_coeff": 2.5, "speed_coeff": 1.25}},
               "unstability":
                   {"tier_1": {"dmg_get_coeff": 1.2, "speed_coeff": 0.9, "hp_reduction_per_sec": 100},
                    "tier_2": {"dmg_get_coeff": 1.4, "speed_coeff": 0.8, "hp_reduction_per_sec": 250},
                    "tier_3": {"dmg_get_coeff": 1.6, "speed_coeff": 0.7, "hp_reduction_per_sec": 400},
                    "tier_4": {"dmg_get_coeff": 1.8, "speed_coeff": 0.6, "hp_reduction_per_sec": 550},
                    "tier_5": {"dmg_get_coeff": 2, "speed_coeff": 0.5, "hp_reduction_per_sec": 700}},
               "sky_revenge":
                   {"tier_1": {"dmg_get_coeff": 1.2, "speed_coeff": 1.1, "dmg_dealt_coeff": 1.1,
                               "hp_reduction_per_sec": 100},
                    "tier_2": {"dmg_get_coeff": 1.6, "speed_coeff": 1.15, "dmg_dealt_coeff": 1.2,
                               "hp_reduction_per_sec": 300},
                    "tier_3": {"dmg_get_coeff": 2, "speed_coeff": 1.2, "dmg_dealt_coeff": 1.3,
                               "hp_reduction_per_sec": 500},
                    "tier_4": {"dmg_get_coeff": 2.5, "speed_coeff": 1.25, "dmg_dealt_coeff": 1.4,
                               "hp_reduction_per_sec": 750},
                    "tier_5": {"dmg_get_coeff": 3, "speed_coeff": 1.35, "dmg_dealt_coeff": 1.5,
                               "hp_reduction_per_sec": 1000}},
               "god_rage":
                   {"tier_1": {"dmg_get_coeff": 1.1, "speed_coeff": 0.95, "hp_reduction_per_sec": 100},
                    "tier_2": {"dmg_get_coeff": 1.25, "speed_coeff": 0.875, "hp_reduction_per_sec": 250},
                    "tier_3": {"dmg_get_coeff": 1.4, "speed_coeff": 0.8, "hp_reduction_per_sec": 400},
                    "tier_4": {"dmg_get_coeff": 1.55, "speed_coeff": 0.725, "hp_reduction_per_sec": 550},
                    "tier_5": {"dmg_get_coeff": 1.7, "speed_coeff": 0.65, "hp_reduction_per_sec": 750}},
               "slayed":
                   {"tier_1": {"dmg_get_coeff": 1.08, "speed_coeff": 0.95, "dmg_get_from_debuffs_coeff": 1.4,
                               "hp_reduction_per_sec": 50},
                    "tier_2": {"dmg_get_coeff": 1.16, "speed_coeff": 0.9, "dmg_get_from_debuffs_coeff": 1.8,
                               "hp_reduction_per_sec": 200},
                    "tier_3": {"dmg_get_coeff": 1.24, "speed_coeff": 0.85, "dmg_get_from_debuffs_coeff": 2.2,
                               "hp_reduction_per_sec": 350},
                    "tier_4": {"dmg_get_coeff": 1.32, "speed_coeff": 0.8, "dmg_get_from_debuffs_coeff": 2.6,
                               "hp_reduction_per_sec": 500},
                    "tier_5": {"dmg_get_coeff": 1.4, "speed_coeff": 0.75, "dmg_get_from_debuffs_coeff": 3,
                               "hp_reduction_per_sec": 650}},
               "freezed":
                   {"tier_1": {"dmg_get_coeff": 0.96, "speed_coeff": 0.92, "dmg_get_from_debuffs_coeff": 0.95},
                    "tier_2": {"dmg_get_coeff": 0.92, "speed_coeff": 0.84, "dmg_get_from_debuffs_coeff": 0.9},
                    "tier_3": {"dmg_get_coeff": 0.88, "speed_coeff": 0.76, "dmg_get_from_debuffs_coeff": 0.85},
                    "tier_4": {"dmg_get_coeff": 0.84, "speed_coeff": 0.68, "dmg_get_from_debuffs_coeff": 0.8},
                    "tier_5": {"dmg_get_coeff": 0.8, "speed_coeff": 0.6, "dmg_get_from_debuffs_coeff": 0.75}}
               }

game_weapons = {"warrior":
                    {"swords":
                         {"stag_blade":
                              {"base":
                                   {"D": {"size": 1.1, "dmg": 250, "ats": 2.1, "AoE": 135},
                                    "C": {"size": 1.3, "dmg": 280, "ats": 2.2, "AoE": 135},
                                    "B": {"size": 1.4, "dmg": 310, "ats": 2.3, "AoE": 135},
                                    "A": {"size": 1.5, "dmg": 350, "ats": 2.5, "AoE": 135},
                                    "S": {"size": 1.6, "dmg": 400, "ats": 2.7, "AoE": 135},
                                    "SR": {"size": 1.8, "dmg": 450, "ats": 3.1, "AoE": 135}}}}},
                "ranger":
                         {"handgun":
                              {"base":
                                   {"D": {"dmg": 150, "ats": 4, "proj_speed": 480},
                                    "C": {"dmg": 160, "ats": 4.2, "proj_speed": 490},
                                    "B": {"dmg": 175, "ats": 4.5, "proj_speed": 505},
                                    "A": {"dmg": 195, "ats": 4.9, "proj_speed": 530},
                                    "S": {"dmg": 220, "ats": 5.4, "proj_speed": 560},
                                    "SR": {"dmg": 250, "ats": 6, "proj_speed": 600},
                                    "lifetime": 2.3}},
                          "volcano":
                              {"base":
                                   {"D": {"dmg": 240, "ats": 19.8, "proj_speed": 840, "effect_len":
                                       {"flamed": 1}},
                                    "C": {"dmg": 248, "ats": 21.6, "proj_speed": 858, "effect_len":
                                       {"flamed": 1.2}},
                                    "B": {"dmg": 264, "ats": 24.3, "proj_speed": 900, "effect_len":
                                       {"flamed": 1.5}},
                                    "A": {"dmg": 280, "ats": 27, "proj_speed": 945, "effect_len":
                                       {"flamed": 1.8}},
                                    "S": {"dmg": 296, "ats": 30.6, "proj_speed": 990, "effect_len":
                                       {"flamed": 3}},
                                    "SR": {"dmg": 320, "ats": 36, "proj_speed": 1050, "effect_len":
                                       {"flamed": 2.3}},
                                    "lifetime": 1.8,
                                    "attack_effect": {"flamed": "tier_4"},
                                    "angle": 5}},
                          "plasma_flow":
                              {"base":
                                   {"D": {"dps": 1000, "proj_speed": 2000, "armor_pen": 1000, "effect_len":
                                       {"electrified": 3}},
                                    "C": {"dps": 1200, "proj_speed": 2000, "armor_pen": 1000, "effect_len":
                                        {"electrified": 3.5}},
                                    "B": {"dps": 1500, "proj_speed": 2000, "armor_pen": 1000, "effect_len":
                                        {"electrified": 4}},
                                    "A": {"dps": 1900, "proj_speed": 2000, "armor_pen": 1000, "effect_len":
                                        {"electrified": 4.5}},
                                    "S": {"dps": 2500, "proj_speed": 2000, "armor_pen": 1000, "effect_len":
                                        {"electrified": 5.5}},
                                    "SR": {"dps": 3200, "proj_speed": 2000, "armor_pen": 1000, "effect_len":
                                        {"electrified": 6.5}},
                                    "attack_effect": {"electrified": "tier_2"},
                                    "lifetime": 0.4,
                                    "speed_growth": 0.01,
                                    "dmg_growth": 0.25,
                                    "size_growth": 9}},
                          "shotgun":
                              {"base":
                                   {"D": {"dmg": 380, "ats": 0.75, "proj_speed": 840, "bullets": 4, "width": 45, "effect_len":
                                        {"stuned": 0.2}},
                                    "C": {"dmg": 400, "ats": 0.8, "proj_speed": 858, "bullets": 4, "width": 43.5, "effect_len":
                                        {"stuned": 0.21}},
                                    "B": {"dmg": 425, "ats": 0.85, "proj_speed": 900, "bullets": 5, "width": 41.25, "effect_len":
                                        {"stuned": 0.23}},
                                    "A": {"dmg": 460, "ats": 0.95, "proj_speed": 945, "bullets": 5, "width": 38.25, "effect_len":
                                        {"stuned": 0.26}},
                                    "S": {"dmg": 500, "ats": 1.07, "proj_speed": 990, "bullets": 5, "width": 34.5, "effect_len":
                                        {"stuned": 0.3}},
                                    "SR": {"dmg": 550, "ats": 1.25, "proj_speed": 1050, "bullets": 6, "width": 30, "effect_len":
                                        {"stuned": 0.35}},
                                    "lifetime": 0.6,
                                    "dmg_growth": 0.2,
                                    "attack_effect": {"stuned": "no_tier"}}},
                         "moon_blessing":
                              {"base":
                                   {"D": {"dmg": 3500, "ats": 1.05, "proj_speed": 960,
                                          "armor_pen": 5, "effect_len": 1.5},
                                    "C": {"dmg": 3600, "ats": 1.125, "proj_speed": 980,
                                          "armor_pen": 5, "effect_len": 1.6},
                                    "B": {"dmg": 3800, "ats": 1.23, "proj_speed": 1010,
                                          "armor_pen": 5, "effect_len": 1.75},
                                    "A": {"dmg": 4050, "ats": 1.38, "proj_speed": 1060,
                                          "armor_pen": 6, "effect_len": 1.95},
                                    "S": {"dmg": 4400, "ats": 1.575, "proj_speed": 1120,
                                          "armor_pen": 6, "effect_len": 2.2},
                                    "SR": {"dmg": 5000, "ats": 1.8, "proj_speed": 1200,
                                          "armor_pen": 7, "effect_len": 2.5},
                                    "lifetime": 2.5,
                                    "attack_effect": {"god_rage": "tier_3"},
                                    "speed_growth": 1.5,
                                    "dmg_growth": 1.2,
                                    "penetration_growth": 1.2,
                                    "size_growth": 3},
                               "alt":
                                   {"D": {"dmg": 1000, "ats": 2.4, "proj_speed": 480,
                                          "armor_pen": 2, "effect_len": 0.5},
                                    "C": {"dmg": 1070, "ats": 2.5, "proj_speed": 490,
                                          "armor_pen": 2, "effect_len": 0.6},
                                    "B": {"dmg": 1150, "ats": 2.7, "proj_speed": 505,
                                          "armor_pen": 2, "effect_len": 0.72},
                                    "A": {"dmg": 1250, "ats": 3, "proj_speed": 530,
                                          "armor_pen": 2, "effect_len": 0.85},
                                    "S": {"dmg": 1400, "ats": 3.4, "proj_speed": 560,
                                          "armor_pen": 3, "effect_len": 1},
                                    "SR": {"dmg": 1650, "ats": 4, "proj_speed": 600,
                                          "armor_pen": 3, "effect_len": 1.2},
                                    "attack_effect": {"sky_revenge": "tier_3"},
                                    "lifetime": 3,
                                    "size_growth": 1.8,
                                    "speed_growth": 1.5,
                                    "dmg_growth": 1.3,
                                    "penetration_growth": 1.5},
                               "change_time": 1.5},
                         "planetar_bomber":
                              {"base":
                                   {"D": {"dmg": 750, "ats": 3, "proj_speed": 640, "splash_size": 1.5, "effect_len":
                                       {"electrified": 1.5}},
                                    "C": {"dmg": 780, "ats": 3.1, "proj_speed": 653, "splash_size": 1.65, "effect_len":
                                       {"electrified": 1.575}},
                                    "B": {"dmg": 850, "ats": 3.3, "proj_speed": 670, "splash_size": 1.92, "effect_len":
                                       {"electrified": 1.725}},
                                    "A": {"dmg": 980, "ats": 3.6, "proj_speed": 706, "splash_size": 2.25, "effect_len":
                                       {"electrified": 1.95}},
                                    "S": {"dmg": 1030, "ats": 4, "proj_speed": 746, "splash_size": 2.7, "effect_len":
                                       {"electrified": 2.25}},
                                    "SR": {"dmg": 1200, "ats": 4.5, "proj_speed": 800, "splash_size": 3.3, "effect_len":
                                       {"electrified": 2.625}},
                                    "lifetime": 2,
                                    "splash_coeff": 0.5,
                                    "speed_growth": 4,
                                    "attack_effect": {"electrified": "tier_3"},
                                    "splash_effect": {"electrified": "tier_2"},
                                    "splash_effect_len": {"electrified": 1}},
                               "alt":
                                   {"D": {"dmg": 3500, "ats": 0.5, "proj_speed": 1200, "splash_size": 1, "effect_len":
                                       {"god_rage": 2, "stuned": 1}},
                                    "C": {"dmg": 3580, "ats": 0.52, "proj_speed": 1225, "splash_size": 1.1, "effect_len":
                                       {"god_rage": 2.1, "stuned": 1.07}},
                                    "B": {"dmg": 3710, "ats": 0.55, "proj_speed": 1260, "splash_size": 1.28, "effect_len":
                                       {"god_rage": 2.3, "stuned": 1.15}},
                                    "A": {"dmg": 3890, "ats": 0.6, "proj_speed": 1325, "splash_size": 1.5, "effect_len":
                                       {"god_rage": 2.6, "stuned": 1.25}},
                                    "S": {"dmg": 4120, "ats": 0.67, "proj_speed": 1400, "splash_size": 1.8, "effect_len":
                                       {"god_rage": 3, "stuned": 1.37}},
                                    "SR": {"dmg": 4500, "ats": 0.75, "proj_speed": 1500, "splash_size": 2.2, "effect_len":
                                       {"god_rage": 3.5, "stuned": 1.5}},
                                    "lifetime": 2.5,
                                    "splash_coeff": 0.4,
                                    "speed_growth": 4,
                                    "attack_effect": {"stuned": "no_tier", "god_rage": "tier_4"},
                                    "splash_effect": {"god_rage": "tier_3"},
                                    "splash_effect_len": {"god_rage": 0.8}},
                               "change_time": 1},
                          "rail_minigun":
                              {"base":
                                   {"D": {"dmg": 200, "ats": 12, "proj_speed": 1000, "splash_size": 1.5},
                                    "C": {"dmg": 215, "ats": 12.5, "proj_speed": 1030, "splash_size": 1.65},
                                    "B": {"dmg": 235, "ats": 13.5, "proj_speed": 1170, "splash_size": 1.92},
                                    "A": {"dmg": 260, "ats": 15, "proj_speed": 1150, "splash_size": 2.25},
                                    "S": {"dmg": 295, "ats": 17, "proj_speed": 1250, "splash_size": 2.7},
                                    "SR": {"dmg": 350, "ats": 20, "proj_speed": 1400, "splash_size": 3.3},
                                    "lifetime": 2,
                                    "splash_coeff": 1},
                               "alt":
                                   {"D": {"dmg": 7000, "ats": 0.6, "proj_speed": 1800, "armor_pen": 1000},
                                    "C": {"dmg": 7300, "ats": 0.615, "proj_speed": 1830, "armor_pen": 1000},
                                    "B": {"dmg": 7900, "ats": 0.645, "proj_speed": 1890, "armor_pen": 1000},
                                    "A": {"dmg": 8700, "ats": 0.69, "proj_speed": 2000, "armor_pen": 1000},
                                    "S": {"dmg": 10000, "ats": 0.75, "proj_speed": 2200, "armor_pen": 1000},
                                    "SR": {"dmg": 12000, "ats": 0.825, "proj_speed": 2500, "armor_pen": 1000},
                                    "lifetime": 2,
                                    "size_growth": 6,
                                    "damage_growth": 0.25},
                               "change_time": 3}
                          },
                "mage":
                    {"protector_timeblade":
                         {"base":
                                   {"D": {"size": 1, "dmg": 1500, "ats": 1.1, "AoE": 135},
                                    "C": {"size": 1.1, "dmg": 1580, "ats": 1.15, "AoE": 135},
                                    "B": {"size": 1.2, "dmg": 1700, "ats": 1.21, "AoE": 135},
                                    "A": {"size": 1.3, "dmg": 1850, "ats": 1.28, "AoE": 135},
                                    "S": {"size": 1.5, "dmg": 2030, "ats": 1.36, "AoE": 135},
                                    "SR": {"size": 1.7, "dmg": 2250, "ats": 1.45, "AoE": 135}}}}}

damage_col = {"weapons":
                  {"warrior": "orange", "mage": "purple", "ranger": "blue", "splash": "purple", "eff": "cyan"},
              "close_combat": "red",
              "room": "black"}

spawn_const = 200

levels_size = {
    1: (7 * sizes["stand_room"][0] + 6 * sizes["corridor"][0] + spawn_const,
        7 * sizes["stand_room"][1] + 6 * sizes["corridor"][0] + spawn_const),
    2: (7 * sizes["stand_room"][0] + 6 * sizes["corridor"][0] + spawn_const,
        7 * sizes["stand_room"][1] + 6 * sizes["corridor"][0] + spawn_const),
    3: (9 * sizes["stand_room"][0] + 8 * sizes["corridor"][0] + spawn_const,
        9 * sizes["stand_room"][1] + 8 * sizes["corridor"][0] + spawn_const),
    4: (9 * sizes["stand_room"][0] + 8 * sizes["corridor"][0] + spawn_const,
        9 * sizes["stand_room"][1] + 8 * sizes["corridor"][0] + spawn_const),
    5: (11 * sizes["stand_room"][0] + 10 * sizes["corridor"][0] + spawn_const,
        11 * sizes["stand_room"][1] + 10 * sizes["corridor"][0] + spawn_const)
}

levels = {1: {"size": (7, 7), "iters": [[2], [2, 2], [3, 4]]},
          2: {"size": (7, 7), "iters": [[2, 2], [2, 3], [2, 3, 4]]},
          3: {"size": (9, 9), "iters": [[2], [2, 2, 3], [2, 2, 4, 2], [2, 3]]},
          4: {"size": (9, 9), "iters": [[2, 2], [2, 2, 3], [2, 2, 3, 2], [2, 2, 2, 3, 4]]},
          5: {"size": (11, 11), "iters": [[2, 2, 3], [2, 2, 2, 2, 3, 3], [2, 2, 2, 2, 3], [2, 2, 3, 4], [2, 2, 3]]}}

enemiy_spawn = {
                1: {"close_combat":
                        {"standart":
                             {"ghast": {2: (2, 3), 3: (3, 4)},
                              "spider": {2: (5, 7), 3: (6, 7)}}}},
                2: {"close_combat":
                        {"standart":
                             {"ghast": {2: (3, 4), 3: (2, 3), 4: (4, 5)},
                              "demon_ghast": {2: (0, 0), 3: (1, 1), 4: (0, 0)},
                              "spider": {2: (5, 7), 3: (8, 10), 4: (15, 20)}}}},
                3: {"close_combat":
                        {"standart":
                             {"ghast": {2: (3, 5), 3: (3, 3), 4: (5, 6), 5: (0, 0)},
                              "demon_ghast": {2: (0, 0), 3: (1, 2), 4: (0, 0), 5: (2, 3)},
                              "spider": {2: (6, 10), 3: (7, 10), 4: (20, 25), 5: (5, 6)}}}},
                4: {"close_combat":
                        {"standart":
                             {"ghast": {2: (4, 5), 3: (3, 4), 4: (6, 7), 5: (2, 3)},
                              "demon_ghast": {2: (0, 1), 3: (2, 2), 4: (0, 1), 5: (3, 4)},
                              "spider": {2: (7, 12), 3: (8, 15), 4: (30, 32), 5: (7, 10)}}}},
                5: {"close_combat":
                        {"standart":
                             {"ghast": {2: (5, 6), 3: (3, 5), 4: (5, 6), 5: (4, 5), 6: (10, 11)},
                              "demon_ghast": {2: (1, 2), 3: (2, 3), 4: (1, 2), 5: (4, 4), 6: (1, 2)},
                              "spider": {2: (10, 14), 3: (11, 17), 4: (35, 38), 5: (10, 12), 6: (7, 10)}}}}
                }

doors = {(0, -1): "hu", (-1, 0): "vl", (1, 0): "vr", (0, 1): "hd"}

cur_weap = None
cur_rank = None
weapon_to_class_matcher = {"stag_blade": Stagnum_blade, "handgun": Handgun, "volcano": Volcano,
                           "moon_blessing": Moon_blessing, "planetar_bomber": Planetar_bomber,
                           "rail_minigun": Rail_minigun, "shotgun": Shotgun, "plasma_flow": Plasma_flow}
cur_class = "ranger"
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
            player.get_damage(0, "room", fps * 2)
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

    def rect(self):
        return self.rect


def anihillation(reason):
    global fon_set
    if reason == "death":
        fon_set = "death"
    elif reason == "win":
        fon_set = "win"


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
            anihillation("death")
        if self.timer:
            self.timer -= 1
        ret = pygame.sprite.spritecollideany(self.wall_collidable_sprite, heal_c)
        if ret:
            hp = ret.used()
            if hp < 1:
                self.cur_hp = (
                    self.cur_hp + self.max_hp * hp if self.cur_hp + self.max_hp * hp < self.max_hp else self.max_hp)
            else:
                self.cur_hp = (self.cur_hp + hp if self.cur_hp + hp < self.max_hp else self.max_hp)
        ret = self.on_col(x, y)
        if ret[0]:
            self.wall_collidable_sprite.rect.x += (classes[cur_class]["speed"] / fps) * x
        if ret[1]:
            self.wall_collidable_sprite.rect.y += (classes[cur_class]["speed"] / fps) * y
        if pygame.mouse.get_pos()[0] > self.rect.x:
            self.turn = 0
            self.image = sprite_images['player'][self.cl][0]
        elif pygame.mouse.get_pos()[0] < self.rect.x:
            self.turn = 1
            self.image = sprite_images['player'][self.cl][1]
        player_health_bar.apply(self.cur_hp)
        weapon.apply(self.rect, self.turn)
        for i in proj_gr:
            i.chpos(((classes[cur_class]["speed"] / fps) * x if ret[0] else 0),
                    ((classes[cur_class]["speed"] / fps) * y if ret[1] else 0))

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

    def get_damage(self, amount, entype, protection_time):
        if not self.timer:
            real_dmg = randint(int(0.9 * amount), int(1.1 * amount))
            damage.add_to_showlist(damage_col[entype],
                                   self.rect.x, self.rect.y - 1.5 * self.rect.h, real_dmg)
            self.cur_hp -= real_dmg
            self.timer += protection_time

    def transition(self):
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
                                                        self.y + 3, self.health_bar_size[0] * (
                                                            1 if hp > (i + 2) * 50 else (hp - (i + 1) * 50) / 50),
                                                        self.health_bar_size[1]))
        screen.blit(self.right_bar,
                    (self.x + (self.max_hp // 50 - 2) * self.medium_bar_rect.w + self.left_bar_rect.w, self.y))
        pygame.draw.rect(screen, "black",
                         (self.x + (self.max_hp // 50 - 2) * self.medium_bar_rect.w + self.left_bar_rect.w + 1,
                          self.y + 3, *self.health_bar_size))
        if hp > self.max_hp - 50:
            pygame.draw.rect(screen, (146, 0, 10),
                             (self.x + (self.max_hp // 50 - 2) * self.medium_bar_rect.w + self.left_bar_rect.w + 1,
                              self.y + 3,
                              self.health_bar_size[0] * (1 if hp == self.max_hp else (self.max_hp - hp) / 50),
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
        self.effects_dict = {"dmg_dealt_coeff": 1, "dmg_get_coeff": 1, "ats_coeff": 1, "speed_coeff": 1,
                             "hp_reduction_per_sec": 0, "dmg_get_from_debuffs_coeff": 1}
        self.cur_effects = {}
        for i in effect_list:
            self.cur_effects[i] = {}
            for j in effect_list[i]:
                self.cur_effects[i][j] = None
        self.dmg_timer = 0
        self.attack_timer = 0
        self.effect_coldown = 0

    def apply(self, x, y):
        if self.cur_hp <= 0:
            self.kill()
        ret = pygame.sprite.spritecollideany(self, player_gr)

        if ret and not self.attack_timer:
            self.attack_timer = (fps // self.ats + 1) * self.effects_dict["ats_coeff"]
            ret.get_damage(self.dmg * self.effects_dict["dmg_dealt_coeff"], self.entype, 0)
        elif self.attack_timer:
            self.attack_timer -= 1
        self.rect.x -= x
        self.rect.y -= y
        if self.dmg_timer:
            self.dmg_timer -= 1
        deltax = player.inf().rect.x - self.formspr.rect.x
        deltay = player.inf().rect.y + player.inf().rect.h // 2 - self.formspr.rect.y
        delta = (deltax ** 2 + deltay ** 2) ** 0.5
        if deltax or deltay:
            self.rect.x += (self.v / fps) * (deltax / delta) * self.effects_dict["speed_coeff"]
            self.formspr.rect.x += (self.v / fps) * (deltax / delta) * self.effects_dict["speed_coeff"]
            self.rect.y += (self.v / fps) * (deltay / delta) * self.effects_dict["speed_coeff"]
            self.formspr.rect.y += (self.v / fps) * (deltay / delta) * self.effects_dict["speed_coeff"]
        if self.effect_coldown == 0:
            self.get_damage(self.effects_dict["hp_reduction_per_sec"], 0, "eff")
            self.effect_coldown += 1
        else:
            self.effect_coldown = (self.effect_coldown + 1) % 12
            self.cur_hp -= (self.effects_dict["hp_reduction_per_sec"] *
                            self.effects_dict["dmg_get_from_debuffs_coeff"] / fps)
        for effects in self.cur_effects:
            for tier in self.cur_effects[effects]:
                if self.cur_effects[effects][tier] is not None and self.cur_effects[effects][tier] <= 0:
                    print(self.cur_effects[effects][tier], self.cur_effects)
                    self.cur_effects[effects][tier] = None
                    for i in effect_list[effects][tier]:
                        if i != "hp_reduction_per_sec":
                            self.effects_dict[i] /= effect_list[effects][tier][i]
                        else:
                            self.effects_dict[i] -= effect_list[effects][tier][i]
                elif self.cur_effects[effects][tier] is not None:
                    self.cur_effects[effects][tier] -= 1

    def get_damage(self, amount, time, weap_connected_to_class):
        if amount != 0 and not self.dmg_timer:
            if weap_connected_to_class != "eff":
                real_dmg = round(randint(int(0.9 * amount), int(1.1 * amount)) * self.effects_dict["dmg_get_coeff"], 1)

                damage.add_to_showlist(damage_col["weapons"][weap_connected_to_class],
                                   self.rect.x, self.rect.y - self.rect.h, real_dmg)
                self.cur_hp -= real_dmg
            else:
                self.cur_hp -= amount * self.effects_dict["dmg_get_from_debuffs_coeff"] / fps
                real_dmg = amount * self.effects_dict["dmg_get_from_debuffs_coeff"] / 5
                damage.add_to_showlist(damage_col["weapons"][weap_connected_to_class],
                                       self.rect.x, self.rect.y - self.rect.h, real_dmg, deltax=(-20, 20), deltay=(-100, 100))
            self.dmg_timer += time

    def get_effect(self, effs, effs_len):
        if effs:
            for i in range(len(effs)):
                if self.cur_effects[effs[i][0]][effs[i][1]] is not None:
                    self.cur_effects[effs[i][0]][effs[i][1]] = max(self.cur_effects[effs[i][0]][effs[i][1]], effs_len[i] * fps)
                else:
                    if (len(effect_list[effs[i][0]]) == 1 or not
                            any([(True if (not effect_list[effs[i][0]][tier] and int(tier[-1]) > int(effs[i][1][-1]))
                            else False) for tier in effect_list[effs[i][0]]])):
                        self.cur_effects[effs[i][0]][effs[i][1]] = effs_len[i] * fps
                        for j in effect_list[effs[i][0]][effs[i][1]]:
                            if j != "hp_reduction_per_sec":
                                self.effects_dict[j] *= effect_list[effs[i][0]][effs[i][1]][j]
                            else:
                                self.effects_dict[j] += effect_list[effs[i][0]][effs[i][1]][j]

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
                                 (b + 0.5 + y * 0.5) * sizes["stand_room"][0] + (b + 0.5 * y) * sizes["corridor"][
                                     0] + spawn_const // 2,
                                 (a + 0.5 + x * 0.5) * sizes["stand_room"][1] + (a + 0.5 * x) * sizes["corridor"][
                                     0] + spawn_const // 2, n)
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
                     (a + 0.5) * sizes["stand_room"][1] + a * sizes["corridor"][0] + spawn_const // 2, n,
                     num=data[a][b], empty=emptiness)
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
        self.weapon = weap
        self.weapon_class = weap_cl
        self.workl = weapon_to_class_matcher[self.weapon]()
        self.image = sprite_images["war_weapons"][self.weapon][self.position][0]
        self.size = game_weapons["warrior"][self.weapon]["base"][self.rank]["size"]
        self.image = pygame.transform.scale_by(self.image, self.size)
        self.rect = self.image.get_rect().move(0, 0)
        self.base_dmg = game_weapons["warrior"][self.weapon]["base"][self.rank]["dmg"]
        self.base_ats = game_weapons["warrior"][self.weapon]["base"][self.rank]["ats"]
        self.AoE = (game_weapons["warrior"][self.weapon]["base"][self.rank]["AoE"]
                    if self.weapon_class == "swords" else None)
        self.reload_timer = 0
        self.x, self.y = 0, 0

    def apply(self, rect, side):
        self.x = rect.x
        self.y = rect.y
        dt = self.workl.apply(self.x, self.y, side, self.rect, self.position,
                              self.weapon, self.AoE, self.base_ats, self.reload_timer, enemies, fps, self.base_dmg, self.size,
                              self.is_attacking, sprite_images, self)
        if "side" in dt:
            self.side = dt["side"]
        if "rect" in dt:
            self.rect = dt["rect"]
        if "pos" in dt:
            self.position = dt["pos"]
        if "timer" in dt:
            self.reload_timer = dt["timer"]
        if "is_att" in dt:
            self.is_attacking = dt["is_att"]
        if "image" in dt:
            self.image = dt["image"]

    def base_attack(self):
        if not self.is_attacking:
            self.position = "base_attack"
            self.is_attacking = True

    def ans_attacking(self):
        return self.is_attacking


class Ranger_weapon(pygame.sprite.Sprite):
    def __init__(self, rank, weap):
        super().__init__(weapon_gr, alls)
        self.cur_atk_type = "base"
        self.position = "hold"
        self.is_attacking = False
        self.side = False
        self.rank = rank
        self.weapon = weap

        self.image = sprite_images["ran_weapons"][self.weapon][self.position][0]
        self.data = game_weapons["ranger"][self.weapon]

        self.images = sprite_images["ran_weapons"][self.weapon]

        self.rect = self.image.get_rect().move(0, 0)
        self.workl = weapon_to_class_matcher[self.weapon](self.data, self.images, self.rank)

        self.x, self.y, self.w, self.h = 0, 0, 0, 0

    def apply(self, rect, side):
        self.x = rect.x
        self.y = rect.y
        self.w = rect.w
        self.h = rect.h
        data = self.workl.apply(self.x, self.y, side, self.rect, pygame.mouse.get_pos(), self.position, fps,
                              self.is_attacking, self.cur_atk_type)
        if "pos" in data:
            self.position = data["pos"]
        if "image" in data:
            self.image = data["image"]
        if "is_attacking" in data:
            self.is_attacking = data["is_attacking"]
        if "cur_atk_type" in data:
            self.cur_atk_type = data["cur_atk_type"]
        if "proj" in data:
            for dt in data["proj"]:
                proj = Projectile(dt["armor_pen"], dt["proj_speed"], dt["dmg"], dt["pos"],
                           dt["proj_img"], dt["lifetime"] * fps, dt["angle"], "player",
                           do_splash=dt.get("splash_coeff", 0), splash_img=dt.get("splash_img", None),
                           splash_size=dt.get("size", 0), size_growth=dt.get("size_growth", 1),
                           speed_growth=dt.get("speed_growth", 1), dmg_g=dt.get("dmg_g", 1),
                           pen_g=dt.get("pen_g", 1), proj_eff=dt.get("proj_effects", None),
                           eff_len=dt.get("effects_len", None), splash_eff=dt.get("splash_effects", None),
                           splash_eff_len=dt.get("splash_effect_len", None), ignore_walls=dt.get("ignoring", False))
            anim = Animation("reload_animation", fps / data["proj"][0]["ats"], self.x + self.w // 2, self.y - self.h)

    def base_attack(self):
        if not self.is_attacking and self.cur_atk_type == "base":
            self.position = "base_attack"
            self.is_attacking = True
        elif not self.is_attacking and self.cur_atk_type == "alt":
            self.position = "alt_attack"
            self.is_attacking = True

    def ans_attacking(self):
        return self.is_attacking

    def ch_atk_mode(self):
        if "alt" in self.data and self.cur_atk_type != "changing":
            self.cur_atk_type = "changing"
            anim = Animation("atk_type_change_animation",
                             self.data["change_time"] * fps, self.x, self.y - self.h)


class Animation(pygame.sprite.Sprite):
    def __init__(self, animation_type, time, x, y):
        super().__init__(animations, alls)
        self.anim_type = animation_type
        self.start_image = sprite_images["animations"][animation_type]
        self.image = self.start_image
        self.timer = time
        self.center = (x + self.image.get_rect().w // 2, y + self.image.get_rect().h // 2)
        self.time = time
        self.pos = x, y
        self.rect = self.image.get_rect().move(x, y)
        if self.anim_type == "atk_type_change_animation" or self.anim_type == "reload_animation":
            self.font = pygame.font.Font(None, 20)

    def apply(self):
        self.timer -= 1
        if self.anim_type == "atk_type_change_animation":
            text = self.font.render(str(round(self.timer / fps, 2)), True, "red")
            self.image = pygame.transform.rotate(self.start_image, 2 * (self.time - self.timer))
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = self.center[0] - self.image.get_rect().w // 2, self.center[1] - self.image.get_rect().h // 2
            screen.blit(text, (self.rect.x + self.rect.w // 2 - 13, self.rect.y + self.rect.h // 2 - 6))
        elif self.anim_type == "reload_animation":
            text = self.font.render(str(round(self.timer / fps, 2)), True, "green")
            self.image = pygame.transform.rotate(self.start_image, 2 * (self.time - self.timer))
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = self.center[0] - self.image.get_rect().w // 2, self.center[1] - self.image.get_rect().h // 2
            screen.blit(text, (self.rect.x + self.rect.w // 2 - 13, self.rect.y + self.rect.h // 2 - 6))
        if self.timer <= 0:
            self.kill()


class Projectile(pygame.sprite.Sprite):
    def __init__(self, lives, speed, dmg, cords, img, lifetime, angle, team, do_splash=0, splash_img=None,
                 splash_size=0, size_growth=1, speed_growth=1, dmg_g=1, pen_g=1, proj_eff=None, eff_len=None,
                 ignore_walls=False, splash_eff=None, splash_eff_len=None):
        super().__init__(proj_gr, alls, transition_killable)
        wcs = player.inf()
        self.image = pygame.transform.rotate(img, -angle)
        self.start_image = self.image
        self.angle = angle
        self.lifetimer = lifetime
        self.lifetime = lifetime
        self.center = list(cords)
        self.rect = self.image.get_rect().move(self.center[0] - self.image.get_rect().w // 2, self.center[1] - self.image.get_rect().h // 2)
        self.wcs = FormalRect(wcs.rect.x, wcs.rect.y, self.rect.w, self.rect.h)
        self.dmg = dmg
        self.hits = 0
        self.pen = lives
        self.speed = speed
        self.proj_eff = proj_eff
        self.eff_len = eff_len
        self.team = team
        self.block = []
        self.ds = do_splash
        self.splash_img = splash_img
        self.splash_size = splash_size
        self.size_growth = size_growth
        self.speed_growth = speed_growth
        self.dmg_growth = dmg_g
        self.penetration_growth = pen_g
        self.ignore_walls = ignore_walls
        self.splash_eff = splash_eff
        self.splash_eff_len = splash_eff_len

    def apply(self):
        self.lifetimer -= 1
        if self.size_growth > 1:
            self.image = pygame.transform.scale_by(self.start_image, (self.size_growth **
                                                                      ((self.lifetime - self.lifetimer) / fps)))
        self.rect.w, self.rect.h = self.image.get_rect().w, self.image.get_rect().h
        self.center[0] += self.speed * cos(radians(self.angle)) / fps * (self.speed_growth **
                                                                      ((self.lifetime - self.lifetimer) / fps))
        self.center[1] += self.speed * sin(radians(self.angle)) / fps * (self.speed_growth **
                                                                      ((self.lifetime - self.lifetimer) / fps))
        self.rect.x, self.rect.y = self.center[0] - self.rect.w // 2, self.center[1] - self.rect.h // 2
        self.wcs.rect.x += self.speed * cos(radians(self.angle)) / fps * (self.speed_growth **
                                                                      ((self.lifetime - self.lifetimer) / fps))
        self.wcs.rect.y += self.speed * sin(radians(self.angle)) / fps * (self.speed_growth **
                                                                      ((self.lifetime - self.lifetimer) / fps))
        self.pen = self.pen * (self.penetration_growth ** (1 / fps))
        ret = pygame.sprite.spritecollide(self, enemies, False)
        if ret:
            for i in ret:
                if i not in self.block and self.hits <= self.pen:
                    i.get_damage(self.dmg * (self.dmg_growth ** ((self.lifetime - self.lifetimer) / fps)),
                                 0, "ranger")
                    i.get_effect(self.proj_eff, self.eff_len)
                    self.block.append(i)
                    self.hits += 1
        if (self.pen <= self.hits or
                (any([pygame.sprite.spritecollideany((self.wcs if i != "hu" else
                FormalRect(self.wcs.rect.x, self.wcs.rect.y + 60, self.wcs.rect.w, self.wcs.rect.h)), walls[i]) for i in walls]) and not self.ignore_walls)
                or self.lifetimer <= 0):
            if self.ds:
                s = Splash(self.dmg * (self.dmg_growth ** ((self.lifetime - self.lifetimer) / fps)) * self.ds,
                           [self.rect.x + self.rect.w // 2, self.rect.y + self.rect.h // 2],
                           self.splash_img, self.splash_size, self.team, self.splash_eff, self.splash_eff_len)
            self.kill()

    def chpos(self, x, y):
        self.center[0] -= x * (self.speed_growth ** ((self.lifetime - self.lifetimer) / fps))
        self.center[1] -= y * (self.speed_growth ** ((self.lifetime - self.lifetimer) / fps))


class Splash(pygame.sprite.Sprite):
    def __init__(self, dmg, cords, img, size, team, eff, eff_len):
        super().__init__(proj_gr, alls, transition_killable)
        self.dmg = dmg
        self.lifetime = splash_lifetime_const * fps
        self.start_img = img
        self.image = img
        self.center = cords
        self.size = size
        self.image = pygame.transform.scale_by(self.start_img, 1 / self.lifetime * self.size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.center[0] - self.rect.w // 2, self.center[1] - self.rect.h // 2
        self.team = team
        self.timer = 0
        self.eff = eff
        self.eff_len = eff_len
        self.block = []

    def apply(self):
        self.timer += 1
        self.image = pygame.transform.scale_by(self.start_img, self.timer / self.lifetime * self.size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.center[0] - self.rect.w // 2, self.center[1] - self.rect.h // 2
        ret = pygame.sprite.spritecollide(self, enemies, False)
        if ret:
            for i in ret:
                if i not in self.block:
                    i.get_damage(self.dmg, 0, "splash")
                    i.get_effect(self.eff, self.eff_len)
                    self.block.append(i)
        if self.timer > self.lifetime:
            self.kill()

    def chpos(self, x, y):
        self.center[0] -= x
        self.center[1] -= y


class Damage():
    def __init__(self):
        self.damage_show_list = []
        self.max_time = 60

    def add_to_showlist(self, col, x, y, n, deltax=(0, 0), deltay=(0, 0)):
        font = pygame.font.Font(None, 40)
        text = font.render(str(-n), True, col)
        self.damage_show_list.append([text, (x + randint(*deltax), y + randint(*deltay)), self.max_time])

    def apply(self):
        x = self.damage_show_list
        deleting = []
        for i in range(len(x)):
            if x[i][2]:
                screen.blit(x[i][0], x[i][1])
                x[i][2] -= 1
            else:
                deleting.append(x[i])
        for i in deleting:
            self.damage_show_list.remove(i)


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    pygame.init()
    w, h = SX, SY
    screen_add = pygame.Surface((levels_size[1][0], levels_size[1][1]))
    screen = pygame.display.set_mode((w, h))
    data_fon = {"start": {0: get_image('Fon/Fon_start_1.png', False), 1: get_image('Fon/Fon_start_2.png', False),
                          2: get_image('Fon/Fon_start_3.png', False)}}
    fon_set = "start"
    pygame.display.set_caption("Soul fight")
    clock = pygame.time.Clock()
    player = None
    weapon = None

    sprite_images = {
                     'walls': {'hu': get_image('Other/Wall_brick_horizontal.png', False),
                               'hd': pygame.transform.rotate(get_image('Other/Wall_brick_horizontal.png', False), 180),
                               'vl': get_image('Other/Wall_brick_vertical.png', False),
                               'vr': pygame.transform.rotate(get_image('Other/Wall_brick_vertical.png', False), 180)},
                     'portals': {'room_transition': get_image('Other/Portal.png', True)},
                     'heals_consumable': {'healing_heart': get_image('Other/Healing_heart.png', True),
                                          'healing_heart_used': get_image('Other/Healing_heart_used.png', True)},
                     'bars': {'player':
                                  {'left': get_image('Other/Health_bar_left.png', True),
                                   'medium': get_image('Other/Health_bar_medium.png', True),
                                   'right': get_image('Other/Health_bar_right.png', True)}},
                     'floor': {1: get_image('Other/Floor_brick_1.png', False),
                               2: get_image('Other/Floor_brick_2.png', False),
                               3: get_image('Other/Floor_brick_3.png', False)},
                     'player': {'warrior': [get_image('Armor/Warrior_armor.png', True),
                                            pygame.transform.flip(get_image('Armor/Warrior_armor.png', True), 1, 0)],
                                'ranger': [get_image('Armor/Ranger_armor.png', True),
                                           pygame.transform.flip(get_image('Armor/Ranger_armor.png', True), 1, 0)]},
                     'animations': {'atk_type_change_animation': get_image('Other/Weapon_change_animation.png', True),
                                    'reload_animation': get_image('Other/Reload_animation.png', True)},
                     'enemies': {'close_combat':
                                     {'ghast': get_image('Enemies/Ghast.png', True),
                                      'demon_ghast': get_image('Enemies/Demon_ghast.png', True),
                                      'spider': get_image('Enemies/Spider.png', True)}},
                     'war_weapons':
               {'stag_blade':
                    {'default': [get_image('Warrior/Stagnum_blade.png', True),
                                 pygame.transform.flip(get_image('Warrior/Stagnum_blade.png', True), 1, 0)],
                     'hold': [get_image('Warrior/Stagnum_blade.png', True),
                                 pygame.transform.flip(get_image('Warrior/Stagnum_blade.png', True), 1, 0)],
                     'base_attack': [get_image('Warrior/Stagnum_blade.png', True),
                                 pygame.transform.flip(get_image('Warrior/Stagnum_blade.png', True), 1, 0)]}},
           'ran_weapons':
               {'handgun':
                    {'default': [get_image('Ranger/Handgun.png', True),
                                pygame.transform.flip(get_image('Ranger/Handgun.png', True), 1, 0)],
                     'hold': [get_image('Ranger/Handgun.png', True),
                                pygame.transform.flip(get_image('Ranger/Handgun.png', True), 1, 0)],
                     'base_attack': [get_image('Ranger/Handgun.png', True),
                                pygame.transform.flip(get_image('Ranger/Handgun.png', True), 1, 0)],
                     'base_proj': pygame.transform.flip(get_image('Ranger/Ammo/Handgun_bullet.png', True), 1, 0)},
                'volcano':
                    {'default': [get_image('Ranger/Volcano.png', True),
                                pygame.transform.flip(get_image('Ranger/Volcano.png', True), 1, 0)],
                     'hold': [get_image('Ranger/Volcano.png', True),
                                pygame.transform.flip(get_image('Ranger/Volcano.png', True), 1, 0)],
                     'base_attack':[get_image('Ranger/Volcano.png', True),
                                pygame.transform.flip(get_image('Ranger/Volcano.png', True), 1, 0)],
                     'base_proj': pygame.transform.flip(get_image('Ranger/Ammo/Volcano_bullet.png', True), 1, 0)},
                'moon_blessing':
                    {'default': [get_image('Ranger/Moon_blessing.png', True),
                                pygame.transform.flip(get_image('Ranger/Moon_blessing.png', True), 1, 0)],
                     'hold': [get_image('Ranger/Moon_blessing.png', True),
                                pygame.transform.flip(get_image('Ranger/Moon_blessing.png', True), 1, 0)],
                     'alt_hold': [get_image('Ranger/Moon_blessing.png', True),
                                pygame.transform.flip(get_image('Ranger/Moon_blessing.png', True), 1, 0)],
                     'base_attack': [get_image('Ranger/Moon_blessing.png', True),
                                pygame.transform.flip(get_image('Ranger/Moon_blessing.png', True), 1, 0)],
                     'alt_attack': [get_image('Ranger/Moon_blessing.png', True),
                                pygame.transform.flip(get_image('Ranger/Moon_blessing.png', True), 1, 0)],
                     'base_proj': pygame.transform.flip(get_image('Ranger/Ammo/Moon_blessing_arrow.png', True), 1, 0),
                     'alt_proj': pygame.transform.flip(get_image('Ranger/Ammo/Moon_blessing_ray.png', True), 1, 0)},
                'planetar_bomber':
                    {'default': [get_image('Ranger/Planetar_bomber.png', True),
                                 pygame.transform.flip(get_image('Ranger/Planetar_bomber.png', True), 1, 0)],
                     'hold': [get_image('Ranger/Planetar_bomber.png', True),
                              pygame.transform.flip(get_image('Ranger/Planetar_bomber.png', True), 1, 0)],
                     'alt_hold': [pygame.transform.flip(get_image('Ranger/Planetar_bomber.png', True), 1, 0),
                                  get_image('Ranger/Planetar_bomber.png', True)],
                     'base_attack': [get_image('Ranger/Planetar_bomber.png', True),
                                     pygame.transform.flip(get_image('Ranger/Planetar_bomber.png', True), 1, 0)],
                     'alt_attack': [pygame.transform.flip(get_image('Ranger/Planetar_bomber.png', True), 1, 0),
                                    get_image('Ranger/Planetar_bomber.png', True)],
                     'base_proj': pygame.transform.flip(get_image('Ranger/Ammo/Planetar_bomber_rocket_small.png',
                                                                  True), 1, 0),
                     'alt_proj': pygame.transform.flip(get_image('Ranger/Ammo/Planetar_bomber_rocket_big.png',
                                                                 True), 1, 0),
                     'base_splash': get_image('Ranger/Splashes/Planetar_bomber_rocket_small_splash.png', True),
                     'alt_splash': get_image('Ranger/Splashes/Planetar_bomber_rocket_big_splash.png', True)},
                "rail_minigun":
                    {'default': [get_image('Ranger/Rail_minigun/Rail_minigun.png', True),
                                 pygame.transform.flip(get_image('Ranger/Rail_minigun/Rail_minigun.png', True), 1, 0)],
                     'hold': [get_image('Ranger/Rail_minigun/Rail_minigun.png', True),
                              pygame.transform.flip(get_image('Ranger/Rail_minigun/Rail_minigun.png', True), 1, 0)],
                     'alt_hold': [get_image('Ranger/Rail_minigun/Rail_minigun.png', True),
                                     pygame.transform.flip(get_image('Ranger/Rail_minigun/Rail_minigun.png', True), 1, 0)],
                     'base_attack': [get_image('Ranger/Rail_minigun/Rail_minigun_base_attack.png', True),
                                     pygame.transform.flip(get_image('Ranger/Rail_minigun/Rail_minigun_base_attack.png', True), 1, 0)],
                     'alt_attack': [get_image('Ranger/Rail_minigun/Rail_minigun_alt_attack.png', True),
                                     pygame.transform.flip(get_image('Ranger/Rail_minigun/Rail_minigun_alt_attack.png', True), 1, 0)],
                     'base_proj': pygame.transform.flip(get_image('Ranger/Ammo/Rail_minigun_bullet.png',
                                                                  True), 1, 0),
                     'alt_proj': pygame.transform.flip(pygame.transform.scale_by(get_image('Ranger/Ammo/Rail_minigun_ray.png',
                                                                 True), 2), 1, 0),
                     'base_splash': get_image('Ranger/Splashes/Rail_minigun_bullet_splash.png', True)},
                'shotgun':
                    {'default': [get_image('Ranger/Shotgun.png', True),
                                 pygame.transform.flip(get_image('Ranger/Shotgun.png', True), 1, 0)],
                     'hold': [get_image('Ranger/Shotgun.png', True),
                              pygame.transform.flip(get_image('Ranger/Shotgun.png', True), 1, 0)],
                     'base_attack': [get_image('Ranger/Shotgun.png', True),
                                     pygame.transform.flip(get_image('Ranger/Shotgun.png', True), 1, 0)],
                     'base_proj': pygame.transform.flip(get_image('Ranger/Ammo/Shotgun_bullet.png', True), 1, 0)},
                'plasma_flow':
                    {'default': [get_image('Ranger/Plasma_flow.png', True),
                                 pygame.transform.flip(get_image('Ranger/Plasma_flow.png', True), 1, 0)],
                     'hold': [get_image('Ranger/Plasma_flow.png', True),
                              pygame.transform.flip(get_image('Ranger/Plasma_flow.png', True), 1, 0)],
                     'base_attack': [get_image('Ranger/Plasma_flow.png', True),
                                     pygame.transform.flip(get_image('Ranger/Plasma_flow.png', True), 1, 0)],
                     'base_proj': pygame.transform.flip(get_image('Ranger/Ammo/Plasma_flow_ray.png', True), 1, 0)}}}
    damage = Damage()
    screen_x = -levels_size[1][0] // 2 + SX // 2
    screen_y = -levels_size[1][1] // 2 + SY // 2
    count = 0
    cur_lvl = None
    atk_butt_pressed = False
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
                                if cur_lvl < 5:
                                    cur_lvl += 1
                                    screen_x = -levels_size[cur_lvl][0] // 2 + SX // 2
                                    screen_y = -levels_size[cur_lvl][1] // 2 + SY // 2
                                    screen_add = pygame.Surface((levels_size[cur_lvl][0], levels_size[cur_lvl][1]))
                                    player.transition()
                                    for i in transition_killable:
                                        i.kill()
                                    screen_add.fill("black")
                                    generate_level(cur_lvl)
                                    break
                                else:
                                    anihillation("win")

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
                    if event.key == pygame.K_c:
                        weapon.ch_atk_mode()

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
                            cur_rank = "SR"
                            player = Player("warrior")
                            weapon = Warrior_weapon(cur_rank, cur_weap, weapon_class)
                        if cur_class == "ranger":
                            cur_weap = "handgun"
                            cur_rank = "SR"
                            player = Player("ranger")
                            weapon = Ranger_weapon(cur_rank, cur_weap)
                        player_health_bar = PlayerHealthBar(200, 150, classes[cur_class]["hp"])
                elif fon_set == "game" and event.button == pygame.BUTTON_LEFT:
                    atk_butt_pressed = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if fon_set == "game" and event.button == pygame.BUTTON_LEFT:
                    atk_butt_pressed = False
        if atk_butt_pressed:
            weapon.base_attack()
        if fon_set == "death":
            for i in alls:
                i.kill()
            screen.fill("black")
            screen_add.fill("black")
            font = pygame.font.Font(None, 200)
            text = font.render("You died", True, (255, 100, 100))
            screen.blit(text, (SX // 2 - 300, SY // 2 - 100))
        elif fon_set == "win":
            for i in alls:
                i.kill()
            screen.fill("black")
            screen_add.fill("black")
            font = pygame.font.Font(None, 200)
            text = font.render("You won", True, (100, 255, 100))
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
            for i in proj_gr:
                i.apply()
            proj_gr.draw(screen)
            for i in animations:
                i.apply()
            animations.draw(screen)
            for i in rooms:
                i.check()
            for i in enemies:
                i.apply(((classes[cur_class]["speed"] / fps) * dx if res[0] else 0),
                        ((classes[cur_class]["speed"] / fps) * dy if res[1] else 0))
            enemies.draw(screen)
            damage.apply()
        pygame.display.flip()
        clock.tick(fps)
