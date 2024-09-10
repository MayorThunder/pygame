from random import randint

import pygame
from math import asin, degrees


class Stagnum_blade():
    def apply(self, x, y, side, rect, position, weapon, AoE, base_ats, timer, enemies, fps, base_dmg, size,
            is_attacking, sprite_images, s):
        cox1 = 154 * size ** 1.15
        cox2 = -65 * size ** 1.05
        coy = -121 * size ** 0.6
        formx = (-rect.w + cox1 if not side else rect.w + cox2)
        formy = rect.h + coy
        if not is_attacking:
            image = pygame.transform.scale_by(
                sprite_images['war_weapons'][weapon][position][1 if side else 0], size)
            rect.x = x - formx
            rect.y = y - formy
        elif timer < fps / base_ats:
            timer += 1
            image = pygame.transform.rotate(pygame.transform.scale_by(
                sprite_images["war_weapons"][weapon][position][1 if side else 0], size),
                AoE / (fps / base_ats) * timer * (1 if side else -1))
            rect.x = x - formx - 25
            rect.y = y - formy - 15
            ret = pygame.sprite.spritecollide(s, enemies, False)
            if ret:
                for i in ret:
                    i.get_damage(base_dmg, (fps // base_ats - timer) + 2, "warrior")
        else:
            timer = 0
            is_attacking = False
            position = "hold"
            image = pygame.transform.scale_by(
                sprite_images["war_weapons"][weapon][position][1 if side else 0], size)
            rect.x = x - formx
            rect.y = y - formy
        return {"side": side, "rect": rect, "pos": position, "timer": timer, "is_att": is_attacking,
                    "image": image}


class Handgun():
    def __init__(self, data, ims, rank):
        self.reload_timer = 0
        self.data = data
        self.images = ims
        self.rank = rank

    def apply(self, x, y, side, rect, mpos, position, fps, is_attacking, *args):
        proj = None
        coy = 65
        cox1 = 60
        cox2 = 45
        rect.x = x - rect.w + (cox1 if not side else cox2)
        rect.y = y - rect.h + coy
        center = (rect.x + rect.w // 2, rect.y + rect.h // 3)
        mpos_x, mpos_y = mpos
        angle = degrees(asin((mpos_y - center[1]) / ((mpos_x - center[0])
                                                     ** 2 + (mpos_y - center[1]) ** 2) ** 0.5))
        real_angle = (angle if not side else -angle + 180)
        if not side:
            angle = -angle
        image = pygame.transform.rotate(self.images[position][1 if side else 0], angle)
        if is_attacking and self.reload_timer == 0:
            proj = [{"angle": real_angle, "pos": center,
                     "dmg": self.data["base"][self.rank]["dmg"], "ats": self.data["base"][self.rank]["ats"],
                     "armor_pen": 1,
                     "proj_speed": self.data["base"][self.rank]["proj_speed"],
                     "lifetime": self.data["base"]["lifetime"], "proj_img": self.images["base_proj"]}]
            self.reload_timer += 1
        elif 0 < self.reload_timer < fps / self.data["base"][self.rank]["ats"]:
            self.reload_timer += 1
        else:
            self.reload_timer = 0
            is_attacking = False
            position = "hold"
        ret = {"side": side, "pos": position, "image": image, "is_attacking": is_attacking}
        if proj:
            ret["proj"] = proj
        return ret


class Shotgun():
    def __init__(self, data, ims, rank):
        self.reload_timer = 0
        self.data = data
        self.images = ims
        self.rank = rank
        self.delta = self.data["base"][self.rank]["width"] / (self.data["base"][self.rank]["bullets"] - 1)

    def apply(self, x, y, side, rect, mpos, position, fps, is_attacking, *args):
        proj = None
        coy = 70
        cox1 = 110
        cox2 = 50
        rect.x = x - rect.w + (cox1 if not side else cox2)
        rect.y = y - rect.h + coy
        center = (rect.x + rect.w // 2, rect.y + rect.h // 2)
        mpos_x, mpos_y = mpos
        angle = degrees(asin((mpos_y - center[1]) / ((mpos_x - center[0])
                                                     ** 2 + (mpos_y - center[1]) ** 2) ** 0.5))
        real_angle = (angle if not side else -angle + 180)
        if not side:
            angle = -angle
        image = pygame.transform.rotate(self.images[position][1 if side else 0], angle)
        if is_attacking and self.reload_timer == 0:
            proj = []
            ef_len = [self.data["base"][self.rank]["effect_len"][i] for i in self.data["base"]["attack_effect"].keys()]
            for i in range(self.data["base"][self.rank]["bullets"]):
                proj.append({"angle": real_angle - (self.data["base"][self.rank]["width"] // 2) + self.delta * i, "pos": center,
                        "dmg": self.data["base"][self.rank]["dmg"], "armor_pen": 1,
                        "proj_speed": self.data["base"][self.rank]["proj_speed"], "ats": self.data["base"][self.rank]["ats"],
                        "lifetime": self.data["base"]["lifetime"], "proj_img": self.images["base_proj"],
                        "dmg_g": self.data["base"]["dmg_growth"],
                        "proj_effects": [[i, j] for (i, j) in self.data["base"]["attack_effect"].items()],
                        "effects_len": ef_len})
            self.reload_timer += 1
        elif 0 < self.reload_timer < fps / self.data["base"][self.rank]["ats"]:
            self.reload_timer += 1
        else:
            self.reload_timer = 0
            is_attacking = False
            position = "hold"
        ret = {"side": side, "pos": position, "image": image, "is_attacking": is_attacking}
        if proj:
            ret["proj"] = proj
        return ret


class Volcano():
    def __init__(self, data, ims, rank):
        self.reload_timer = 0
        self.data = data
        self.images = ims
        self.rank = rank

    def apply(self, x, y, side, rect, mpos, position, fps, is_attacking, *args):
        proj = None
        coy = 85
        cox1 = 110
        cox2 = 50
        rect.x = x - rect.w + (cox1 if not side else cox2)
        rect.y = y - rect.h + coy
        center = (rect.x + rect.w // 2, rect.y + rect.h // 2)
        mpos_x, mpos_y = mpos
        angle = degrees(asin((mpos_y - center[1]) / ((mpos_x - center[0])
                                                     ** 2 + (mpos_y - center[1]) ** 2) ** 0.5))
        real_angle = (angle if not side else -angle + 180)
        if not side:
            angle = -angle
        image = pygame.transform.rotate(self.images[position][1 if side else 0], angle)
        if is_attacking and self.reload_timer == 0:
            real_angle = real_angle + randint(-self.data["base"]["angle"] * 10, self.data["base"]["angle"] * 10) / 10
            ef_len = [self.data["base"][self.rank]["effect_len"][i] for i in self.data["base"]["attack_effect"].keys()]
            proj = [{"angle": real_angle, "pos": center,
                    "dmg": self.data["base"][self.rank]["dmg"], "armor_pen": 1,
                    "proj_speed": self.data["base"][self.rank]["proj_speed"], "ats": self.data["base"][self.rank]["ats"],
                    "lifetime": self.data["base"]["lifetime"], "proj_img": self.images["base_proj"],
                    "proj_effects": [[i, j] for (i, j) in self.data["base"]["attack_effect"].items()],
                    "effects_len": ef_len}]
            self.reload_timer += 1
        elif 0 < self.reload_timer < fps / self.data["base"][self.rank]["ats"]:
            self.reload_timer += 1
        else:
            self.reload_timer = 0
            is_attacking = False
            position = "hold"
        ret = {"side": side, "pos": position, "image": image, "is_attacking": is_attacking}
        if proj:
            ret["proj"] = proj
        return ret


class Moon_blessing():
    def __init__(self, data, ims, rank):
        self.reload_timer = 0
        self.change_timer = 0
        self.data = data
        self.images = ims
        self.rank = rank
        self.ch_to = "alt"

    def apply(self, x, y, side, rect, mpos, position, fps, is_attacking, CAT):
        proj = None
        coy = 75
        cox1 = 40
        cox2 = 25
        rect.x = x - rect.w + (cox1 if not side else cox2)
        rect.y = y - rect.h + coy
        center = (rect.x + rect.w // 2, rect.y + rect.h // 2)
        mpos_x, mpos_y = mpos
        angle = degrees(asin((mpos_y - center[1]) / ((mpos_x - center[0])
                                                                ** 2 + (mpos_y - center[1]) ** 2) ** 0.5))
        real_angle = (angle if not side else -angle + 180)
        if not side:
            angle = -angle
        image = pygame.transform.rotate(self.images[position][1 if side else 0], angle)
        if CAT != "changing":
            if is_attacking and self.reload_timer == 0:
                ef_len = self.data[CAT][self.rank]["effect_len"]
                proj = [{"angle": real_angle, "pos": center,
                        "dmg": self.data[CAT][self.rank]["dmg"], "armor_pen": self.data[CAT][self.rank]["armor_pen"],
                        "proj_speed": self.data[CAT][self.rank]["proj_speed"], "ats": self.data[CAT][self.rank]["ats"],
                        "lifetime": self.data[CAT]["lifetime"],
                        "proj_img": self.images[f"{CAT}_proj"], "size_growth": self.data[CAT].get("size_growth", 1),
                        "speed_growth": self.data[CAT].get("speed_growth", 1),
                        "dmg_g": self.data[CAT].get("dmg_growth", 1),
                        "pen_g": self.data[CAT].get("penetration_growth", 1), "proj_effects": [[i, j] for (i, j) in self.data[CAT]["attack_effect"].items()],
                        "effects_len": [ef_len]}]
                self.reload_timer += 1
            elif 0 < self.reload_timer < fps / (self.data["base"][self.rank]["ats"] if CAT == "base" else
            self.data["alt"][self.rank]["ats"]):
                self.reload_timer += 1
            else:
                self.reload_timer = 0
                is_attacking = False
                position = "hold"
        elif CAT == "changing" and self.change_timer < self.data["change_time"] * fps:
            self.change_timer += 1
        else:
            if self.ch_to == "base":
                self.ch_to = "alt"
                CAT = "base"
            else:
                self.ch_to = "base"
                CAT = "alt"
            self.change_timer = 0
        ret = {"pos": position, "image": image, "is_attacking": is_attacking, "cur_atk_type": CAT}
        if proj:
            ret["proj"] = proj
        return ret


class Planetar_bomber():
    def __init__(self, data, ims, rank):
        self.reload_timer = 0
        self.change_timer = 0
        self.data = data
        self.images = ims
        self.rank = rank
        self.ch_to = "alt"

    def apply(self, x, y, side, rect, mpos, position, fps, is_attacking, CAT):
        proj = None
        coy = 60
        cox1 = 70
        cox2 = 120
        if self.ch_to == "alt":
            rect.x = x - rect.w + (cox1 if not side else cox2)
            rect.y = y - rect.h + coy
        else:
            rect.x = x - rect.w + (cox1 if side else cox2)
            rect.y = y - rect.h + coy
        center = (rect.x + rect.w // 2, rect.y + rect.h // 2)
        mpos_x, mpos_y = mpos
        angle = degrees(asin((mpos_y - center[1]) / ((mpos_x - center[0])
                                                                ** 2 + (mpos_y - center[1]) ** 2) ** 0.5))
        real_angle = (angle if not side else -angle + 180)
        if not side:
            angle = -angle
        image = pygame.transform.rotate(self.images[position][1 if side else 0], angle)
        if CAT != "changing":
            if is_attacking and self.reload_timer == 0:
                ef_len = [self.data[CAT][self.rank]["effect_len"][i] for i in
                          self.data[CAT]["attack_effect"].keys()]
                spl_len = [self.data[CAT][self.rank]["effect_len"][i] * self.data[CAT]["splash_effect_len"][i] for i in
                          self.data[CAT]["splash_effect"].keys()]
                proj = [{"angle": real_angle, "pos": center,
                        "dmg": self.data[CAT][self.rank]["dmg"], "armor_pen": 1,
                        "proj_speed": self.data[CAT][self.rank]["proj_speed"], "ats": self.data[CAT][self.rank]["ats"],
                        "lifetime": self.data[CAT]["lifetime"], "splash_coeff": self.data[CAT]["splash_coeff"],
                        "size": self.data[CAT][self.rank]["splash_size"], "proj_img": self.images[f"{CAT}_proj"],
                        "splash_img": self.images[f"{CAT}_splash"], "speed_growth": self.data[CAT]["speed_growth"],
                        "proj_effects": [[i, j] for (i, j) in self.data[CAT]["attack_effect"].items()],
                        "effects_len": ef_len,
                        "splash_effects": [[i, j] for (i, j) in self.data[CAT]["splash_effect"].items()],
                        "splash_effect_len": spl_len}]
                self.reload_timer += 1
            elif 0 < self.reload_timer < fps / self.data[CAT][self.rank]["ats"]:
                self.reload_timer += 1
            else:
                self.reload_timer = 0
                is_attacking = False
                position = ("hold" if self.ch_to == "alt" else "alt_hold")
        elif CAT == "changing" and self.change_timer < self.data["change_time"] * fps:
            self.change_timer += 1
        else:
            if self.ch_to == "base":
                self.ch_to = "alt"
                CAT = "base"
                position = "hold"
            else:
                self.ch_to = "base"
                CAT = "alt"
                position = "alt_hold"
            self.change_timer = 0
        ret = {"pos": position, "image": image, "is_attacking": is_attacking, "cur_atk_type": CAT}
        if proj:
            ret["proj"] = proj
        return ret


class Rail_minigun():
    def __init__(self, data, ims, rank):
        self.reload_timer = 0
        self.change_timer = 0
        self.data = data
        print(self.data)
        self.images = ims
        self.rank = rank
        self.ch_to = "alt"

    def apply(self, x, y, side, rect, mpos, position, fps, is_attacking, CAT):
        proj = None
        coy = 90
        cox1 = 140
        cox2 = 80
        rect.x = x - rect.w + (cox1 if not side else cox2)
        rect.y = y - rect.h + coy
        center = (rect.x + rect.w // 2, rect.y + rect.h // 2)
        mpos_x, mpos_y = mpos
        angle = degrees(asin((mpos_y - center[1]) / ((mpos_x - center[0])
                                                                ** 2 + (mpos_y - center[1]) ** 2) ** 0.5))
        real_angle = (angle if not side else -angle + 180)
        if not side:
            angle = -angle
        image = pygame.transform.rotate(self.images[position][1 if side else 0], angle)
        if CAT != "changing":
            if is_attacking and self.reload_timer == 0:
                proj = [{"angle": real_angle, "pos": (center[0], center[1] + rect.h // 4),
                        "dmg": self.data[CAT][self.rank]["dmg"], "armor_pen": self.data[CAT][self.rank].get("armor_pen", 1),
                        "proj_speed": self.data[CAT][self.rank]["proj_speed"], "ats": self.data[CAT][self.rank]["ats"],
                        "lifetime": self.data[CAT]["lifetime"],
                        "splash_coeff": self.data[CAT].get("splash_coeff", 0),
                        "size": self.data[CAT][self.rank].get("splash_size", 0), "proj_img": self.images[f"{CAT}_proj"],
                        "splash_img": self.images.get(f"{CAT}_splash", None),
                        "size_growth": self.data[CAT].get("size_growth", 1),
                        "dmg_g": self.data[CAT].get("damage_growth", 1)}]
                self.reload_timer += 1
            elif 0 < self.reload_timer < fps / (self.data["base"][self.rank]["ats"] if CAT == "base" else
            self.data["alt"][self.rank]["ats"]):
                self.reload_timer += 1
            else:
                self.reload_timer = 0
                is_attacking = False
                position = "hold"
        elif CAT == "changing" and self.change_timer < self.data["change_time"] * fps:
            self.change_timer += 1
        else:
            if self.ch_to == "base":
                self.ch_to = "alt"
                CAT = "base"
            else:
                self.ch_to = "base"
                CAT = "alt"
            self.change_timer = 0
        ret = {"pos": position, "image": image, "is_attacking": is_attacking, "cur_atk_type": CAT}
        if proj:
            ret["proj"] = proj
        return ret


class Plasma_flow():
    def __init__(self, data, ims, rank):
        self.reload_timer = 0
        self.data = data
        self.images = ims
        self.rank = rank

    def apply(self, x, y, side, rect, mpos, position, fps, is_attacking, *args):
        proj = None
        coy = 85
        cox1 = 110
        cox2 = 50
        rect.x = x - rect.w + (cox1 if not side else cox2)
        rect.y = y - rect.h + coy
        center = (rect.x + rect.w // 2, rect.y + rect.h // 3)
        mpos_x, mpos_y = mpos
        angle = degrees(asin((mpos_y - center[1]) / ((mpos_x - center[0])
                                                     ** 2 + (mpos_y - center[1]) ** 2) ** 0.5))
        real_angle = (angle if not side else -angle + 180)
        if not side:
            angle = -angle
        image = pygame.transform.rotate(self.images[position][1 if side else 0], angle)
        if is_attacking and self.reload_timer == 0:
            ef_len = [self.data["base"][self.rank]["effect_len"][i] for i in self.data["base"]["attack_effect"].keys()]
            proj = [{"angle": real_angle, "pos": center,
                    "dmg": self.data["base"][self.rank]["dps"] / fps, "armor_pen": self.data["base"][self.rank]["armor_pen"],
                    "proj_speed": self.data["base"][self.rank]["proj_speed"], "ats": fps,
                    "lifetime": self.data["base"]["lifetime"], "proj_img": self.images["base_proj"],
                    "speed_growth": self.data["base"]["speed_growth"], "size_growth": self.data["base"]["size_growth"],
                    "dmg_growth": self.data["base"]["dmg_growth"],
                    "proj_effects": [[i, j] for (i, j) in self.data["base"]["attack_effect"].items()],
                    "effects_len": ef_len, "ignoring": True}]
            self.reload_timer += 1
        elif 0 < self.reload_timer < 1:
            self.reload_timer += 1
        else:
            self.reload_timer = 0
            is_attacking = False
            position = "hold"
        ret = {"side": side, "pos": position, "image": image, "is_attacking": is_attacking}
        if proj:
            ret["proj"] = proj
        return ret